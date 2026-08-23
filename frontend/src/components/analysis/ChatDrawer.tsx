"use client";

import { useState, useRef, useEffect, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  X, Send, Loader2, Sparkles, AlertCircle, Trash2,
} from "lucide-react";
import {
  RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis,
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer,
  PieChart, Pie, Cell,
} from "recharts";
import { cn } from "@/lib/utils";
import { GOLD, chartTooltipStyle, chartCursorStyle } from "@/lib/analysis-theme";
import { apiBase } from "@/lib/api";
import { useAuthStore } from "@/store/authStore";

// ── Types ──────────────────────────────────────────────────────────────────────

type ChunkType = "status" | "text" | "chart" | "widget" | "table" | "suggestions" | "done";

interface StreamChunk {
  chunk_type: ChunkType;
  response?: string;
  stream_completed?: boolean;
  chart?: ChartSpec;
  widget?: WidgetSpec;
  table?: TableSpec;
  status?: string;
  status_message?: string;
  suggested_questions?: string[];
  section_ref?: string;
}

interface ChartSpec {
  chart_type: "radar" | "bar" | "doughnut" | "pie" | "line";
  title: string;
  labels: string[];
  datasets: Array<{ label: string; data: (number | null)[]; color?: string; colors?: string[] }>;
  horizontal?: boolean;
  x_label?: string;
  y_label?: string;
}

interface WidgetSpec {
  widget_type: string;
  title: string;
  [key: string]: unknown;
}

interface TableSpec {
  title: string;
  columns: string[];
  rows: string[][];
  column_types?: string[];
}

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  charts?: ChartSpec[];
  widgets?: WidgetSpec[];
  suggestions?: string[];
  isStreaming?: boolean;
  error?: boolean;
}

interface ChatHistory {
  thread_id: string;
  messages: Array<{ id: string; role: string; content: string; chart_specs?: ChartSpec[]; widget_specs?: WidgetSpec[]; created_at: string }>;
}

// ── Color palette ──────────────────────────────────────────────────────────────

const CHART_COLORS = [
  "#c4a574", "#9d8bb5", "#6b9e8f", "#b87d5c",
  "#8b9eb7", "#e8dcc8", "#f59e0b", "#4ade80",
  "#60a5fa", "#f87171",
];

// ── Status badge ───────────────────────────────────────────────────────────────

function StatusBadge({ status, message }: { status: string; message: string }) {
  const icons: Record<string, string> = {
    routing: "⟳",
    thinking: "◎",
    tool_call: "⚙",
    tool_done: "✓",
    generating: "✦",
    searching: "⌕",
    error: "⚠",
  };
  const colors: Record<string, string> = {
    routing:    "text-white/40",
    thinking:   "text-[#c4a574]/70",
    tool_call:  "text-[#9d8bb5]/80",
    tool_done:  "text-[#6b9e8f]/80",
    generating: "text-[#c4a574]/80",
    searching:  "text-[#8b9eb7]/70",
    error:      "text-rose-400",
  };
  return (
    <motion.div
      initial={{ opacity: 0, y: 4 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -4 }}
      className={cn(
        "flex items-center gap-1.5 text-[10px] font-mono px-2 py-1 rounded-md w-fit",
        "border border-white/[0.06]",
        colors[status] || "text-white/30"
      )}
      style={{ background: "rgba(255,255,255,0.02)" }}
    >
      <span className={cn("text-[9px]", status === "tool_call" && "animate-spin", status === "thinking" && "animate-pulse")}>
        {icons[status] || "◉"}
      </span>
      {message}
    </motion.div>
  );
}

// ── Chart renderer ─────────────────────────────────────────────────────────────

