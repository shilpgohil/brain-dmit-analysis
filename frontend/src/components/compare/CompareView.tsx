"use client";

import type { AnalysisResult, QuotientKey } from "@/lib/types";
import { QUOTIENT_LABELS } from "@/lib/types";
import { GlassCard } from "@/components/ui/GlassCard";
import { GOLD } from "@/lib/analysis-theme";

const MI_KEYS: { key: keyof NonNullable<AnalysisResult["multiple_intelligences"]>; label: string }[] = [
  { key: "linguistic", label: "Linguistic" },
  { key: "logical_mathematical", label: "Logical" },
  { key: "spatial", label: "Spatial" },
  { key: "musical", label: "Musical" },
  { key: "bodily_kinesthetic", label: "Kinesthetic" },
  { key: "interpersonal", label: "Interpersonal" },
  { key: "intrapersonal", label: "Intrapersonal" },
  { key: "naturalistic", label: "Naturalistic" },
  { key: "existential", label: "Existential" },
];

const PERSONALITY_KEYS: { key: keyof NonNullable<AnalysisResult["personality"]>; label: string }[] = [
  { key: "openness", label: "Openness" },
  { key: "conscientiousness", label: "Conscientiousness" },
  { key: "extraversion", label: "Extraversion" },
  { key: "agreeableness", label: "Agreeableness" },
  { key: "neuroticism", label: "Neuroticism" },
];

const QUOTIENT_ORDER: QuotientKey[] = ["IQ", "EQ", "CQ", "AQ", "SQ", "PQ", "LQ", "MQ", "FQ", "DQ"];

const COLOR_A = "#c4a574";
const COLOR_B = "#9d8bb5";

function pct(n: number | null | undefined) {
  if (n == null) return null;
  return Math.round(n * 100);
}

function CompareRow({
  label,
  va,
  vb,
  colorA = COLOR_A,
  colorB = COLOR_B,
}: {
  label: string;
  va: number | null | undefined;
  vb: number | null | undefined;
  colorA?: string;
  colorB?: string;
}) {
  const pa = pct(va);
  const pb = pct(vb);
  if (pa == null && pb == null) return null;
  const diff = pa != null && pb != null ? pa - pb : null;

  return (
    <div>
      <div className="flex justify-between text-[11px] mb-1.5">
        <span className="text-white/60">{label}</span>
        <span className="font-mono text-white/40">
          {pa != null ? `${pa}%` : "N/A"} vs {pb != null ? `${pb}%` : "N/A"}
          {diff != null && Math.abs(diff) > 5 && (
            <span className="ml-1" style={{ color: diff > 0 ? colorA : colorB }}>
              ({diff > 0 ? "+" : ""}{diff})
            </span>
          )}
        </span>
      </div>
      <div className="grid grid-cols-2 gap-3">
        <div className="h-2 rounded-full bg-white/[0.06] overflow-hidden">
          {pa != null && (
            <div className="h-full rounded-full" style={{ width: `${pa}%`, background: `linear-gradient(90deg, ${colorA}80, ${colorA})` }} />
          )}
        </div>
        <div className="h-2 rounded-full bg-white/[0.06] overflow-hidden">
          {pb != null && (
            <div className="h-full rounded-full" style={{ width: `${pb}%`, background: `linear-gradient(90deg, ${colorB}80, ${colorB})` }} />
          )}
        </div>
      </div>
    </div>
  );
}

