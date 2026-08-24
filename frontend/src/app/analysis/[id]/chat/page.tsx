"use client";

import { useState, useRef, useEffect, useCallback, useMemo } from "react";
import { useParams, useRouter } from "next/navigation";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import Link from "next/link";
import { motion, AnimatePresence } from "framer-motion";
import {
  ArrowLeft, Plus, Send, Loader2, Sparkles,
  Trash2, MessageSquare, ChevronRight,
  AlertTriangle, X, ChevronDown,
} from "lucide-react";
import {
  RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis,
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend,
  PieChart, Pie, Cell, LineChart, Line, CartesianGrid, Area, AreaChart,
} from "recharts";
import { cn } from "@/lib/utils";
import { GOLD, chartTooltipStyle, chartCursorStyle } from "@/lib/analysis-theme";
import { apiBase } from "@/lib/api";
import { useAuthStore } from "@/store/authStore";
import { useAuthGuard } from "@/hooks/useAuthGuard";
import { getAnalysis } from "@/lib/api";
import type { AnalysisResult } from "@/lib/types";
import { FingerprintField } from "@/components/effects/FingerprintField";

// ── Types ──────────────────────────────────────────────────────────────────────

interface ChartSpec {
  chart_type: "radar" | "bar" | "doughnut" | "pie" | "line" | "area";
  title: string;
  labels: string[];
  datasets: Array<{ label: string; data: (number | null)[]; color?: string; colors?: string[] }>;
  horizontal?: boolean;
  x_label?: string;
  y_label?: string;
}

interface WidgetSpec { widget_type: string; title: string; [key: string]: unknown }

interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  charts?: ChartSpec[];
  widgets?: WidgetSpec[];
  suggestions?: string[];
  isStreaming?: boolean;
  error?: boolean;
  created_at?: string;
}

interface StatusEntry { status: string; msg: string; id: number }

const CHART_COLORS = ["#c4a574","#9d8bb5","#6b9e8f","#b87d5c","#8b9eb7","#e8dcc8","#f59e0b","#4ade80","#60a5fa","#f87171"];

const STARTER_SUGGESTIONS = [
  { label: "Top Strengths",        q: "What are the top strengths based on this analysis?" },
  { label: "Career Matches",       q: "Show the best-fit career matches as a chart" },
  { label: "Intelligence Profile", q: "Show the multiple intelligence radar chart and explain it" },
  { label: "Brain Architecture",   q: "Explain the brain hemisphere and lobe results" },
  { label: "Learning Style",       q: "How should this person study and learn best?" },
  { label: "10 Quotients",         q: "Show all 10 quotient scores as a visual chart" },
  { label: "SWOT Analysis",        q: "Show the SWOT analysis matrix" },
  { label: "Development Plan",     q: "Create a 30-day personalised development roadmap" },
  { label: "Personality",          q: "Show the personality radar and explain communication style" },
  { label: "Fingerprint Patterns", q: "Show the fingerprint pattern distribution and what each means" },
];

// ── Inline markdown renderer ────────────────────────────────────────────────

/** Full GFM-aware Markdown renderer styled for the dark gold theme. */
function Markdown({ children }: { children: string }) {
  return (
    <ReactMarkdown
      remarkPlugins={[remarkGfm]}
      components={{
        /* Paragraphs */
        p: ({ children }) => (
          <p className="mb-2 last:mb-0 text-[13px] leading-relaxed text-white/75">{children}</p>
        ),
        /* Headings */
        h1: ({ children }) => (
          <h1 className="text-[15px] font-semibold text-white/90 mt-4 mb-2 first:mt-0">{children}</h1>
        ),
        h2: ({ children }) => (
          <h2 className="text-[14px] font-semibold text-white/85 mt-3 mb-1.5">{children}</h2>
        ),
        h3: ({ children }) => (
          <h3 className="text-[13px] font-semibold text-white/80 mt-2.5 mb-1">{children}</h3>
        ),
        h4: ({ children }) => (
          <h4 className="text-[12px] font-medium text-white/75 mt-2 mb-1">{children}</h4>
        ),
        /* Emphasis */
        strong: ({ children }) => (
          <strong className="font-semibold text-white/95">{children}</strong>
        ),
        em: ({ children }) => (
          <em className="italic text-white/65">{children}</em>
        ),
        /* Bullet list */
        ul: ({ children }) => (
          <ul
            className="my-2 space-y-0.5 text-[13px] text-white/75"
            style={{ listStyleType: "disc", paddingLeft: "1.25rem" }}
          >
            {children}
          </ul>
        ),
        /* Numbered list */
        ol: ({ children }) => (
          <ol
            className="my-2 space-y-0.5 text-[13px] text-white/75"
            style={{ listStyleType: "decimal", paddingLeft: "1.25rem" }}
          >
            {children}
          </ol>
        ),
        /* List item */
        li: ({ children }) => (
          <li className="leading-relaxed marker:text-[#c4a574]">{children}</li>
        ),
        /* Blockquote */
        blockquote: ({ children }) => (
          <blockquote
            className="border-l-2 border-[#c4a574]/50 pl-3 my-2 text-white/55 italic text-[12px]"
            style={{ background: "rgba(196,165,116,0.05)", borderRadius: "0 6px 6px 0", padding: "6px 12px" }}
          >
            {children}
          </blockquote>
        ),
        /* Inline code */
        code: ({ children, className }) => {
          const isBlock = className?.includes("language-");
          if (isBlock) {
            return (
              <code
                className="block my-2 p-3 rounded-xl text-[11px] font-mono text-white/70 overflow-x-auto"
                style={{ background: "rgba(255,255,255,0.05)", border: "1px solid rgba(255,255,255,0.08)" }}
              >
                {children}
              </code>
            );
          }
          return (
            <code
              className="text-[11px] font-mono px-1.5 py-0.5 rounded-md text-[#c4a574]/90"
              style={{ background: "rgba(196,165,116,0.10)", border: "1px solid rgba(196,165,116,0.18)" }}
            >
              {children}
            </code>
          );
        },
        /* Fenced code block */
        pre: ({ children }) => (
          <pre
            className="my-2 p-3 rounded-xl text-[11px] font-mono text-white/70 overflow-x-auto"
            style={{ background: "rgba(255,255,255,0.04)", border: "1px solid rgba(255,255,255,0.07)" }}
          >
            {children}
          </pre>
        ),
        /* Horizontal rule */
        hr: () => (
          <hr className="my-3 border-none border-t" style={{ borderTop: "1px solid rgba(255,255,255,0.08)" }} />
        ),
        /* GFM table */
        table: ({ children }) => (
          <div className="my-3 overflow-x-auto rounded-xl" style={{ border: "1px solid rgba(196,165,116,0.2)" }}>
            <table className="w-full text-[12px] border-collapse">{children}</table>
          </div>
        ),
        thead: ({ children }) => (
          <thead style={{ background: "rgba(196,165,116,0.08)" }}>{children}</thead>
        ),
        tbody: ({ children }) => <tbody>{children}</tbody>,
        tr: ({ children }) => (
          <tr style={{ borderBottom: "1px solid rgba(255,255,255,0.05)" }}>{children}</tr>
        ),
        th: ({ children }) => (
          <th className="px-3 py-2 text-left font-semibold text-white/70 text-[11px] tracking-wide uppercase whitespace-nowrap">
            {children}
          </th>
        ),
        td: ({ children }) => (
          <td className="px-3 py-2 text-white/60 align-top leading-relaxed">{children}</td>
        ),
        /* Links */
        a: ({ href, children }) => (
          <a
            href={href}
            target="_blank"
            rel="noopener noreferrer"
            className="text-[#c4a574] underline underline-offset-2 decoration-[#c4a574]/40 hover:decoration-[#c4a574] transition-colors"
          >
            {children}
          </a>
        ),
        /* Strikethrough (GFM) */
        del: ({ children }) => (
          <del className="text-white/35 line-through">{children}</del>
        ),
      }}
    >
      {children}
    </ReactMarkdown>
  );
}

