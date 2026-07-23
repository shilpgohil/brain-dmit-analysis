"use client";

import type { AnalysisResult } from "@/lib/types";
import { GlassCard } from "@/components/ui/GlassCard";

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

function pct(n: number) {
  return Math.round(n * 100);
}

export function CompareView({ a, b }: { a: AnalysisResult; b: AnalysisResult }) {
  const nameA = a.subject_name ?? "Profile A";
  const nameB = b.subject_name ?? "Profile B";
  const miA = a.multiple_intelligences;
  const miB = b.multiple_intelligences;

  if (!miA || !miB) {
    return <p className="text-white/40 text-sm">Intelligence data not available for one or both sessions.</p>;
  }

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-2 gap-4 text-center">
        <div>
          <p className="font-editorial text-xl text-white">{nameA}</p>
          <p className="text-[10px] font-mono text-accent-gold mt-1">Session A</p>
        </div>
        <div>
          <p className="font-editorial text-xl text-white">{nameB}</p>
          <p className="text-[10px] font-mono mt-1" style={{ color: "#9d8bb5" }}>Session B</p>
        </div>
      </div>

      <GlassCard padding="lg">
        <h3 className="font-editorial text-lg text-white mb-4">Multiple Intelligences</h3>
        <div className="space-y-4">
          {MI_KEYS.map(({ key, label }) => {
            const va = miA[key] ?? 0;
            const vb = miB[key] ?? 0;
            const diff = va - vb;
            return (
              <div key={key}>
                <div className="flex justify-between text-[11px] mb-1.5">
                  <span className="text-white/60">{label}</span>
                  <span className="font-mono text-white/40">
                    {pct(va)}% vs {pct(vb)}%
                    {Math.abs(diff) > 0.05 && (
                      <span className={diff > 0 ? " text-accent-gold ml-1" : " text-accent-sage ml-1"}>
                        ({diff > 0 ? "+" : ""}{pct(diff)})
                      </span>
                    )}
                  </span>
                </div>
                <div className="grid grid-cols-2 gap-3">
                  <div className="h-2 rounded-full bg-white/[0.06] overflow-hidden">
                    <div className="h-full rounded-full" style={{ width: `${pct(va)}%`, background: "linear-gradient(90deg, #c4a574, #e8dcc8)" }} />
                  </div>
                  <div className="h-2 rounded-full bg-white/[0.06] overflow-hidden">
                    <div className="h-full rounded-full" style={{ width: `${pct(vb)}%`, background: "linear-gradient(90deg, #9d8bb5, #b87d8a)" }} />
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </GlassCard>

      {a.extensions && b.extensions && (
        <GlassCard padding="lg">
          <h3 className="font-editorial text-lg text-white mb-2">Extension modules</h3>
          <p className="text-sm text-white/45 font-light">
            {a.extensions.length} vs {b.extensions.length} extension results computed
          </p>
        </GlassCard>
      )}
    </div>
  );
}
