"""
DMIT AI Consultant — LLM provider with resilient retry + circuit-breaker.

Provider chain (in order):
  1. Groq  — llama-3.3-70b-versatile  (primary, fast)
  2. Groq  — llama-3.1-70b-versatile  (secondary Groq model)
  3. Groq  — llama-3.1-8b-instant     (fast fallback, higher TPM)
  4. NVIDIA — deepseek-v4-flash-0731  (final fallback)

Resilience features:
  • Exponential backoff with Retry-After header respect on 429s
  • Per-provider circuit-breaker (stops routing to dead providers for a cooldown)
  • Token budget enforcement — trims history so we never hit TPM limits
  • Graceful degradation — always yields a user-visible error if all providers fail
"""
from __future__ import annotations

import asyncio
import logging
import os
import time
from typing import AsyncGenerator, Dict, Any, List, Optional

logger = logging.getLogger(__name__)

# ── Credentials ────────────────────────────────────────────────────────────────

NVIDIA_API_KEY  = os.getenv("NVIDIA_API_KEY",  "")
NVIDIA_BASE_URL = "https://integrate.api.nvidia.com/v1"
NVIDIA_MODEL    = "deepseek-ai/deepseek-v4-flash-0731"

GROQ_API_KEY    = os.getenv("GROQ_API_KEY",    "")
GROQ_BASE_URL   = "https://api.groq.com/openai/v1"

# Groq model chain — tried in order.
# VERIFIED live against /v1/models on this key (2026-08-24). All llama-3.x
# chat models are decommissioned on Groq — do not use them.
GROQ_MODELS = [
    "openai/gpt-oss-120b",   # primary — most capable live model on this key
    "qwen/qwen3.6-27b",      # secondary — separate quota bucket
    "openai/gpt-oss-20b",    # fast fallback
]
GROQ_FAST_MODEL = "openai/gpt-oss-20b"   # used for titles/JSON — cheap & fast

NVIDIA_EMBED_KEY   = os.getenv("NVIDIA_EMBED_KEY", "")
NVIDIA_EMBED_MODEL = "nvidia/nv-embedqa-e5-v5"
NVIDIA_EMBED_BASE  = "https://integrate.api.nvidia.com/v1"

# ── Token budget ───────────────────────────────────────────────────────────────

# Rough 4-chars-per-token heuristic.  Keep system + context + history safely
# under the model's context window to avoid TPM overruns.
_MAX_CONTEXT_CHARS  = 8_000    # session context block
_MAX_HISTORY_CHARS  = 3_000    # recent conversation history
_MAX_RESPONSE_TOKENS = 1_500   # streaming completion budget

# ── Circuit-breaker state ──────────────────────────────────────────────────────

class _CircuitBreaker:
    """
    Simple half-open circuit breaker per provider.
    After `threshold` consecutive failures the provider is blocked for
    `cooldown_s` seconds before a single probe is allowed through.
    """

    def __init__(self, name: str, threshold: int = 3, cooldown_s: float = 60.0):
        self.name       = name
        self.threshold  = threshold
        self.cooldown_s = cooldown_s
        self._fails     = 0
        self._open_at   = 0.0   # epoch timestamp when circuit opened

    @property
    def is_open(self) -> bool:
        if self._fails < self.threshold:
            return False
        return time.monotonic() < self._open_at + self.cooldown_s

    def record_success(self) -> None:
        self._fails = 0

    def record_failure(self) -> None:
        self._fails += 1
        if self._fails >= self.threshold:
            self._open_at = time.monotonic()
            logger.warning(
                "CircuitBreaker[%s]: opened after %d failures — "
                "blocking for %.0f s",
                self.name, self._fails, self.cooldown_s,
            )


# One circuit-breaker per logical provider
_cb_groq   = _CircuitBreaker("groq",   threshold=3, cooldown_s=90.0)
_cb_nvidia = _CircuitBreaker("nvidia", threshold=2, cooldown_s=120.0)

# ── Lazy OpenAI clients ────────────────────────────────────────────────────────

_groq_client   = None
_nvidia_client = None
_embed_client  = None


def _get_groq():
    global _groq_client
    if _groq_client is None:
        from openai import AsyncOpenAI
        _groq_client = AsyncOpenAI(
            base_url=GROQ_BASE_URL,
            api_key=GROQ_API_KEY,
            timeout=25.0,
            max_retries=0,   # we handle retries ourselves
        )
    return _groq_client


def _get_nvidia():
    global _nvidia_client
    if _nvidia_client is None:
        from openai import AsyncOpenAI
        _nvidia_client = AsyncOpenAI(
            base_url=NVIDIA_BASE_URL,
            api_key=NVIDIA_API_KEY,
            timeout=55.0,
            max_retries=0,
        )
    return _nvidia_client


def _get_embed():
    global _embed_client
    if _embed_client is None:
        from openai import AsyncOpenAI
        _embed_client = AsyncOpenAI(
            base_url=NVIDIA_EMBED_BASE,
            api_key=NVIDIA_EMBED_KEY,
            timeout=10.0,
        )
    return _embed_client