function InlineChart({ spec }: { spec: ChartSpec }) {
  const { chart_type, title, labels, datasets } = spec;
  const primaryColor = datasets[0]?.color || GOLD.primary;
  const colors = datasets[0]?.colors || CHART_COLORS;

  return (
    <div className="rounded-xl overflow-hidden mt-2 mb-1"
      style={{ background: "rgba(196,165,116,0.04)", border: `1px solid ${GOLD.border}` }}>
      <div className="px-3 pt-2.5 pb-0">
        <p className="text-[10px] font-mono uppercase tracking-widest text-white/35">{title}</p>
      </div>
      <div className="px-2 pb-2">
        {(chart_type === "radar") && (
          <ResponsiveContainer width="100%" height={200}>
            <RadarChart data={labels.map((label, i) => ({
              subject: label,
              value: datasets[0]?.data[i] ?? 0,
            }))}>
              <PolarGrid stroke="rgba(255,255,255,0.07)" />
              <PolarAngleAxis
                dataKey="subject"
                tick={{ fill: "rgba(255,255,255,0.45)", fontSize: 9 }}
              />
              <PolarRadiusAxis domain={[0, 100]} tick={false} axisLine={false} />
              <Radar
                dataKey="value"
                stroke={primaryColor}
                fill={primaryColor}
                fillOpacity={0.18}
                strokeWidth={1.5}
              />
              <Tooltip
                {...chartTooltipStyle}
                formatter={(v: unknown) => [`${Number(v).toFixed(0)}%`, datasets[0]?.label || ""]}
              />
            </RadarChart>
          </ResponsiveContainer>
        )}
        {(chart_type === "bar") && (
          <ResponsiveContainer width="100%" height={Math.max(120, labels.length * 22)}>
            <BarChart
              data={labels.map((label, i) => ({ name: label, value: datasets[0]?.data[i] ?? 0 }))}
              layout={spec.horizontal ? "vertical" : "horizontal"}
              margin={{ top: 4, right: 12, left: spec.horizontal ? 80 : 0, bottom: 4 }}
            >
              {spec.horizontal ? (
                <>
                  <XAxis type="number" domain={[0, 100]} tick={{ fill: "rgba(255,255,255,0.3)", fontSize: 9 }} />
                  <YAxis type="category" dataKey="name" tick={{ fill: "rgba(255,255,255,0.5)", fontSize: 9 }} width={75} />
                </>
              ) : (
                <>
                  <XAxis dataKey="name" tick={{ fill: "rgba(255,255,255,0.4)", fontSize: 9 }} />
                  <YAxis domain={[0, 100]} tick={{ fill: "rgba(255,255,255,0.3)", fontSize: 9 }} />
                </>
              )}
              <Tooltip {...chartTooltipStyle} cursor={chartCursorStyle} formatter={(v: unknown) => [`${Number(v).toFixed(0)}%`]} />
              <Bar dataKey="value" fill={primaryColor} radius={[3, 3, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        )}
        {(chart_type === "doughnut" || chart_type === "pie") && (
          <ResponsiveContainer width="100%" height={160}>
            <PieChart>
              <Pie
                data={labels.map((label, i) => ({ name: label, value: datasets[0]?.data[i] ?? 0 }))}
                cx="50%" cy="50%"
                innerRadius={chart_type === "doughnut" ? 40 : 0}
                outerRadius={65}
                paddingAngle={2}
                dataKey="value"
              >
                {labels.map((_, i) => (
                  <Cell key={i} fill={colors[i % colors.length]} />
                ))}
              </Pie>
              <Tooltip {...chartTooltipStyle} formatter={(v: unknown) => [`${Number(v).toFixed(0)}%`]} />
            </PieChart>
          </ResponsiveContainer>
        )}
      </div>
    </div>
  );
}

// ── Widget renderers ───────────────────────────────────────────────────────────

function ScoreGrid({ spec }: { spec: WidgetSpec }) {
  const items = (spec.items as Array<{ key: string; label: string; value: number; color: string; tier: string; icon?: string }>) || [];
  const cols = (spec.columns as number) || 4;
  return (
    <div className="rounded-xl overflow-hidden mt-2"
      style={{ background: "rgba(196,165,116,0.04)", border: `1px solid ${GOLD.border}` }}>
      <p className="text-[10px] font-mono uppercase tracking-widest text-white/35 px-3 pt-2.5 pb-1.5">{spec.title as string}</p>
      <div className={cn("grid gap-1.5 px-2 pb-2", cols === 5 ? "grid-cols-5" : "grid-cols-4")}>
        {items.map((item) => (
          <div key={item.key} className="rounded-lg p-2 text-center"
            style={{ background: `${item.color}12`, border: `1px solid ${item.color}30` }}>
            <p className="text-lg font-bold leading-none" style={{ color: item.color }}>
              {item.value.toFixed(0)}%
            </p>
            <p className="text-[8px] text-white/40 mt-0.5 leading-tight">{item.label}</p>
            <p className="text-[7px] mt-0.5" style={{ color: `${item.color}80` }}>{item.tier}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

function CareerCards({ spec }: { spec: WidgetSpec }) {
  const items = (spec.items as Array<{ rank: number; title: string; family: string; suitability_pct: number; key_strengths: string[]; color: string }>) || [];
  return (
    <div className="rounded-xl overflow-hidden mt-2"
      style={{ background: "rgba(196,165,116,0.04)", border: `1px solid ${GOLD.border}` }}>
      <p className="text-[10px] font-mono uppercase tracking-widest text-white/35 px-3 pt-2.5 pb-1.5">{spec.title as string}</p>
      <div className="px-2 pb-2 space-y-1.5">
        {items.map((c) => (
          <div key={c.rank} className="flex items-center gap-2.5 rounded-lg px-2.5 py-2"
            style={{ background: `${c.color}10`, border: `1px solid ${c.color}25` }}>
            <div className="w-6 h-6 rounded-full flex items-center justify-center text-[10px] font-bold flex-shrink-0"
              style={{ background: c.color, color: "#0a0a12" }}>
              {c.rank}
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-xs font-medium text-white/80 truncate">{c.title}</p>
              <div className="flex items-center gap-1.5 mt-0.5">
                <span className="text-[9px] font-mono px-1 py-0.5 rounded"
                  style={{ background: `${c.color}20`, color: c.color }}>{c.family}</span>
                {c.key_strengths.slice(0, 2).map((s, i) => (
                  <span key={i} className="text-[8px] text-white/30">{s}</span>
                ))}
              </div>
            </div>
            <div className="text-sm font-bold flex-shrink-0" style={{ color: c.color }}>
              {c.suitability_pct.toFixed(0)}%
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

function SwotMatrix({ spec }: { spec: WidgetSpec }) {
  const quadrants = [
    { key: "strengths", label: "S", title: "Strengths", color: "#6b9e8f" },
    { key: "weaknesses", label: "W", title: "Weaknesses", color: "#b87d5c" },
    { key: "opportunities", label: "O", title: "Opportunities", color: "#c4a574" },
    { key: "threats", label: "T", title: "Threats", color: "#9d8bb5" },
  ];
  return (
    <div className="rounded-xl overflow-hidden mt-2"
      style={{ background: "rgba(196,165,116,0.04)", border: `1px solid ${GOLD.border}` }}>
      <p className="text-[10px] font-mono uppercase tracking-widest text-white/35 px-3 pt-2.5 pb-1.5">SWOT Analysis</p>
      <div className="grid grid-cols-2 gap-1 px-2 pb-2">
        {quadrants.map(({ key, label, title, color }) => {
          const items = (spec[key] as string[]) || [];
          return (
            <div key={key} className="rounded-lg p-2"
              style={{ background: `${color}0d`, border: `1px solid ${color}25` }}>
              <div className="flex items-center gap-1.5 mb-1.5">
                <span className="w-5 h-5 rounded-md text-[10px] font-bold flex items-center justify-center"
                  style={{ background: color, color: "#0a0a12" }}>{label}</span>
                <span className="text-[9px] font-medium" style={{ color }}>{title}</span>
              </div>
              <ul className="space-y-0.5">
                {items.slice(0, 3).map((item, i) => (
                  <li key={i} className="text-[9px] text-white/55 leading-snug">• {item}</li>
                ))}
              </ul>
            </div>
          );
        })}
      </div>
    </div>
  );
}

function MILadder({ spec }: { spec: WidgetSpec }) {
  const items = (spec.items as Array<{ rank: number; intelligence: string; value: number; tier: string; color: string }>) || [];
  return (
    <div className="rounded-xl overflow-hidden mt-2"
      style={{ background: "rgba(196,165,116,0.04)", border: `1px solid ${GOLD.border}` }}>
      <p className="text-[10px] font-mono uppercase tracking-widest text-white/35 px-3 pt-2.5 pb-1.5">{spec.title as string}</p>
      <div className="px-2 pb-2 space-y-1">
        {items.map((item) => (
          <div key={item.rank} className="flex items-center gap-2">
            <span className="text-[9px] font-mono w-4 text-right text-white/25">{item.rank}</span>
            <div className="flex-1 flex items-center gap-1.5">
              <div className="flex-1 h-1.5 rounded-full overflow-hidden bg-white/[0.05]">
                <motion.div
                  className="h-full rounded-full"
                  style={{ background: item.color }}
                  initial={{ width: 0 }}
                  animate={{ width: `${item.value}%` }}
                  transition={{ duration: 0.6, delay: item.rank * 0.05 }}
                />
              </div>
            </div>
            <span className="text-[9px] text-white/50 w-20 truncate">{item.intelligence}</span>
            <span className="text-[9px] font-mono w-8 text-right" style={{ color: item.color }}>{item.value.toFixed(0)}%</span>
          </div>
        ))}
      </div>
    </div>
  );
}

function BrainSummary({ spec }: { spec: WidgetSpec }) {
  const lh = (spec.left_pct as number) || 0;
  const rh = (spec.right_pct as number) || 0;
  const leftTraits  = (spec.left_traits  as string[]) || [];
  const rightTraits = (spec.right_traits as string[]) || [];
  return (
    <div className="rounded-xl overflow-hidden mt-2"
      style={{ background: "rgba(196,165,116,0.04)", border: `1px solid ${GOLD.border}` }}>
      <p className="text-[10px] font-mono uppercase tracking-widest text-white/35 px-3 pt-2.5 pb-1.5">{spec.title as string}</p>
      <div className="grid grid-cols-2 gap-1.5 px-2 pb-2">
        {[
          { side: "Left", pct: lh, color: "#9d8bb5", traits: leftTraits },
          { side: "Right", pct: rh, color: "#c4a574", traits: rightTraits },
        ].map(({ side, pct, color, traits }) => (
          <div key={side} className="rounded-lg p-2.5"
            style={{ background: `${color}0d`, border: `1px solid ${color}25` }}>
            <div className="flex justify-between items-center mb-1.5">
              <span className="text-[10px] font-medium" style={{ color }}>{side} Brain</span>
              <span className="text-sm font-bold" style={{ color }}>{pct.toFixed(0)}%</span>
            </div>
            <ul className="space-y-0.5">
              {traits.slice(0, 3).map((t, i) => (
                <li key={i} className="text-[9px] text-white/45">• {t}</li>
              ))}
            </ul>
          </div>
        ))}
      </div>
      {!!spec.balance_label && (
        <p className="text-[9px] text-white/30 px-3 pb-2 text-center">{String(spec.balance_label)}</p>
      )}
    </div>
  );
}

function GenericWidget({ spec }: { spec: WidgetSpec }) {
  return (
    <div className="rounded-xl p-3 mt-2"
      style={{ background: "rgba(196,165,116,0.04)", border: `1px solid ${GOLD.border}` }}>
      <p className="text-[10px] font-mono uppercase tracking-widest text-white/35 mb-1">{spec.title as string}</p>
      <pre className="text-[9px] text-white/40 whitespace-pre-wrap overflow-auto max-h-40">
        {JSON.stringify(spec, null, 2)}
      </pre>
    </div>
  );
}

function WidgetRenderer({ spec }: { spec: WidgetSpec }) {
  const components: Record<string, React.ComponentType<{ spec: WidgetSpec }>> = {
    score_grid:         ScoreGrid,
    career_cards:       CareerCards,
    swot_matrix:        SwotMatrix,
    mi_strength_ladder: MILadder,
    brain_summary:      BrainSummary,
  };
  const Comp = components[spec.widget_type] || GenericWidget;
  return <Comp spec={spec} />;
}

// ── Markdown-like text renderer ────────────────────────────────────────────────

function MessageText({ content }: { content: string }) {
  return (
    <div
      className="text-sm text-white/80 leading-relaxed prose-dmit"
      style={{ fontFamily: "inherit" }}
      dangerouslySetInnerHTML={{
        __html: content
          .replace(/\*\*(.+?)\*\*/g, '<strong class="text-white/95 font-semibold">$1</strong>')
          .replace(/\*(.+?)\*/g, '<em class="text-white/70">$1</em>')
          .replace(/^#{1,3} (.+)$/gm, '<p class="text-white/90 font-semibold text-[13px] mt-2 mb-1">$1</p>')
          .replace(/^[-•] (.+)$/gm, '<div class="flex gap-1.5 my-0.5"><span class="text-[#c4a574] flex-shrink-0">•</span><span>$1</span></div>')
          .replace(/\n\n/g, '<br/><br/>')
          .replace(/\n/g, '<br/>'),
      }}
    />
  );
}

// ── Suggestion chips ───────────────────────────────────────────────────────────

function SuggestionChips({ chips, onSelect }: { chips: string[]; onSelect: (q: string) => void }) {
  return (
    <div className="flex flex-wrap gap-1.5 mt-3">
      {chips.map((chip, i) => (
        <motion.button
          key={i}
          initial={{ opacity: 0, y: 6 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: i * 0.06 }}
          onClick={() => onSelect(chip)}
          className="text-[10px] px-2.5 py-1.5 rounded-lg text-white/55 hover:text-[#c4a574] transition-colors border border-white/[0.06] hover:border-[#c4a574]/30"
          style={{ background: "rgba(255,255,255,0.02)" }}
        >
          {chip}
        </motion.button>
      ))}
    </div>
  );
}

// ── Main ChatDrawer ────────────────────────────────────────────────────────────

interface ChatDrawerProps {
  sessionId: string;
  candidateName?: string;
  isOpen: boolean;
  onClose: () => void;
}

export function ChatDrawer({ sessionId, candidateName, isOpen, onClose }: ChatDrawerProps) {
  const accessToken = useAuthStore((s) => s.accessToken);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput]     = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [threadId, setThreadId]   = useState<string | null>(null);
  const [currentStatus, setCurrentStatus] = useState<{ status: string; msg: string } | null>(null);
  const [historyLoaded, setHistoryLoaded] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const textareaRef    = useRef<HTMLTextAreaElement>(null);
  const abortRef       = useRef<AbortController | null>(null);

  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, []);

  useEffect(() => { scrollToBottom(); }, [messages, scrollToBottom]);

  // ── Load history ─────────────────────────────────────────────────────────
  useEffect(() => {
    if (!isOpen || historyLoaded || !accessToken) return;
    const load = async () => {
      try {
        const res = await fetch(`${apiBase()}/sessions/${sessionId}/chat/history`, {
          headers: { Authorization: `Bearer ${accessToken}` },
        });
        if (!res.ok) return;
        const data: ChatHistory = await res.json();
        setThreadId(data.thread_id);
        const loaded: Message[] = data.messages.map((m) => ({
          id: m.id,
          role: m.role as "user" | "assistant",
          content: m.content,
          charts:  m.chart_specs  || [],
          widgets: m.widget_specs || [],
        }));
        setMessages(loaded);
        setHistoryLoaded(true);
      } catch {
        setHistoryLoaded(true);
      }
    };
    load();
  }, [isOpen, historyLoaded, sessionId, accessToken]);

  // ── Send message ──────────────────────────────────────────────────────────
  const sendMessage = useCallback(async (text: string) => {
    if (!text.trim() || isLoading) return;
    setError(null);
    const userMsg: Message = {
      id: `u-${Date.now()}`,
      role: "user",
      content: text,
    };
    const assistantMsgId = `a-${Date.now()}`;
    const assistantMsg: Message = {
      id: assistantMsgId,
      role: "assistant",
      content: "",
      charts: [],
      widgets: [],
      isStreaming: true,
    };

    setMessages((prev) => [...prev, userMsg, assistantMsg]);
    setInput("");
    setIsLoading(true);
    setCurrentStatus({ status: "routing", msg: "Getting started..." });

    abortRef.current = new AbortController();

    try {
      const res = await fetch(`${apiBase()}/sessions/${sessionId}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${accessToken}`,
        },
        body: JSON.stringify({ message: text, thread_id: threadId }),
        signal: abortRef.current.signal,
      });

      if (!res.ok) {
        const errText = await res.text();
        throw new Error(errText || `HTTP ${res.status}`);
      }

      // Get thread ID from header
      const newThreadId = res.headers.get("X-Thread-Id");
      if (newThreadId) setThreadId(newThreadId);

      // Read NDJSON stream
      const reader = res.body?.getReader();
      const decoder = new TextDecoder();
      if (!reader) throw new Error("No response body");

      let buffer = "";
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split("\n");
        buffer = lines.pop() || "";

        for (const line of lines) {
          const trimmed = line.trim();
          if (!trimmed) continue;
          try {
            const chunk: StreamChunk = JSON.parse(trimmed);
            processChunk(chunk, assistantMsgId);
          } catch {
            // skip malformed
          }
        }
      }
    } catch (e: unknown) {
      if ((e as Error).name === "AbortError") return;
      const msg = e instanceof Error ? e.message : "Connection failed";
      setError(msg);
      setMessages((prev) =>
        prev.map((m) =>
          m.id === assistantMsgId
            ? { ...m, content: "Sorry, something went wrong. Please try again.", isStreaming: false, error: true }
            : m
        )
      );
    } finally {
      setIsLoading(false);
      setCurrentStatus(null);
    }
  }, [isLoading, sessionId, accessToken, threadId]);

  const processChunk = useCallback((chunk: StreamChunk, assistantMsgId: string) => {
    switch (chunk.chunk_type) {
      case "status":
        if (chunk.status && chunk.status_message) {
          setCurrentStatus({ status: chunk.status, msg: chunk.status_message });
        }
        break;
      case "text":
        setMessages((prev) =>
          prev.map((m) =>
            m.id === assistantMsgId
              ? { ...m, content: m.content + (chunk.response || "") }
              : m
          )
        );
        break;
      case "chart":
        if (chunk.chart) {
          setMessages((prev) =>
            prev.map((m) =>
              m.id === assistantMsgId
                ? { ...m, charts: [...(m.charts || []), chunk.chart!] }
                : m
            )
          );
        }
        break;
      case "widget":
        if (chunk.widget) {
          setMessages((prev) =>
            prev.map((m) =>
              m.id === assistantMsgId
                ? { ...m, widgets: [...(m.widgets || []), chunk.widget!] }
                : m
            )
          );
        }
        break;
      case "suggestions":
        if (chunk.suggested_questions?.length) {
          setMessages((prev) =>
            prev.map((m) =>
              m.id === assistantMsgId
                ? { ...m, suggestions: chunk.suggested_questions }
                : m
            )
          );
        }
        break;
      case "done":
        setMessages((prev) =>
          prev.map((m) =>
            m.id === assistantMsgId ? { ...m, isStreaming: false } : m
          )
        );
        setCurrentStatus(null);
        break;
    }
  }, []);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage(input);
    }
  };

  const clearChat = useCallback(async () => {
    if (!accessToken) return;
    try {
      await fetch(`${apiBase()}/sessions/${sessionId}/chat`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${accessToken}` },
      });
      setMessages([]);
      setThreadId(null);
      setHistoryLoaded(false);
    } catch { /* ignore */ }
  }, [sessionId, accessToken]);

  const initialSuggestions = [
    `What are ${candidateName ? candidateName + "'s" : "the"} top strengths?`,
    "Show the intelligence profile chart",
    "Which careers are the best fit?",
    "How should this person study?",
    "Explain the brain hemisphere results",
    "Show the personality analysis",
  ];

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Mobile backdrop */}
          <motion.div
            className="fixed inset-0 bg-black/40 z-[60] lg:hidden"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
          />

          {/* Drawer panel */}
          <motion.div
            className="fixed right-0 top-14 bottom-0 z-[65] flex flex-col w-full max-w-[420px]"
            style={{
              background: "rgba(4,4,15,0.97)",
              borderLeft: `1px solid ${GOLD.border}`,
              backdropFilter: "blur(20px)",
            }}
            initial={{ x: 420, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            exit={{ x: 420, opacity: 0 }}
            transition={{ duration: 0.35, ease: [0.16, 1, 0.3, 1] }}
          >
            {/* Header */}
            <div
              className="flex items-center justify-between px-4 py-3 flex-shrink-0"
              style={{ borderBottom: `1px solid ${GOLD.border}` }}
            >
              <div className="flex items-center gap-2.5">
                <div
                  className="w-7 h-7 rounded-lg flex items-center justify-center flex-shrink-0"
                  style={{ background: `${GOLD.primary}22`, border: `1px solid ${GOLD.border}` }}
                >
                  <Sparkles className="w-3.5 h-3.5" style={{ color: GOLD.primary }} />
                </div>
                <div>
                  <p className="text-sm font-medium text-white/85">DMIT Insight</p>
                  <p className="text-[9px] text-white/30 font-mono">AI Consultant · {candidateName || "Session"}</p>
                </div>
              </div>
              <div className="flex items-center gap-1">
                {messages.length > 0 && (
                  <button
                    onClick={clearChat}
                    className="w-7 h-7 rounded-lg flex items-center justify-center text-white/25 hover:text-rose-400 transition-colors"
                    title="Clear chat"
                  >
                    <Trash2 className="w-3.5 h-3.5" />
                  </button>
                )}
                <button
                  onClick={onClose}
                  className="w-7 h-7 rounded-lg flex items-center justify-center text-white/30 hover:text-white/70 transition-colors"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>
            </div>

            {/* Messages area */}
            <div className="flex-1 overflow-y-auto px-4 py-3 space-y-4 scroll-smooth">
              {/* Empty state */}
              {messages.length === 0 && (
                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="pt-4"
                >
                  <p className="text-xs text-white/35 mb-4 leading-relaxed">
                    Ask me anything about {candidateName ? <strong className="text-white/60">{candidateName}</strong> : "this analysis"}.
                    I can explain scores, suggest careers, show charts, and create a personalised development plan.
                  </p>
                  <div className="flex flex-wrap gap-1.5">
                    {initialSuggestions.map((s, i) => (
                      <motion.button
                        key={i}
                        initial={{ opacity: 0, y: 6 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: i * 0.05 }}
                        onClick={() => sendMessage(s)}
                        className="text-[10px] px-2.5 py-1.5 rounded-lg text-white/50 hover:text-[#c4a574] border border-white/[0.06] hover:border-[#c4a574]/30 transition-all"
                        style={{ background: "rgba(255,255,255,0.02)" }}
                      >
                        {s}
                      </motion.button>
                    ))}
                  </div>
                </motion.div>
              )}

              {/* Message list */}
              {messages.map((msg) => (
                <div
                  key={msg.id}
                  className={cn(
                    "flex",
                    msg.role === "user" ? "justify-end" : "justify-start"
                  )}
                >
                  <div
                    className={cn(
                      "max-w-[88%] rounded-2xl px-3.5 py-2.5",
                      msg.role === "user"
                        ? "rounded-br-sm"
                        : "rounded-bl-sm"
                    )}
                    style={
                      msg.role === "user"
                        ? { background: `${GOLD.primary}22`, border: `1px solid ${GOLD.border}` }
                        : { background: "rgba(255,255,255,0.03)", border: "1px solid rgba(255,255,255,0.06)" }
                    }
                  >
                    {msg.role === "user" ? (
                      <p className="text-sm text-white/85">{msg.content}</p>
                    ) : (
                      <>
                        {/* Status badge while streaming */}
                        {msg.isStreaming && currentStatus && (
                          <div className="mb-2">
                            <AnimatePresence mode="wait">
                              <StatusBadge
                                key={currentStatus.status + currentStatus.msg}
                                status={currentStatus.status}
                                message={currentStatus.msg}
                              />
                            </AnimatePresence>
                          </div>
                        )}

                        {/* Text content */}
                        {msg.content && <MessageText content={msg.content} />}

                        {/* Streaming cursor */}
                        {msg.isStreaming && msg.content && (
                          <span className="inline-block w-0.5 h-3.5 ml-0.5 rounded-full animate-pulse"
                            style={{ background: GOLD.primary, verticalAlign: "text-bottom" }} />
                        )}

                        {/* Empty streaming state */}
                        {msg.isStreaming && !msg.content && !currentStatus && (
                          <div className="flex items-center gap-1.5 py-0.5">
                            {[0, 1, 2].map((i) => (
                              <motion.div key={i} className="w-1.5 h-1.5 rounded-full"
                                style={{ background: GOLD.primary }}
                                animate={{ scale: [1, 1.3, 1], opacity: [0.4, 1, 0.4] }}
                                transition={{ duration: 0.8, repeat: Infinity, delay: i * 0.15 }}
                              />
                            ))}
                          </div>
                        )}

                        {/* Charts */}
                        {(msg.charts || []).map((chart, i) => (
                          <InlineChart key={i} spec={chart} />
                        ))}

                        {/* Widgets */}
                        {(msg.widgets || []).map((widget, i) => (
                          <WidgetRenderer key={i} spec={widget} />
                        ))}

                        {/* Suggestion chips */}
                        {!msg.isStreaming && msg.suggestions && msg.suggestions.length > 0 && (
                          <SuggestionChips
                            chips={msg.suggestions}
                            onSelect={sendMessage}
                          />
                        )}
                      </>
                    )}
                  </div>
                </div>
              ))}

              {/* Error message */}
              {error && (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="flex items-center gap-2 text-rose-400 text-xs p-2 rounded-lg"
                  style={{ background: "rgba(244,63,94,0.06)", border: "1px solid rgba(244,63,94,0.2)" }}
                >
                  <AlertCircle className="w-3.5 h-3.5 flex-shrink-0" />
                  {error}
                </motion.div>
              )}

              <div ref={messagesEndRef} />
            </div>

            {/* Input area */}
            <div
              className="px-3 py-3 flex-shrink-0"
              style={{ borderTop: `1px solid ${GOLD.border}` }}
            >
              <div
                className="flex items-end gap-2 rounded-xl p-2"
                style={{ background: "rgba(255,255,255,0.03)", border: "1px solid rgba(255,255,255,0.07)" }}
              >
                <textarea
                  ref={textareaRef}
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={handleKeyDown}
                  placeholder={`Ask about ${candidateName || "the analysis"}…`}
                  disabled={isLoading}
                  rows={1}
                  className="flex-1 bg-transparent resize-none text-sm text-white/80 placeholder:text-white/25 focus:outline-none leading-relaxed py-0.5 max-h-24 overflow-y-auto"
                  style={{ fontFamily: "inherit" }}
                />
                <motion.button
                  onClick={() => sendMessage(input)}
                  disabled={!input.trim() || isLoading}
                  whileTap={{ scale: 0.9 }}
                  className={cn(
                    "w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0 transition-all",
                    input.trim() && !isLoading
                      ? "opacity-100 cursor-pointer"
                      : "opacity-30 cursor-not-allowed"
                  )}
                  style={
                    input.trim() && !isLoading
                      ? { background: GOLD.gradient, color: "#0a0a12" }
                      : { background: "rgba(255,255,255,0.05)", color: "rgba(255,255,255,0.3)" }
                  }
                >
                  {isLoading ? (
                    <Loader2 className="w-3.5 h-3.5 animate-spin" />
                  ) : (
                    <Send className="w-3.5 h-3.5" />
                  )}
                </motion.button>
              </div>
              <p className="text-[8px] text-white/15 text-center mt-1.5">
                Shift+Enter for new line · AI responses are for educational purposes
              </p>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}