// ── Status shimmer pill ─────────────────────────────────────────────────────

function StatusPill({ entry }: { entry: StatusEntry }) {
  const isToolCall = entry.status === "tool_call";
  const isToolDone = entry.status === "tool_done";

  const borderColor = isToolDone
    ? "rgba(107,158,143,0.28)"
    : isToolCall
      ? "rgba(157,139,181,0.28)"
      : "rgba(196,165,116,0.2)";
  const bgColor = isToolDone
    ? "rgba(107,158,143,0.07)"
    : isToolCall
      ? "rgba(157,139,181,0.09)"
      : "rgba(196,165,116,0.06)";
  const textColor = isToolDone ? "#6b9e8f" : isToolCall ? "#9d8bb5" : "rgba(196,165,116,0.85)";

  return (
    <motion.div
      initial={{ opacity: 0, y: 4, filter: "blur(4px)" }}
      animate={{ opacity: 1, y: 0, filter: "blur(0px)" }}
      exit={{ opacity: 0, y: -4, filter: "blur(4px)" }}
      transition={{ duration: 0.18, ease: "easeOut" }}
      className="flex items-center gap-2.5 text-[11px] px-3.5 py-2 rounded-2xl w-fit mb-2 relative overflow-hidden"
      style={{ background: bgColor, border: `1px solid ${borderColor}` }}
    >
      {/* Shimmer — only on non-done statuses */}
      {!isToolDone && (
        <motion.div
          className="absolute inset-0 pointer-events-none"
          style={{
            background: "linear-gradient(90deg, transparent 0%, rgba(255,255,255,0.035) 50%, transparent 100%)",
            transform: "skewX(-20deg)",
          }}
          animate={{ x: ["-120%", "220%"] }}
          transition={{ duration: 1.5, repeat: Infinity, ease: "linear" }}
        />
      )}

      {/* Indicator */}
      <div className="flex-shrink-0">
        {isToolDone ? (
          <motion.div initial={{ scale: 0 }} animate={{ scale: 1 }}
            className="w-3 h-3 rounded-full flex items-center justify-center"
            style={{ background: "rgba(107,158,143,0.22)" }}>
            <svg className="w-2 h-2" viewBox="0 0 12 12" fill="none">
              <path d="M2 6l3 3 5-5" stroke="#6b9e8f" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </motion.div>
        ) : (
          <div className="relative w-3 h-3">
            <div className="absolute inset-0 rounded-full"
              style={{ border: "1.5px solid rgba(196,165,116,0.2)" }} />
            <motion.div
              className="absolute inset-0 rounded-full"
              style={{ borderTop: `1.5px solid ${textColor}`, borderRight: "1.5px solid transparent", borderBottom: "1.5px solid transparent", borderLeft: "1.5px solid transparent" }}
              animate={{ rotate: 360 }}
              transition={{ duration: 0.65, repeat: Infinity, ease: "linear" }}
            />
          </div>
        )}
      </div>

      <span className="relative font-mono leading-none" style={{ color: textColor }}>
        {entry.msg}
      </span>
    </motion.div>
  );
}
// ── Chart renderer ─────────────────────────────────────────────────────────────

