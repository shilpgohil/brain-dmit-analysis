# Code Craft & Anti-AI Invariants — DMIT Platform

## 1. Non-Negotiable No-Comments Rule
Code must be 100% clean, expressive, and self-documenting.
- **ABSOLUTE BAN** on narrative, explanatory, or boilerplate comments in code.
- No `// Fetching user session...`, `// Calculating ridge count...`, `# Stage 1 loop...`.
- Code intent must be communicated entirely through descriptive naming, precise types, and idiomatic structure:
  - Good: `const isTentedArch = coresCount === 0 && deltasCount === 0 && apexAngle < 60;`
  - Bad: `// Check if tented arch` followed by obscure variable names.
- Allowed comments: Only mandatory third-party annotations (e.g. `/* eslint-disable */`, `# type: ignore`), scientific paper references (e.g. Table 1.1), or critical security warnings.

---

## 2. Anti-AI-Code Standards
Never generate code that looks like a shallow AI boilerplate template:
- **No Mock Placeholders**: Never leave mock data arrays, fake timeout simulations, or `// TODO: implement later` stubs in production routes.
- **No Monolithic Files**: Break complex analytical logic into modular, testable domain modules.
- **Strict Typing**: TypeScript `strict: true` with zero `any` or `unknown` escape hatches; Python Pydantic v2 models and type hints on every function signature.
- **Zero Swallowed Exceptions**: Never use bare `except: pass` or `catch (e) {}` that hides biometric calculation bugs or image parsing errors.