export function CompareView({ a, b }: { a: AnalysisResult; b: AnalysisResult }) {
  const nameA = a.subject_name ?? "Profile A";
  const nameB = b.subject_name ?? "Profile B";
  const miA = a.multiple_intelligences;
  const miB = b.multiple_intelligences;
  const persA = a.personality;
  const persB = b.personality;
  const qA = a.quotients;
  const qB = b.quotients;

  const hasQuotients = (qA && Object.keys(qA).length > 0) || (qB && Object.keys(qB).length > 0);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="grid grid-cols-2 gap-4 text-center">
        <div>
          <p className="font-serif-display text-xl text-white">{nameA}</p>
          <div className="w-full h-1 rounded-full mt-2" style={{ background: `linear-gradient(90deg, ${COLOR_A}80, ${COLOR_A})` }} />
          <p className="text-[10px] font-mono mt-1" style={{ color: COLOR_A }}>Session A</p>
        </div>
        <div>
          <p className="font-serif-display text-xl text-white">{nameB}</p>
          <div className="w-full h-1 rounded-full mt-2" style={{ background: `linear-gradient(90deg, ${COLOR_B}80, ${COLOR_B})` }} />
          <p className="text-[10px] font-mono mt-1" style={{ color: COLOR_B }}>Session B</p>
        </div>
      </div>

      {/* Multiple Intelligences */}
      {(miA || miB) && (
        <GlassCard padding="lg">
          <h3 className="font-serif-display text-lg text-white mb-5">Multiple Intelligences</h3>
          <div className="space-y-4">
            {MI_KEYS.map(({ key, label }) => (
              <CompareRow key={key} label={label} va={miA?.[key]} vb={miB?.[key]} />
            ))}
          </div>
        </GlassCard>
      )}

      {/* Quotients */}
      {hasQuotients && (
        <GlassCard padding="lg">
          <h3 className="font-serif-display text-lg text-white mb-1">10-Quotient Profile</h3>
          <p className="text-[10px] font-mono text-white/30 uppercase tracking-widest mb-5">IQ · EQ · CQ · AQ · SQ · PQ · LQ · MQ · FQ · DQ</p>
          <div className="space-y-4">
            {QUOTIENT_ORDER.map((k) => {
              const va = qA?.[k];
              const vb = qB?.[k];
              if (va == null && vb == null) return null;
              return (
                <CompareRow key={k}
                  label={`${k} — ${QUOTIENT_LABELS[k]}`}
                  va={va}
                  vb={vb}
                />
              );
            })}
          </div>
        </GlassCard>
      )}

      {/* Personality */}
      {(persA || persB) && (
        <GlassCard padding="lg">
          <h3 className="font-serif-display text-lg text-white mb-5">Personality Profile (Big Five)</h3>
          <div className="space-y-4">
            {PERSONALITY_KEYS.map(({ key, label }) => (
              <CompareRow key={key} label={label} va={persA?.[key]} vb={persB?.[key]} />
            ))}
          </div>
        </GlassCard>
      )}

      {/* Career comparison */}
      {(a.career_matches?.length > 0 || b.career_matches?.length > 0) && (
        <GlassCard padding="lg">
          <h3 className="font-serif-display text-lg text-white mb-4">Top Career Matches</h3>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <p className="text-[9px] font-mono uppercase tracking-widest mb-3" style={{ color: COLOR_A }}>
                {nameA}
              </p>
              <div className="space-y-2">
                {a.career_matches.slice(0, 5).map((c) => (
                  <div key={c.title} className="flex items-center justify-between">
                    <span className="text-[11px] text-white/60 truncate mr-2">{c.title}</span>
                    <span className="text-[10px] font-mono flex-shrink-0" style={{ color: COLOR_A }}>
                      {Math.round(c.match_score * 100)}%
                    </span>
                  </div>
                ))}
              </div>
            </div>
            <div>
              <p className="text-[9px] font-mono uppercase tracking-widest mb-3" style={{ color: COLOR_B }}>
                {nameB}
              </p>
              <div className="space-y-2">
                {b.career_matches.slice(0, 5).map((c) => (
                  <div key={c.title} className="flex items-center justify-between">
                    <span className="text-[11px] text-white/60 truncate mr-2">{c.title}</span>
                    <span className="text-[10px] font-mono flex-shrink-0" style={{ color: COLOR_B }}>
                      {Math.round(c.match_score * 100)}%
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </GlassCard>
      )}

      {/* Extension count summary */}
      {a.extensions && b.extensions && (
        <GlassCard padding="lg">
          <h3 className="font-serif-display text-lg text-white mb-2">Extension Modules</h3>
          <div className="grid grid-cols-2 gap-4 text-center">
            <div>
              <p className="text-3xl font-mono" style={{ color: COLOR_A }}>{a.extensions.length}</p>
              <p className="text-[10px] text-white/30 mt-1">modules analyzed</p>
            </div>
            <div>
              <p className="text-3xl font-mono" style={{ color: COLOR_B }}>{b.extensions.length}</p>
              <p className="text-[10px] text-white/30 mt-1">modules analyzed</p>
            </div>
          </div>
        </GlassCard>
      )}
    </div>
  );
}