function InlineChart({ spec }: { spec: ChartSpec }) {
  const { chart_type, title, labels, datasets } = spec;
  const primary = datasets[0]?.color || GOLD.primary;
  const colors  = datasets[0]?.colors || CHART_COLORS;
  const isHoriz = spec.horizontal;
  const h = Math.max(150, isHoriz ? labels.length * 24 + 30 : 180);

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.35 }}
      className="rounded-2xl overflow-hidden mt-3 mb-1"
      style={{ background: "rgba(196,165,116,0.03)", border: `1px solid ${GOLD.border}` }}
    >
      <div className="px-4 py-2.5 flex items-center gap-2"
        style={{ borderBottom: `1px solid ${GOLD.border}` }}>
        <Sparkles className="w-3 h-3 flex-shrink-0" style={{ color: GOLD.primary }} />
        <p className="text-[10px] font-mono uppercase tracking-widest text-white/35">{title}</p>
      </div>
      <div className="px-3 pb-3 pt-2">
        {/* Radar */}
        {chart_type === "radar" && (
          <ResponsiveContainer width="100%" height={220}>
            <RadarChart data={labels.map((s, i) => ({ subject: s, value: datasets[0]?.data[i] ?? 0 }))}>
              <PolarGrid stroke="rgba(255,255,255,0.05)" />
              <PolarAngleAxis dataKey="subject" tick={{ fill: "rgba(255,255,255,0.4)", fontSize: 9 }} />
              <PolarRadiusAxis domain={[0, 100]} tick={false} axisLine={false} />
              <Radar dataKey="value" stroke={primary} fill={primary} fillOpacity={0.15} strokeWidth={1.5} />
              <Tooltip {...chartTooltipStyle} formatter={(v: unknown) => [`${Number(v).toFixed(0)}%`]} />
            </RadarChart>
          </ResponsiveContainer>
        )}

        {/* Bar (vertical or horizontal, single or multi-dataset) */}
        {chart_type === "bar" && (
          <ResponsiveContainer width="100%" height={h}>
            <BarChart
              data={labels.map((l, i) => ({
                name: l,
                ...Object.fromEntries(datasets.map(d => [d.label, d.data[i] ?? 0]))
              }))}
              layout={isHoriz ? "vertical" : "horizontal"}
              margin={{ top: 4, right: 12, left: isHoriz ? 90 : 0, bottom: 4 }}
            >
              {isHoriz ? (
                <>
                  <XAxis type="number" domain={[0, 100]} tick={{ fill: "rgba(255,255,255,0.25)", fontSize: 8 }} />
                  <YAxis type="category" dataKey="name" tick={{ fill: "rgba(255,255,255,0.45)", fontSize: 8 }} width={85} />
                </>
              ) : (
                <>
                  <XAxis dataKey="name" tick={{ fill: "rgba(255,255,255,0.35)", fontSize: 8 }} />
                  <YAxis tick={{ fill: "rgba(255,255,255,0.25)", fontSize: 8 }} />
                </>
              )}
              <Tooltip {...chartTooltipStyle} cursor={chartCursorStyle}
                formatter={(v: unknown) => [`${Number(v).toFixed(0)}%`]} />
              {datasets.length > 1 && <Legend wrapperStyle={{ fontSize: 9, color: "rgba(255,255,255,0.4)" }} />}
              {datasets.map((d, i) => (
                <Bar key={d.label} dataKey={d.label}
                  fill={d.color || CHART_COLORS[i % CHART_COLORS.length]}
                  radius={isHoriz ? [0, 3, 3, 0] : [3, 3, 0, 0]} />
              ))}
            </BarChart>
          </ResponsiveContainer>
        )}

        {/* Doughnut / pie */}
        {(chart_type === "doughnut" || chart_type === "pie") && (
          <ResponsiveContainer width="100%" height={170}>
            <PieChart>
              <Pie
                data={labels.map((l, i) => ({ name: l, value: datasets[0]?.data[i] ?? 0 }))}
                cx="50%" cy="50%"
                innerRadius={chart_type === "doughnut" ? 42 : 0}
                outerRadius={65}
                paddingAngle={2}
                dataKey="value"
              >
                {labels.map((_, i) => <Cell key={i} fill={colors[i % colors.length]} />)}
              </Pie>
              <Tooltip {...chartTooltipStyle} formatter={(v: unknown) => [`${Number(v).toFixed(0)}%`]} />
            </PieChart>
          </ResponsiveContainer>
        )}

        {/* Line chart */}
        {chart_type === "line" && (
          <ResponsiveContainer width="100%" height={180}>
            <LineChart data={labels.map((l, i) => ({
              name: l,
              ...Object.fromEntries(datasets.map(d => [d.label, d.data[i]]))
            }))} margin={{ top: 4, right: 12, left: 0, bottom: 4 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.04)" />
              <XAxis dataKey="name" tick={{ fill: "rgba(255,255,255,0.3)", fontSize: 8 }} />
              <YAxis tick={{ fill: "rgba(255,255,255,0.25)", fontSize: 8 }} />
              <Tooltip {...chartTooltipStyle} />
              {datasets.map((d, i) => (
                <Line key={d.label} type="monotone" dataKey={d.label}
                  stroke={d.color || CHART_COLORS[i % CHART_COLORS.length]}
                  strokeWidth={2} dot={{ r: 3, fill: d.color || CHART_COLORS[i] }}
                  activeDot={{ r: 5 }} />
              ))}
            </LineChart>
          </ResponsiveContainer>
        )}

        {/* Area chart */}
        {chart_type === "area" && (
          <ResponsiveContainer width="100%" height={180}>
            <AreaChart data={labels.map((l, i) => ({
              name: l,
              ...Object.fromEntries(datasets.map(d => [d.label, d.data[i]]))
            }))} margin={{ top: 4, right: 12, left: 0, bottom: 4 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.04)" />
              <XAxis dataKey="name" tick={{ fill: "rgba(255,255,255,0.3)", fontSize: 8 }} />
              <YAxis tick={{ fill: "rgba(255,255,255,0.25)", fontSize: 8 }} />
              <Tooltip {...chartTooltipStyle} />
              {datasets.map((d, i) => {
                const c = d.color || CHART_COLORS[i % CHART_COLORS.length];
                return (
                  <Area key={d.label} type="monotone" dataKey={d.label}
                    stroke={c} fill={c} fillOpacity={0.12} strokeWidth={1.5} />
                );
              })}
            </AreaChart>
          </ResponsiveContainer>
        )}
      </div>
    </motion.div>
  );
}

// ── Widget renderers ───────────────────────────────────────────────────────────

function ScoreGrid({ spec }: { spec: WidgetSpec }) {
  const items = (spec.items as Array<{ key: string; label: string; value: number; color: string; tier: string }>) || [];
  const cols = (spec.columns as number) || 4;
  return (
    <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}
      className="rounded-2xl overflow-hidden mt-3"
      style={{ background: "rgba(196,165,116,0.03)", border: `1px solid ${GOLD.border}` }}>
      <div className="px-4 py-2.5 border-b" style={{ borderColor: GOLD.border }}>
        <p className="text-[10px] font-mono uppercase tracking-widest text-white/35">{spec.title as string}</p>
      </div>
      <div className={cn("grid gap-1.5 p-3", cols >= 5 ? "grid-cols-5" : "grid-cols-4")}>
        {items.map((item) => (
          <div key={item.key} className="rounded-xl p-2.5 text-center"
            style={{ background: `${item.color}10`, border: `1px solid ${item.color}28` }}>
            <p className="text-base font-bold leading-none" style={{ color: item.color }}>{item.value.toFixed(0)}%</p>
            <p className="text-[8px] text-white/35 mt-1 leading-tight">{item.label}</p>
            <p className="text-[7px] mt-0.5" style={{ color: `${item.color}80` }}>{item.tier}</p>
          </div>
        ))}
      </div>
    </motion.div>
  );
}

function CareerCards({ spec }: { spec: WidgetSpec }) {
  const items = (spec.items as Array<{ rank: number; title: string; family: string; suitability_pct: number; key_strengths: string[]; color: string }>) || [];
  return (
    <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}
      className="rounded-2xl overflow-hidden mt-3"
      style={{ background: "rgba(196,165,116,0.03)", border: `1px solid ${GOLD.border}` }}>
      <div className="px-4 py-2.5 border-b" style={{ borderColor: GOLD.border }}>
        <p className="text-[10px] font-mono uppercase tracking-widest text-white/35">{spec.title as string}</p>
      </div>
      <div className="p-3 space-y-2">
        {items.map((c) => (
          <div key={c.rank} className="flex items-center gap-3 rounded-xl px-3 py-2.5"
            style={{ background: `${c.color}0a`, border: `1px solid ${c.color}22` }}>
            <div className="w-6 h-6 rounded-full flex items-center justify-center text-[10px] font-bold flex-shrink-0"
              style={{ background: c.color, color: "#0a0a12" }}>{c.rank}</div>
            <div className="flex-1 min-w-0">
              <p className="text-xs font-medium text-white/80 truncate">{c.title}</p>
              <div className="flex items-center gap-1.5 mt-0.5 flex-wrap">
                <span className="text-[8px] px-1.5 py-0.5 rounded font-medium"
                  style={{ background: `${c.color}18`, color: c.color }}>{c.family}</span>
                {c.key_strengths.slice(0, 2).map((s, i) => (
                  <span key={i} className="text-[8px] text-white/28">{s}</span>
                ))}
              </div>
            </div>
            <p className="text-sm font-bold flex-shrink-0" style={{ color: c.color }}>{c.suitability_pct.toFixed(0)}%</p>
          </div>
        ))}
      </div>
    </motion.div>
  );
}