# ── Retry-After helper ─────────────────────────────────────────────────────────

def _retry_after(exc: Exception) -> float:
    """
    Extract the Retry-After wait time (seconds) from a 429 error response.
    Returns 0 if the header is absent or the error is not a rate-limit.
    """
    try:
        # openai-python wraps the HTTP response in exc.response
        resp = getattr(exc, "response", None)
        if resp is None:
            return 0.0
        status = getattr(resp, "status_code", 0)
        if status != 429:
            return 0.0
        headers = getattr(resp, "headers", {})
        ra = headers.get("retry-after") or headers.get("Retry-After") or "0"
        return min(float(ra), 60.0)   # cap at 60 s
    except Exception:
        return 0.0


def _is_rate_limit(exc: Exception) -> bool:
    try:
        status = getattr(getattr(exc, "response", None), "status_code", 0)
        return status == 429
    except Exception:
        return False


# ── Token-budget helpers ───────────────────────────────────────────────────────

def _trim(text: str, max_chars: int) -> str:
    """Trim *text* to at most *max_chars*, appending an ellipsis marker."""
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "\n\n[...context trimmed to fit token budget...]"


def _trim_history(history: List[Dict[str, Any]], max_chars: int) -> List[Dict[str, Any]]:
    """
    Keep as many *recent* messages as fit within *max_chars* total.
    Always preserves the last user message.
    """
    if not history:
        return history
    total = 0
    kept: List[Dict[str, Any]] = []
    for msg in reversed(history):
        chunk = len(msg.get("content", ""))
        if total + chunk > max_chars and kept:
            break
        kept.append(msg)
        total += chunk
    return list(reversed(kept))


# ── Core streaming with retry ──────────────────────────────────────────────────

async def _stream_groq(
    messages: List[Dict[str, Any]],
    temperature: float,
    max_tokens: int,
    model: str,
) -> AsyncGenerator[str, None]:
    """
    Single Groq model attempt with up to 2 retries on 429.
    Raises on non-429 errors so the caller can try the next model.
    """
    client = _get_groq()
    for attempt in range(3):
        try:
            stream = await client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True,
            )
            got_any = False
            async for chunk in stream:
                choices = getattr(chunk, "choices", None)
                if not choices:
                    continue
                delta = getattr(choices[0].delta, "content", None)
                if delta:
                    got_any = True
                    yield delta
            if got_any:
                return
            # Empty stream — treat as soft failure
            logger.warning("LLMProvider: Groq[%s] returned empty stream", model)
            return
        except Exception as exc:
            if _is_rate_limit(exc):
                wait = _retry_after(exc) or (2 ** attempt * 3)
                logger.warning(
                    "LLMProvider: Groq[%s] rate-limited (429), waiting %.1f s "
                    "(attempt %d/3)",
                    model, wait, attempt + 1,
                )
                await asyncio.sleep(wait)
                continue
            raise   # non-rate-limit error bubbles up


async def _stream_nvidia(
    messages: List[Dict[str, Any]],
    temperature: float,
    max_tokens: int,
    use_reasoning: bool = False,
) -> AsyncGenerator[str, None]:
    """NVIDIA DeepSeek with up to 2 retries on 429."""
    client = _get_nvidia()
    extra: Dict[str, Any] = {}
    if use_reasoning:
        extra["extra_body"] = {
            "chat_template_kwargs": {"thinking": True, "reasoning_effort": "low"}
        }
    for attempt in range(3):
        try:
            stream = await client.chat.completions.create(
                model=NVIDIA_MODEL,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True,
                **extra,
            )
            async for chunk in stream:
                choices = getattr(chunk, "choices", None)
                if not choices:
                    continue
                delta = getattr(choices[0].delta, "content", None)
                if delta:
                    yield delta
            return
        except Exception as exc:
            if _is_rate_limit(exc):
                wait = _retry_after(exc) or (2 ** attempt * 5)
                logger.warning(
                    "LLMProvider: NVIDIA rate-limited (429), waiting %.1f s "
                    "(attempt %d/3)",
                    wait, attempt + 1,
                )
                await asyncio.sleep(wait)
                continue
            raise


# ── Public API ─────────────────────────────────────────────────────────────────

