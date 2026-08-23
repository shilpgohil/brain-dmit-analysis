"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import Link from "next/link";
import { apiBase } from "@/lib/api";
import { useAuthStore } from "@/store/authStore";
import { useAuthGuard } from "@/hooks/useAuthGuard";
import { ChevronLeft, Loader2 } from "lucide-react";

interface Partner {
  id: string; name: string; email: string; centre_name?: string;
  city?: string; state?: string; phone?: string; plan_id?: string;
  is_active: number; public_slug?: string; notes?: string;
  overrides?: FeatureOverride[];
}

interface FeatureOverride { feature_id: string; feature_value: string; key: string; display_name: string; }
interface PlanFeature { key: string; display_name: string; value_type: string; default_value?: string; feature_value?: string; category: string; id?: string; }
interface Plan { id: string; name: string; display_name: string; color_hex: string; }

export default function PartnerDetailPage() {
  const { id } = useParams<{ id: string }>();
  const { user, isLoading: authLoading } = useAuthGuard("admin");
  const { accessToken } = useAuthStore();
  const [partner, setPartner] = useState<Partner | null>(null);
  const [plans, setPlans] = useState<Plan[]>([]);
  const [planFeatures, setPlanFeatures] = useState<PlanFeature[]>([]);
  const [allFeatures, setAllFeatures] = useState<PlanFeature[]>([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState<string | null>(null);
  const [tab, setTab] = useState<"overview" | "features" | "sessions">("overview");

  const headers = { Authorization: `Bearer ${accessToken}` };

  const load = async () => {
    if (!accessToken) return;
    const [p, pl, af] = await Promise.all([
      fetch(`${apiBase()}/admin/partners/${id}`, { headers }).then((r) => r.json()),
      fetch(`${apiBase()}/admin/plans`, { headers }).then((r) => r.json()),
      fetch(`${apiBase()}/admin/features`, { headers }).then((r) => r.json()),
    ]);
    setPartner(p);
    setPlans(pl);
    setAllFeatures(af);
    if (p.plan_id) {
      const pf = await fetch(`${apiBase()}/admin/plans/${p.plan_id}/features`, { headers }).then((r) => r.json());
      setPlanFeatures(pf);
    }
    setLoading(false);
  };

  useEffect(() => { load(); }, [id, accessToken]);

  const setOverride = async (feature_id: string, value: string, display_name: string) => {
    setSaving(feature_id);
    await fetch(`${apiBase()}/admin/partners/${id}/features`, {
      method: "PUT",
      headers: { ...headers, "Content-Type": "application/json" },
      body: JSON.stringify({ feature_id, feature_value: value, reason: "Admin override" }),
    });
    await load();
    setSaving(null);
  };

  if (authLoading || !user) return (
    <div className="flex items-center justify-center min-h-[60vh]">
      <div className="w-7 h-7 rounded-full border-2 border-[#c4a574] border-t-transparent animate-spin" />
    </div>
  );

  if (loading) return (
    <div className="flex items-center justify-center min-h-[60vh] gap-2 text-white/30">
      <Loader2 className="w-4 h-4 animate-spin" /> Loading…
    </div>
  );

  if (!partner) return <p className="text-rose-400 p-8">Partner not found.</p>;

  const plan = plans.find((p) => p.id === partner.plan_id);

  // Build merged feature view: plan defaults + overrides
  const overrideMap = new Map<string, string>(
    (partner.overrides ?? []).map((o) => [o.feature_id, o.feature_value])
  );

  return (
    <div className="min-h-screen p-8">
      <div className="max-w-4xl mx-auto">
        {/* Back */}
        <Link href="/admin/partners" className="flex items-center gap-1.5 text-sm text-white/35 hover:text-white/70 mb-6 transition-colors">
          <ChevronLeft className="w-4 h-4" /> Back to Partners
        </Link>

        <div className="flex items-start justify-between gap-4 mb-6">
          <div>
            <h1 className="font-serif-display text-2xl text-white">{partner.name}</h1>
            <p className="text-white/35 text-sm mt-0.5">
              {partner.email} · {partner.centre_name ?? "—"} · {partner.city ?? "—"}
            </p>
          </div>
          <div className="flex items-center gap-3">
            {plan && (
              <span className="text-xs px-3 py-1 rounded-full font-mono uppercase tracking-wide"
                style={{ color: plan.color_hex, background: `${plan.color_hex}15`, border: `1px solid ${plan.color_hex}30` }}>
                {plan.display_name}
              </span>
            )}
            <span className={`text-xs px-3 py-1 rounded-full font-mono`}
              style={{ color: partner.is_active ? "#10b981" : "#f43f5e", background: partner.is_active ? "rgba(16,185,129,0.12)" : "rgba(244,63,94,0.12)" }}>
              {partner.is_active ? "Active" : "Inactive"}
            </span>
          </div>
        </div>

        {/* Tabs */}
        <div className="flex gap-1 p-1 rounded-xl w-fit mb-6"
          style={{ background: "rgba(255,255,255,0.03)", border: "1px solid rgba(255,255,255,0.06)" }}>
          {(["overview", "features", "sessions"] as const).map((t) => (
            <button key={t} onClick={() => setTab(t)}
              className="px-4 py-2 rounded-lg text-xs font-mono uppercase tracking-widest transition-all"
              style={tab === t
                ? { background: "linear-gradient(135deg, #e8dcc8 0%, #c4a574 100%)", color: "#1a1510" }
                : { color: "rgba(255,255,255,0.35)" }}>
              {t}
            </button>
          ))}
        </div>

        {/* Feature flags tab */}
        {tab === "features" && (
          <div className="space-y-3">
            <p className="text-xs text-white/30 leading-relaxed mb-4">
              Overrides take precedence over the partner&apos;s plan defaults. Toggle a feature here to
              grant or restrict access regardless of their current plan.
            </p>
            {allFeatures.map((f: PlanFeature & { id?: string }) => {
              // Find plan default
              const planDefault = planFeatures.find((pf) => pf.key === f.key)?.feature_value ?? f.default_value ?? "false";
              const override = overrideMap.get(f.id ?? "");
              const effective = override ?? planDefault;
              const isBool = f.value_type === "boolean";
              const isEnabled = effective !== "false" && effective !== "0" && effective !== "";
              const hasOverride = override !== undefined;

              return (
                <motion.div key={f.key}
                  className="flex items-center gap-4 px-5 py-4 rounded-2xl"
                  style={{
                    background: hasOverride ? "rgba(196,165,116,0.04)" : "rgba(255,255,255,0.02)",
                    border: hasOverride ? "1px solid rgba(196,165,116,0.2)" : "1px solid rgba(255,255,255,0.05)",
                  }}
                >
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2">
                      <p className="text-sm text-white/75">{f.display_name}</p>
                      {hasOverride && (
                        <span className="text-[8px] font-mono px-1.5 py-0.5 rounded"
                          style={{ background: "rgba(196,165,116,0.15)", color: "#c4a574" }}>
                          OVERRIDE
                        </span>
                      )}
                    </div>
                    <p className="text-[10px] text-white/25 font-mono mt-0.5">
                      {f.key} · plan default: {planDefault}
                    </p>
                  </div>

                  {isBool ? (
                    <button
                      onClick={() => setOverride(f.id ?? "", isEnabled ? "false" : "true", f.display_name)}
                      disabled={saving === f.id}
                      className="relative w-10 h-5.5 rounded-full transition-all flex-shrink-0"
                      style={{
                        height: "22px", width: "40px",
                        background: isEnabled ? "#c4a574" : "rgba(255,255,255,0.12)",
                      }}>
                      <span className="absolute top-0.5 w-4 h-4 rounded-full bg-white shadow transition-all"
                        style={{ left: isEnabled ? "calc(100% - 18px)" : "2px" }} />
                    </button>
                  ) : (
                    <p className="text-sm font-mono text-white/50 flex-shrink-0">{effective}</p>
                  )}
                </motion.div>
              );
            })}
          </div>
        )}

        {/* Overview tab */}
        {tab === "overview" && (
          <div className="rounded-2xl p-5 space-y-3"
            style={{ background: "rgba(255,255,255,0.02)", border: "1px solid rgba(255,255,255,0.06)" }}>
            {[
              ["Email", partner.email],
              ["Centre", partner.centre_name ?? "—"],
              ["City", partner.city ?? "—"],
              ["State", partner.state ?? "—"],
              ["Phone", partner.phone ?? "—"],
              ["Public slug", partner.public_slug ?? "—"],
              ["Notes", partner.notes ?? "—"],
            ].map(([label, value]) => (
              <div key={label} className="flex gap-4">
                <span className="text-[10px] text-white/30 font-mono uppercase tracking-widest w-28 flex-shrink-0 pt-0.5">{label}</span>
                <span className="text-sm text-white/70">{value}</span>
              </div>
            ))}
          </div>
        )}

        {tab === "sessions" && (
          <p className="text-white/30 text-sm">Session list coming soon — use the main sessions page filtered by partner.</p>
        )}
      </div>
    </div>
  );
}