function SwotMatrix({ spec }: { spec: WidgetSpec }) {
  const quads = [
    { key: "strengths", label: "S", title: "Strengths", c: "#6b9e8f" },
    { key: "weaknesses", label: "W", title: "Weaknesses", c: "#b87d5c" },
    { key: "opportunities", label: "O", title: "Opportunities", c: "#c4a574" },
    { key: "threats", label: "T", title: "Threats", c: "#9d8bb5" },
  ];
  return (
    <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}
      className="rounded-2xl overflow-hidden mt-3"
      style={{ background: "rgba(196,165,116,0.03)", border: `1px solid ${GOLD.border}` }}>
      <div className="px-4 py-2.5 border-b" style={{ borderColor: GOLD.border }}>
        <p className="text-[10px] font-mono uppercase tracking-widest text-white/35">SWOT Analysis</p>
      </div>
      <div className="grid grid-cols-2 gap-1.5 p-3">
        {quads.map(({ key, label, title, c }) => (
          <div key={key} className="rounded-xl p-3" style={{ background: `${c}0a`, border: `1px solid ${c}22` }}>
            <div className="flex items-center gap-2 mb-2">
              <span className="w-5 h-5 rounded-lg text-[10px] font-bold flex items-center justify-center"
                style={{ background: c, color: "#0a0a12" }}>{label}</span>
              <span className="text-[10px] font-medium" style={{ color: c }}>{title}</span>
            </div>
            {((spec[key] as string[]) || []).slice(0, 3).map((item, i) => (
              <p key={i} className="text-[9px] text-white/45 mb-0.5">• {item}</p>
            ))}
          </div>
        ))}
      </div>
    </motion.div>
  );
}

function MILadder({ spec }: { spec: WidgetSpec }) {
  const items = (spec.items as Array<{ rank: number; intelligence: string; value: number; color: string; tier: string }>) || [];
  return (
    <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}
      className="rounded-2xl overflow-hidden mt-3"
      style={{ background: "rgba(196,165,116,0.03)", border: `1px solid ${GOLD.border}` }}>
      <div className="px-4 py-2.5 border-b" style={{ borderColor: GOLD.border }}>
        <p className="text-[10px] font-mono uppercase tracking-widest text-white/35">{spec.title as string}</p>
      </div>
      <div className="px-3 pb-3 pt-2 space-y-2">
        {items.map((item) => (
          <div key={item.rank} className="flex items-center gap-2.5">
            <span className="text-[9px] font-mono w-4 text-right text-white/20">{item.rank}</span>
            <div className="flex-1">
              <div className="h-1.5 rounded-full bg-white/[0.04] overflow-hidden">
                <motion.div className="h-full rounded-full"
                  style={{ background: item.color }}
                  initial={{ width: 0 }}
                  animate={{ width: `${item.value}%` }}
                  transition={{ duration: 0.5, delay: item.rank * 0.04 }}
                />
              </div>
            </div>
            <span className="text-[9px] text-white/45 w-20 truncate text-right">{item.intelligence}</span>
            <span className="text-[9px] font-mono w-8 text-right" style={{ color: item.color }}>{item.value.toFixed(0)}%</span>
          </div>
        ))}
      </div>
    </motion.div>
  );
}

function BrainSummary({ spec }: { spec: WidgetSpec }) {
  const lh = (spec.left_pct as number) || 0;
  const rh = (spec.right_pct as number) || 0;
  const leftTraits  = (spec.left_traits  as string[]) || [];
  const rightTraits = (spec.right_traits as string[]) || [];
  return (
    <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}
      className="rounded-2xl overflow-hidden mt-3"
      style={{ background: "rgba(196,165,116,0.03)", border: `1px solid ${GOLD.border}` }}>
      <div className="px-4 py-2.5 border-b" style={{ borderColor: GOLD.border }}>
        <p className="text-[10px] font-mono uppercase tracking-widest text-white/35">{spec.title as string}</p>
      </div>
      <div className="grid grid-cols-2 gap-2 p-3">
        {[{ side: "Left", pct: lh, c: "#9d8bb5", traits: leftTraits },
          { side: "Right", pct: rh, c: "#c4a574", traits: rightTraits }].map(({ side, pct, c, traits }) => (
          <div key={side} className="rounded-xl p-3" style={{ background: `${c}0a`, border: `1px solid ${c}22` }}>
            <div className="flex justify-between items-center mb-2">
              <span className="text-[10px] font-medium" style={{ color: c }}>{side} Brain</span>
              <span className="text-sm font-bold" style={{ color: c }}>{pct.toFixed(0)}%</span>
            </div>
            {traits.slice(0, 3).map((t, i) => (
              <p key={i} className="text-[9px] text-white/40">• {t}</p>
            ))}
          </div>
        ))}
      </div>
      {!!spec.balance_label && (
        <p className="text-[9px] text-white/25 text-center pb-2">{String(spec.balance_label)}</p>
      )}
    </motion.div>
  );
}

function GenericWidget({ spec }: { spec: WidgetSpec }) {
  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}
      className="rounded-2xl p-4 mt-3"
      style={{ background: "rgba(196,165,116,0.03)", border: `1px solid ${GOLD.border}` }}>
      <p className="text-[10px] font-mono uppercase tracking-widest text-white/35 mb-1">{spec.title as string}</p>
    </motion.div>
  );
}

function WidgetRenderer({ spec }: { spec: WidgetSpec }) {
  const map: Record<string, React.ComponentType<{ spec: WidgetSpec }>> = {
    score_grid: ScoreGrid, score_grid_quotients: ScoreGrid, score_grid_mi: ScoreGrid,
    career_cards: CareerCards,
    swot_matrix: SwotMatrix,
    mi_strength_ladder: MILadder,
    brain_summary: BrainSummary,
  };
  const Comp = map[spec.widget_type] || GenericWidget;
  return <Comp spec={spec} />;
}

// ── Suggestion chips ───────────────────────────────────────────────────────────

function SuggestionChips({ chips, onSelect }: { chips: string[]; onSelect: (q: string) => void }) {
  return (
    <div className="flex flex-wrap gap-1.5 mt-4">
      {chips.map((chip, i) => (
        <motion.button key={i} type="button"
          initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }}
          transition={{ delay: i * 0.05 }}
          onClick={() => onSelect(chip)}
          className="text-[10px] px-3 py-1.5 rounded-xl text-white/40 hover:text-[#c4a574] transition-all border border-white/[0.05] hover:border-[#c4a574]/25 hover:bg-[#c4a574]/[0.04]"
        >{chip}</motion.button>
      ))}
    </div>
  );
}

// ── Main page ──────────────────────────────────────────────────────────────────