async def stream_chat(
    messages: List[Dict[str, Any]],
    temperature: float = 0.5,
    max_tokens: int = _MAX_RESPONSE_TOKENS,
    use_reasoning: bool = False,
) -> AsyncGenerator[str, None]:
    """
    Streams text deltas.  Full provider cascade:
      Groq[llama-3.3-70b] → Groq[llama-3.1-70b] → Groq[llama-3.1-8b-instant]
        → NVIDIA[deepseek-v4-flash]

    Each step only runs if the previous step failed (exception) or the
    circuit-breaker for that provider is open.
    """
    # ── Enforce token budget ───────────────────────────────────────────────
    budget_messages = _apply_token_budget(messages)

    # ── Try Groq model cascade ─────────────────────────────────────────────
    if not _cb_groq.is_open:
        for model in GROQ_MODELS:
            try:
                got_any = False
                async for token in _stream_groq(budget_messages, temperature, max_tokens, model):
                    got_any = True
                    yield token
                if got_any:
                    _cb_groq.record_success()
                    return
            except Exception as exc:
                logger.warning(
                    "LLMProvider: Groq[%s] failed (%s: %s) — trying next",
                    model, type(exc).__name__, exc,
                )
                _cb_groq.record_failure()
    else:
        logger.warning("LLMProvider: Groq circuit is OPEN — skipping to NVIDIA")

    # ── NVIDIA fallback ────────────────────────────────────────────────────
    if not _cb_nvidia.is_open:
        try:
            got_any = False
            async for token in _stream_nvidia(
                budget_messages, temperature, max_tokens, use_reasoning
            ):
                got_any = True
                yield token
            if got_any:
                _cb_nvidia.record_success()
                return
        except Exception as exc:
            logger.error(
                "LLMProvider: NVIDIA failed (%s: %s)",
                type(exc).__name__, exc,
            )
            _cb_nvidia.record_failure()
    else:
        logger.warning("LLMProvider: NVIDIA circuit is OPEN — all providers exhausted")

    # ── All providers failed ───────────────────────────────────────────────
    yield (
        "I'm temporarily unable to reach the AI service — all providers are "
        "either rate-limited or unavailable. Please wait a minute and try again."
    )


async def complete_json(
    messages: List[Dict[str, Any]],
    temperature: float = 0.1,
    max_tokens: int = 512,
) -> str:
    """Non-streaming completion via Groq's fastest model (for titles/JSON)."""
    try:
        client = _get_groq()
        for attempt in range(3):
            try:
                res = await client.chat.completions.create(
                    model=GROQ_FAST_MODEL,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    stream=False,
                )
                return res.choices[0].message.content or ""
            except Exception as exc:
                if _is_rate_limit(exc) and attempt < 2:
                    wait = _retry_after(exc) or (2 ** attempt * 2)
                    await asyncio.sleep(wait)
                    continue
                raise
    except Exception as exc:
        logger.error("LLMProvider: complete_json failed: %s", exc)
        return ""


async def generate_thread_title(first_user_message: str, candidate_name: str) -> str:
    """Generate a short 3-5 word chat thread title."""
    prompt = (
        f"Generate a 3-5 word title for a DMIT counselling conversation. "
        f"First message: \"{first_user_message[:100]}\". "
        f"Return ONLY the title, no quotes or trailing punctuation."
    )
    try:
        result = await complete_json(
            [{"role": "user", "content": prompt}],
            temperature=0.3, max_tokens=20,
        )
        title = result.strip().strip('"\'').rstrip('.').strip()
        return title if 3 < len(title) < 80 else first_user_message[:40]
    except Exception:
        return first_user_message[:40]


# ── Embeddings ─────────────────────────────────────────────────────────────────

async def embed_text(text: str) -> Optional[List[float]]:
    """Embed text using NVIDIA NeMo for vector search."""
    try:
        client = _get_embed()
        res = await client.embeddings.create(
            model=NVIDIA_EMBED_MODEL, input=text, encoding_format="float",
        )
        return res.data[0].embedding
    except Exception as exc:
        logger.warning("LLMProvider: embedding failed: %s", exc)
        return None


# ── DuckDuckGo search ──────────────────────────────────────────────────────────

async def duckduckgo_search(query: str, max_results: int = 4) -> str:
    """Real-time web search for current events/data."""
    try:
        from duckduckgo_search import DDGS

        def _sync():
            with DDGS() as ddgs:
                return list(ddgs.text(query, max_results=max_results))

        results = await asyncio.to_thread(_sync)
        if not results:
            return "No results found."
        lines = [
            f"**{r.get('title', '')}**\n{r.get('body', '')}\n{r.get('href', '')}"
            for r in results
        ]
        return "\n\n".join(lines)
    except ImportError:
        return "[Search unavailable: install duckduckgo-search]"
    except Exception as exc:
        logger.warning("DuckDuckGo search failed: %s", exc)
        return f"[Search failed: {exc}]"


# ── Internal: token-budget enforcement ────────────────────────────────────────

def _apply_token_budget(messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Walk the message list and trim large content blocks so the total
    prompt stays within a safe token budget.

    Heuristic: system message = session context (trim to _MAX_CONTEXT_CHARS).
    User/assistant history = trim oldest messages first.
    """
    if not messages:
        return messages

    result = []
    history_budget = _MAX_HISTORY_CHARS

    for i, msg in enumerate(messages):
        role    = msg.get("role", "")
        content = msg.get("content", "") or ""

        if role == "system":
            # The system prompt carries the full DMIT session context.
            # Trim it but keep the first part (most important facts).
            result.append({"role": "system", "content": _trim(content, _MAX_CONTEXT_CHARS)})
        elif role in ("user", "assistant"):
            if len(content) > history_budget and i < len(messages) - 2:
                # Collapse old messages that are too long into a summary placeholder
                result.append({
                    "role": role,
                    "content": content[: max(100, history_budget // 4)] + " [...]",
                })
            else:
                result.append({"role": role, "content": content})
            history_budget = max(0, history_budget - len(content))

    return result