export default function ChatPage() {
  const { id } = useParams<{ id: string }>();
  useAuthGuard("partner");
  const accessToken = useAuthStore((s) => s.accessToken);
  const router = useRouter();

  const [result, setResult]           = useState<AnalysisResult | null>(null);
  const [messages, setMessages]       = useState<ChatMessage[]>([]);
  const [input, setInput]             = useState("");
  const [isLoading, setIsLoading]     = useState(false);
  const [threadId, setThreadId]       = useState<string | null>(null);
  const [threadTitle, setThreadTitle] = useState<string | null>(null);
  const [historyLoaded, setHistoryLoaded] = useState(false);
  // Single status pill — replaces rather than accumulates (no duplication)
  const [currentStatus, setCurrentStatus] = useState<{ status: string; msg: string } | null>(null);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [error, setError]             = useState<string | null>(null);
  const [isScrolledUp, setIsScrolledUp] = useState(false);

  const scrollAreaRef  = useRef<HTMLDivElement>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const textareaRef    = useRef<HTMLTextAreaElement>(null);
  const abortRef       = useRef<AbortController | null>(null);
  const userScrolledUpRef = useRef(false);

  const candidateName = result?.subject_name || "the candidate";

  // ── Load analysis ──────────────────────────────────────────────────────────
  useEffect(() => {
    if (!accessToken) return;
    getAnalysis(id).then(setResult).catch(() => {});
  }, [id, accessToken]);

  // ── Load chat history ──────────────────────────────────────────────────────
  useEffect(() => {
    if (!accessToken || historyLoaded) return;
    const load = async () => {
      try {
        const res = await fetch(`${apiBase()}/sessions/${id}/chat/history`, {
          headers: { Authorization: `Bearer ${accessToken}` },
        });
        if (!res.ok) return;
        const data = await res.json();
        setThreadId(data.thread_id);
        setThreadTitle(data.title || null);
        const loaded: ChatMessage[] = data.messages.map((m: {
          id: string; role: string; content: string;
          chart_specs?: ChartSpec[]; widget_specs?: WidgetSpec[]; created_at?: string
        }) => ({
          id: m.id, role: m.role as "user" | "assistant",
          content: m.content, charts: m.chart_specs || [],
          widgets: m.widget_specs || [], created_at: m.created_at,
        }));
        setMessages(loaded);
      } catch { /* ignore */ }
      setHistoryLoaded(true);
    };
    load();
  }, [id, accessToken, historyLoaded]);

  // ── Scroll detection ───────────────────────────────────────────────────────
  useEffect(() => {
    const el = scrollAreaRef.current;
    if (!el) return;
    const onScroll = () => {
      const atBottom = el.scrollHeight - el.scrollTop - el.clientHeight < 80;
      userScrolledUpRef.current = !atBottom;
      setIsScrolledUp(!atBottom);
    };
    el.addEventListener("scroll", onScroll, { passive: true });
    return () => el.removeEventListener("scroll", onScroll);
  }, []);

  // ── Auto-scroll to bottom ──────────────────────────────────────────────────
  const scrollToBottom = useCallback((force = false) => {
    if (force || !userScrolledUpRef.current) {
      messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }
  }, []);

  useEffect(() => { scrollToBottom(); }, [messages.length, scrollToBottom]);

  // Also scroll when streaming content arrives
  const forceScrollDown = useCallback(() => {
    userScrolledUpRef.current = false;
    setIsScrolledUp(false);
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, []);

  // ── Auto-resize textarea ───────────────────────────────────────────────────
  useEffect(() => {
    const el = textareaRef.current;
    if (!el) return;
    el.style.height = "auto";
    el.style.height = `${Math.min(el.scrollHeight, 140)}px`;
  }, [input]);

  // ── Status helpers — single pill, no accumulation ─────────────────────────
  const addStatus = useCallback((status: string, msg: string) => {
    setCurrentStatus({ status, msg });
  }, []);

  const clearStatus = useCallback(() => {
    setCurrentStatus(null);
  }, []);

  // ── Process NDJSON chunk ───────────────────────────────────────────────────
  const processChunk = useCallback((chunk: Record<string, unknown>, assistantId: string) => {
    const ct = chunk.chunk_type as string;
    if (ct === "status") {
      addStatus(chunk.status as string, chunk.status_message as string);
    } else if (ct === "text") {
      setMessages((prev) => prev.map((m) =>
        m.id === assistantId ? { ...m, content: m.content + (chunk.response as string || "") } : m
      ));
      // Auto-scroll if not scrolled up
      if (!userScrolledUpRef.current) {
        requestAnimationFrame(() => messagesEndRef.current?.scrollIntoView());
      }
    } else if (ct === "chart" && chunk.chart) {
      setMessages((prev) => prev.map((m) =>
        m.id === assistantId ? { ...m, charts: [...(m.charts || []), chunk.chart as ChartSpec] } : m
      ));
    } else if (ct === "widget" && chunk.widget) {
      setMessages((prev) => prev.map((m) =>
        m.id === assistantId ? { ...m, widgets: [...(m.widgets || []), chunk.widget as WidgetSpec] } : m
      ));
    } else if (ct === "suggestions" && Array.isArray(chunk.suggested_questions)) {
      setMessages((prev) => prev.map((m) =>
        m.id === assistantId ? { ...m, suggestions: chunk.suggested_questions as string[] } : m
      ));
    } else if (ct === "done") {
      setMessages((prev) => prev.map((m) =>
        m.id === assistantId ? { ...m, isStreaming: false } : m
      ));
      clearStatus();
      scrollToBottom(true);
    }
  }, [addStatus, clearStatus, scrollToBottom]);

  // ── Send message ───────────────────────────────────────────────────────────
  const sendMessage = useCallback(async (text: string) => {
    if (!text.trim() || isLoading) return;
    setError(null);
    clearStatus();
    const uid = `u-${Date.now()}`;
    const aid = `a-${Date.now()}`;
    setMessages((prev) => [
      ...prev,
      { id: uid, role: "user", content: text },
      { id: aid, role: "assistant", content: "", charts: [], widgets: [], isStreaming: true },
    ]);
    setInput("");
    setIsLoading(true);
    userScrolledUpRef.current = false;
    setIsScrolledUp(false);
    abortRef.current = new AbortController();

    try {
      const res = await fetch(`${apiBase()}/sessions/${id}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json", Authorization: `Bearer ${accessToken}` },
        body: JSON.stringify({ message: text, thread_id: threadId }),
        signal: abortRef.current.signal,
      });
      if (!res.ok) throw new Error((await res.text()) || `HTTP ${res.status}`);

      const newThread = res.headers.get("X-Thread-Id");
      if (newThread && newThread !== threadId) {
        setThreadId(newThread);
      }

      const reader = res.body?.getReader();
      if (!reader) throw new Error("No response body");
      const dec = new TextDecoder();
      let buf = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        buf += dec.decode(value, { stream: true });
        const lines = buf.split("\n");
        buf = lines.pop() || "";
        for (const line of lines) {
          const t = line.trim();
          if (!t) continue;
          try { processChunk(JSON.parse(t), aid); } catch { /* skip */ }
        }
      }

      // Poll for title update if this was first message
      if (!threadTitle && threadId) {
        setTimeout(async () => {
          try {
            const histRes = await fetch(`${apiBase()}/sessions/${id}/chat/history`, {
              headers: { Authorization: `Bearer ${accessToken}` },
            });
            if (histRes.ok) {
              const d = await histRes.json();
              if (d.title) setThreadTitle(d.title);
            }
          } catch { /* ignore */ }
        }, 3000);
      }
    } catch (e: unknown) {
      if ((e as Error).name === "AbortError") return;
      const errMsg = e instanceof Error ? e.message : "Failed to connect";
      setError(errMsg);
      setMessages((prev) => prev.map((m) =>
        m.id === aid ? { ...m, content: "I couldn't connect to the AI service. Please check your connection and try again.", isStreaming: false, error: true } : m
      ));
      clearStatus();
    } finally {
      setIsLoading(false);
    }
  }, [isLoading, id, accessToken, threadId, processChunk, clearStatus, threadTitle, scrollToBottom]);

  const handleKey = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); sendMessage(input); }
  };

  const clearChat = async () => {
    if (!accessToken) return;
    await fetch(`${apiBase()}/sessions/${id}/chat`, {
      method: "DELETE", headers: { Authorization: `Bearer ${accessToken}` },
    }).catch(() => {});
    setMessages([]);
    setThreadId(null);
    setThreadTitle(null);
    setHistoryLoaded(false);
    clearStatus();
  };

  const isEmpty = messages.length === 0;
  const streamingMsg = messages.find((m) => m.isStreaming);

  return (
    <div className="fixed inset-0 flex overflow-hidden" style={{ background: "#020208", top: 56 }}>
      {/* Ambient background */}
      <div className="absolute inset-0 pointer-events-none overflow-hidden">
        <div className="absolute -top-32 -right-32 w-[500px] h-[500px] rounded-full opacity-[0.03]"
          style={{ background: "radial-gradient(circle, #c4a574, transparent 70%)", filter: "blur(60px)" }} />
        <div className="absolute -bottom-32 -left-32 w-[400px] h-[400px] rounded-full opacity-[0.03]"
          style={{ background: "radial-gradient(circle, #9d8bb5, transparent 70%)", filter: "blur(50px)" }} />
        <div className="absolute inset-0 opacity-20"
          style={{
            backgroundImage: "linear-gradient(rgba(196,165,116,0.04) 1px, transparent 1px), linear-gradient(90deg, rgba(196,165,116,0.04) 1px, transparent 1px)",
            backgroundSize: "48px 48px",
          }} />
      </div>

      {/* ── Sidebar ─────────────────────────────────────────────────────── */}
      <AnimatePresence>
        {sidebarOpen && (
          <>
            {/* Mobile scrim */}
            <motion.div className="fixed inset-0 bg-black/50 z-[5] lg:hidden"
              initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
              onClick={() => setSidebarOpen(false)} />

            <motion.aside
              initial={{ x: -270, opacity: 0 }}
              animate={{ x: 0, opacity: 1 }}
              exit={{ x: -270, opacity: 0 }}
              transition={{ duration: 0.3, ease: [0.16, 1, 0.3, 1] }}
              className="w-[280px] max-w-[85vw] lg:w-[250px] flex-shrink-0 flex flex-col z-20 lg:z-10 lg:relative fixed left-0 top-0 bottom-0"
              style={{ borderRight: `1px solid ${GOLD.border}`, background: "rgba(4,4,15,0.97)", backdropFilter: "blur(24px)" }}
            >
              {/* Sidebar header — no logo here (the main nav above already
                  carries the brand logo; duplicating it looked cluttered).
                  This is the consultant's identity block instead. */}
              <div className="flex items-center justify-between px-4 py-3.5 flex-shrink-0"
                style={{ borderBottom: `1px solid ${GOLD.border}` }}>
                <div className="flex items-center gap-2.5">
                  <div className="w-8 h-8 rounded-xl flex items-center justify-center flex-shrink-0"
                    style={{ border: `1px solid ${GOLD.border}`, background: "linear-gradient(135deg, rgba(196,165,116,0.15), rgba(157,139,181,0.10))" }}>
                    <MessageSquare className="w-4 h-4" style={{ color: GOLD.primary }} />
                  </div>
                  <div>
                    <p className="text-[12px] font-semibold text-white/85 leading-none">AI Consultant</p>
                    <p className="text-[8px] text-white/25 font-mono mt-0.5 uppercase tracking-wider">DMIT Advisory</p>
                  </div>
                </div>
                <button type="button" onClick={() => setSidebarOpen(false)}
                  className="w-6 h-6 rounded-lg flex items-center justify-center text-white/20 hover:text-white/55 transition-colors">
                  <X className="w-3.5 h-3.5" />
                </button>
              </div>

              {/* Actions */}
              <div className="px-3 pt-3 space-y-1 flex-shrink-0">
                <Link href={`/analysis/${id}`}
                  className="flex items-center gap-2 px-3 py-2 rounded-xl text-white/35 hover:text-white/65 text-[11px] transition-all hover:bg-white/[0.025] border border-transparent hover:border-white/[0.05]">
                  <ArrowLeft className="w-3 h-3 flex-shrink-0" /> Back to Analysis
                </Link>
                <button type="button" onClick={clearChat}
                  className="flex items-center gap-2 w-full px-3 py-2 rounded-xl text-white/35 hover:text-[#c4a574] text-[11px] transition-all hover:bg-[#c4a574]/[0.04] border border-transparent hover:border-[#c4a574]/15">
                  <Plus className="w-3 h-3 flex-shrink-0" /> New Conversation
                </button>
              </div>

              {/* Session info */}
              <div className="px-3 pt-3 flex-shrink-0">
                <div className="px-3 py-3 rounded-2xl"
                  style={{ background: "rgba(196,165,116,0.04)", border: `1px solid ${GOLD.border}` }}>
                  <p className="text-[8px] text-white/20 font-mono uppercase tracking-widest mb-1.5">Session</p>
                  <p className="text-[11px] font-medium text-white/75 truncate">{candidateName}</p>
                  <p className="text-[8px] text-white/20 font-mono mt-0.5">{id.slice(0, 16)}…</p>
                  {result?.status === "completed" && (
                    <div className="flex items-center gap-1 mt-1.5">
                      <div className="w-1.5 h-1.5 rounded-full bg-emerald-400/60" />
                      <p className="text-[8px] text-emerald-400/60 font-mono">Analysis Complete</p>
                    </div>
                  )}
                </div>
              </div>

              {/* Chat title + history */}
              <div className="px-3 pt-3 flex-1 overflow-y-auto min-h-0">
                {threadTitle && (
                  <div className="mb-3">
                    <p className="text-[8px] text-white/18 font-mono uppercase tracking-widest px-1 mb-1.5">Current Chat</p>
                    <div className="px-3 py-2 rounded-xl"
                      style={{ background: `${GOLD.primary}08`, border: `1px solid ${GOLD.border}` }}>
                      <p className="text-[11px] text-white/65 font-medium">{threadTitle}</p>
                      <p className="text-[8px] text-white/25 font-mono mt-0.5">{messages.length} messages</p>
                    </div>
                  </div>
                )}

                {messages.length > 0 && (
                  <>
                    <p className="text-[8px] text-white/18 font-mono uppercase tracking-widest px-1 mb-1.5">Messages</p>
                    <div className="space-y-0.5">
                      {messages.filter((m) => m.role === "user").slice(-8).map((m) => (
                        <div key={m.id}
                          className="px-2.5 py-2 rounded-xl text-[10px] text-white/35 truncate cursor-default hover:text-white/55 hover:bg-white/[0.02] transition-colors">
                          {m.content.slice(0, 38)}{m.content.length > 38 ? "…" : ""}
                        </div>
                      ))}
                    </div>
                  </>
                )}
              </div>

              {/* Quick starters */}
              <div className="flex-shrink-0 p-3" style={{ borderTop: `1px solid ${GOLD.border}` }}>
                <p className="text-[8px] text-white/18 font-mono uppercase tracking-widest mb-2 px-1">Quick Start</p>
                <div className="grid grid-cols-2 gap-1">
                  {STARTER_SUGGESTIONS.slice(0, 6).map((s) => (
                    <button key={s.label} type="button" onClick={() => sendMessage(s.q)}
                      className="text-left px-2 py-1.5 rounded-xl text-[9px] text-white/35 hover:text-[#c4a574] transition-all border border-white/[0.04] hover:border-[#c4a574]/15 hover:bg-[#c4a574]/[0.04]">
                      {s.label}
                    </button>
                  ))}
                </div>
              </div>
            </motion.aside>
          </>
        )}
      </AnimatePresence>

      {/* ── Main area ──────────────────────────────────────────────────────── */}
      <div className="flex-1 flex flex-col min-w-0 relative z-10">
        {/* Top bar */}
        <div className="flex items-center justify-between px-4 h-12 flex-shrink-0"
          style={{ borderBottom: `1px solid ${GOLD.border}`, background: "rgba(4,4,15,0.7)", backdropFilter: "blur(12px)" }}>
          <div className="flex items-center gap-2.5">
            {!sidebarOpen && (
              <button type="button" onClick={() => setSidebarOpen(true)}
                className="w-7 h-7 rounded-xl flex items-center justify-center text-white/25 hover:text-white/60 transition-colors"
                style={{ border: "1px solid rgba(255,255,255,0.05)" }}>
                <MessageSquare className="w-3.5 h-3.5" />
              </button>
            )}
            <div className="flex items-center gap-2">
              <p className="text-[12px] font-medium text-white/80">AI Consultant</p>
              {threadTitle && (
                <span className="hidden sm:block text-[10px] text-white/25 font-mono">· {threadTitle}</span>
              )}
            </div>
            {isLoading && (
              <div className="flex items-center gap-1.5 text-[10px] font-mono"
                style={{ color: "rgba(196,165,116,0.6)" }}>
                <motion.div animate={{ opacity: [1, 0.3, 1] }} transition={{ duration: 1, repeat: Infinity }}
                  className="w-1.5 h-1.5 rounded-full" style={{ background: GOLD.primary }} />
                Thinking
              </div>
            )}
          </div>
          <div className="flex items-center gap-1.5">
            {messages.length > 0 && (
              <button type="button" onClick={clearChat} title="Clear conversation"
                className="w-7 h-7 rounded-xl flex items-center justify-center text-white/18 hover:text-rose-400 transition-colors">
                <Trash2 className="w-3.5 h-3.5" />
              </button>
            )}
            <Link href={`/analysis/${id}`}
              className="flex items-center gap-1 text-[10px] px-2.5 py-1.5 rounded-xl text-white/30 hover:text-white/55 border border-white/[0.05] hover:border-white/[0.08] transition-all">
              <ArrowLeft className="w-3 h-3" />
              <span className="hidden sm:inline">Analysis</span>
            </Link>
          </div>
        </div>

        {/* Messages scroll area.
            min-h-0 is REQUIRED: inside a flex column, a child's implicit
            min-height:auto prevents it from shrinking below its content, so
            overflow-y-auto never engages and the mouse wheel appears dead. */}
        <div
          ref={scrollAreaRef}
          className="flex-1 min-h-0 overflow-y-auto overscroll-contain"
          style={{ scrollbarWidth: "thin", scrollbarColor: `rgba(196,165,116,0.15) transparent` }}
        >
          <div className="max-w-3xl mx-auto px-4 py-6 space-y-6 pb-4">
            {/* Empty state */}
            {isEmpty && (
              <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }} className="pt-6 text-center">
                <div className="w-16 h-16 rounded-2xl mx-auto mb-5 flex items-center justify-center"
                  style={{ border: `1px solid ${GOLD.border}`, background: "linear-gradient(135deg, rgba(196,165,116,0.12), rgba(157,139,181,0.08))" }}>
                  <MessageSquare className="w-7 h-7" style={{ color: GOLD.primary }} />
                </div>
                <h2 className="text-xl font-semibold text-white/85 mb-2">AI Consultant</h2>
                <p className="text-[13px] text-white/30 mb-8 max-w-md mx-auto leading-relaxed">
                  Your personalised AI counsellor for {candidateName}.
                  Ask anything about intelligence, careers, brain patterns, or development.
                </p>
                <div className="grid grid-cols-2 sm:grid-cols-3 gap-2 max-w-2xl mx-auto">
                  {STARTER_SUGGESTIONS.map((s, i) => (
                    <motion.button key={s.label} type="button"
                      initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: 0.1 + i * 0.04 }}
                      onClick={() => sendMessage(s.q)}
                      className="text-left p-3.5 rounded-2xl transition-all group"
                      style={{ background: "rgba(196,165,116,0.03)", border: `1px solid ${GOLD.border}` }}>
                      <p className="font-medium text-[11px] text-white/60 group-hover:text-[#c4a574] transition-colors mb-1">{s.label}</p>
                      <p className="text-white/22 text-[9px] leading-tight line-clamp-2">{s.q}</p>
                      <ChevronRight className="w-3 h-3 text-white/12 group-hover:text-[#c4a574]/40 mt-1.5 transition-colors" />
                    </motion.button>
                  ))}
                </div>
              </motion.div>
            )}

            {/* Messages */}
            {messages.map((msg) => (
              <motion.div key={msg.id}
                initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}
                className={cn("flex", msg.role === "user" ? "justify-end" : "justify-start gap-3")}>
                {/* AI avatar */}
                {msg.role === "assistant" && (
                  <div className="w-7 h-7 rounded-xl flex items-center justify-center flex-shrink-0 mt-1 self-start"
                    style={{ border: `1px solid ${GOLD.border}`, background: "rgba(196,165,116,0.08)" }}>
                    <MessageSquare className="w-3.5 h-3.5" style={{ color: `${GOLD.primary}cc` }} />
                  </div>
                )}

                <div className={cn("min-w-0", msg.role === "user" ? "max-w-[75%]" : "flex-1 min-w-0")}>
                  <div className={cn("rounded-2xl px-4 py-3",
                    msg.role === "user" ? "rounded-br-sm" : "rounded-bl-sm")}
                    style={msg.role === "user"
                      ? { background: `${GOLD.primary}18`, border: `1px solid ${GOLD.border}` }
                      : { background: "rgba(255,255,255,0.022)", border: "1px solid rgba(255,255,255,0.055)" }}>

                    {msg.role === "user" ? (
                      <p className="text-[13px] text-white/80 leading-relaxed">{msg.content}</p>
                    ) : (
                      <>
                        {/* Status pill — single, animates to next (while streaming) */}
                        {msg.isStreaming && currentStatus && (
                          <AnimatePresence mode="wait">
                            <StatusPill key={currentStatus.msg} entry={{ ...currentStatus, id: 0 }} />
                          </AnimatePresence>
                        )}

                        {/* Typing dots (no content and no status yet) */}
                        {msg.isStreaming && !msg.content && !currentStatus && (
                          <div className="flex items-center gap-1.5 py-1">
                            {[0,1,2].map((i) => (
                              <motion.div key={i} className="w-1.5 h-1.5 rounded-full"
                                style={{ background: GOLD.primary }}
                                animate={{ scale: [1,1.4,1], opacity: [0.3,1,0.3] }}
                                transition={{ duration: 0.9, repeat: Infinity, delay: i * 0.2 }}
                              />
                            ))}
                          </div>
                        )}

                        {/* Text */}
                        {msg.content && <Markdown>{msg.content}</Markdown>}

                        {/* Streaming cursor */}
                        {msg.isStreaming && msg.content && (
                          <motion.span animate={{ opacity: [1,0,1] }}
                            transition={{ duration: 0.7, repeat: Infinity }}
                            className="inline-block w-0.5 h-3.5 ml-0.5 rounded-full"
                            style={{ background: GOLD.primary, verticalAlign: "text-bottom" }}
                          />
                        )}

                        {/* Charts */}
                        {(msg.charts || []).map((c, i) => <InlineChart key={i} spec={c} />)}

                        {/* Widgets */}
                        {(msg.widgets || []).map((w, i) => <WidgetRenderer key={i} spec={w} />)}

                        {/* Suggestions */}
                        {!msg.isStreaming && (msg.suggestions || []).length > 0 && (
                          <SuggestionChips chips={msg.suggestions!} onSelect={sendMessage} />
                        )}

                        {/* Error badge */}
                        {msg.error && (
                          <div className="flex items-center gap-1.5 mt-2 text-rose-400/60 text-[10px]">
                            <AlertTriangle className="w-3 h-3" />
                            Connection error — please try again
                          </div>
                        )}
                      </>
                    )}
                  </div>
                </div>
              </motion.div>
            ))}

            {/* Error banner */}
            {error && (
              <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}
                className="flex items-center justify-between gap-3 px-4 py-2.5 rounded-2xl text-rose-400 text-[11px]"
                style={{ background: "rgba(244,63,94,0.05)", border: "1px solid rgba(244,63,94,0.18)" }}>
                <div className="flex items-center gap-2">
                  <AlertTriangle className="w-3.5 h-3.5 flex-shrink-0" />
                  {error}
                </div>
                <button type="button" onClick={() => setError(null)} className="hover:text-rose-300">
                  <X className="w-3.5 h-3.5" />
                </button>
              </motion.div>
            )}

            <div ref={messagesEndRef} className="h-px" />
          </div>
        </div>

        {/* Jump-to-bottom button */}
        <AnimatePresence>
          {isScrolledUp && (
            <motion.button
              type="button"
              initial={{ opacity: 0, scale: 0.8, y: 8 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.8, y: 8 }}
              transition={{ duration: 0.2 }}
              onClick={forceScrollDown}
              className="absolute bottom-24 right-6 z-20 flex items-center gap-1.5 px-3 py-2 rounded-2xl text-[11px] font-medium shadow-2xl"
              style={{
                background: "rgba(4,4,15,0.95)",
                border: `1px solid ${GOLD.border}`,
                backdropFilter: "blur(12px)",
                color: GOLD.primary,
                boxShadow: `0 8px 32px rgba(0,0,0,0.5), 0 0 20px rgba(196,165,116,0.1)`,
              }}
            >
              <ChevronDown className="w-3.5 h-3.5" />
              Latest
            </motion.button>
          )}
        </AnimatePresence>

        {/* Composer */}
        <div className="flex-shrink-0 px-4 pb-4 pt-2">
          <div className="max-w-3xl mx-auto">
            {/* Suggestions above composer */}
            {!isLoading && isEmpty && (
              <div className="flex flex-wrap gap-1.5 mb-2">
                {STARTER_SUGGESTIONS.slice(0, 3).map((s) => (
                  <button key={s.label} type="button" onClick={() => sendMessage(s.q)}
                    className="text-[10px] px-2.5 py-1.5 rounded-xl text-white/35 hover:text-[#c4a574] transition-all border border-white/[0.05] hover:border-[#c4a574]/20">
                    {s.label}
                  </button>
                ))}
              </div>
            )}

            <div className="flex items-end gap-3 rounded-2xl px-4 py-3 transition-all"
              style={{
                background: "rgba(255,255,255,0.025)",
                border: `1px solid ${isLoading ? GOLD.border : "rgba(255,255,255,0.07)"}`,
                boxShadow: isLoading ? `0 0 40px rgba(196,165,116,0.06)` : "none",
                transition: "border-color 0.3s, box-shadow 0.3s",
              }}>
              <textarea ref={textareaRef}
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKey}
                placeholder={isLoading ? "Thinking…" : `Ask about ${candidateName}…`}
                disabled={isLoading}
                rows={1}
                className="flex-1 bg-transparent resize-none text-[13px] text-white/75 placeholder:text-white/20 focus:outline-none focus:ring-0 focus:border-transparent leading-relaxed py-0.5"
                style={{ fontFamily: "inherit", maxHeight: "140px", outline: "none", boxShadow: "none" }}
              />
              <motion.button type="button"
                onClick={() => sendMessage(input)}
                disabled={!input.trim() || isLoading}
                whileTap={{ scale: 0.88 }}
                className={cn("w-9 h-9 rounded-xl flex items-center justify-center flex-shrink-0 transition-all",
                  input.trim() && !isLoading ? "cursor-pointer" : "opacity-25 cursor-not-allowed")}
                style={input.trim() && !isLoading
                  ? { background: GOLD.gradient, color: "#0a0a12", boxShadow: `0 4px 16px ${GOLD.glow}` }
                  : { background: "rgba(255,255,255,0.04)" }}>
                {isLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4" />}
              </motion.button>
            </div>
            <p className="text-center text-[9px] text-white/12 mt-1.5 font-mono">
              Shift+Enter for new line · For educational & counselling purposes
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
