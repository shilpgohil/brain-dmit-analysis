"use client";

import { useEffect, useState, useCallback } from "react";
import { motion } from "framer-motion";
import { apiBase } from "@/lib/api";
import { useAuthGuard } from "@/hooks/useAuthGuard";
import { useAuthStore } from "@/store/authStore";
import { Loader2, ChevronDown, ChevronUp, CheckCircle2, AlertCircle } from "lucide-react";

interface Plan { id: string; name: string; display_name: string; description: string; color_hex: string; sort_order: number; }
interface Feature { id: string; key: string; display_name: string; value_type: string; default_value: string; category: string; }
interface PlanFeature extends Feature { feature_value?: string; }

function authHeaders() {
  const token = useAuthStore.getState().accessToken;
  return { Authorization: `Bearer ${token}` };
}

export default function AdminPlansPage() {
  const { user, isLoading: authLoading } = useAuthGuard("admin");
  const [plans, setPlans] = useState<Plan[]>([]);
  const [expanded, setExpanded] = useState<string | null>(null);
  const [planFeatures, setPlanFeatures] = useState<Record<string, PlanFeature[]>>({});
  const [loading, setLoading] = useState(true);
  const [savingKey, setSavingKey] = useState<string | null>(null);
  const [toast, setToast] = useState<{ type: "ok" | "err"; msg: string } | null>(null);

  const showToast = (type: "ok" | "err", msg: string) => {
    setToast({ type, msg });
    setTimeout(() => setToast(null), 3000);
  };

  const loadPlans = useCallback(async () => {
    const h = authHeaders();
    if (!h.Authorization.includes("null") && h.Authorization.length > 10) {
      const res = await fetch(`${apiBase()}/admin/plans`, { headers: h });
      if (res.ok) {
        const pl = await res.json();
        setPlans(Array.isArray(pl) ? pl : []);
      }
      setLoading(false);
    }
  }, []);

  const loadPlanFeatures = useCallback(async (planId: string, force = false) => {
    if (!force && planFeatures[planId]) return;
    const h = authHeaders();
    const res = await fetch(`${apiBase()}/admin/plans/${planId}/features`, { headers: h });
    if (res.ok) {
      const pf = await res.json();
      setPlanFeatures(prev => ({ ...prev, [planId]: Array.isArray(pf) ? pf : [] }));
    }
  }, [planFeatures]);

  const toggle = (planId: string) => {
    if (expanded === planId) {
      setExpanded(null);
    } else {
      setExpanded(planId);
      loadPlanFeatures(planId);
    }
  };

  const saveFeature = async (planId: string, featureId: string, value: string) => {
    const key = `${planId}-${featureId}`;
    setSavingKey(key);

    // Optimistic update — flip toggle immediately in UI
    setPlanFeatures(prev => ({
      ...prev,
      [planId]: (prev[planId] ?? []).map(f =>
        f.id === featureId ? { ...f, feature_value: value } : f
      ),
    }));

    try {
      const h = authHeaders();
      const res = await fetch(`${apiBase()}/admin/plans/${planId}/features`, {
        method: "PUT",
        headers: { ...h, "Content-Type": "application/json" },
        body: JSON.stringify({ feature_id: featureId, feature_value: value }),
      });
      if (!res.ok) {
        const err = await res.text();
        throw new Error(err || `HTTP ${res.status}`);
      }
      // Sync confirmed server state
      await loadPlanFeatures(planId, true);
      showToast("ok", "Saved");
    } catch (e: any) {
      // Rollback optimistic update by re-fetching original state
      await loadPlanFeatures(planId, true);
      showToast("err", `Failed: ${e.message}`);
    } finally {
      setSavingKey(null);
    }
  };

  useEffect(() => { loadPlans(); }, [user]);

  if (authLoading || !user) {
    return <div className="flex items-center justify-center min-h-[60vh]"><div className="w-7 h-7 rounded-full border-2 border-[#c4a574] border-t-transparent animate-spin" /></div>;
  }

  return (
    <div className="min-h-screen p-8">
      {/* Toast notification */}
      {toast && (
        <div className={`fixed top-5 right-5 z-[200] flex items-center gap-2 px-4 py-3 rounded-xl text-sm font-medium shadow-2xl transition-all
          ${toast.type === "ok" ? "bg-emerald-950 border border-emerald-700/40 text-emerald-300" : "bg-rose-950 border border-rose-700/40 text-rose-300"}`}>
          {toast.type === "ok" ? <CheckCircle2 className="w-4 h-4" /> : <AlertCircle className="w-4 h-4" />}
          {toast.msg}
        </div>
      )}
      <div className="max-w-4xl mx-auto">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="font-serif-display text-2xl text-white">Plans & Features</h1>
            <p className="text-white/30 text-sm mt-0.5">Configure what each plan can access</p>
          </div>
        </div>

        {loading ? (
          <div className="flex items-center gap-2 text-white/30 py-8"><Loader2 className="w-4 h-4 animate-spin" /> Loading…</div>
        ) : (
          <div className="space-y-3">
            {plans.map((plan) => (
              <motion.div key={plan.id}
                className="rounded-2xl overflow-hidden"
                style={{ border: `1px solid ${plan.color_hex}30`, background: `${plan.color_hex}06` }}
                initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}>

                {/* Plan header */}
                <button
                  className="w-full flex items-center gap-4 px-6 py-4 text-left"
                  onClick={() => toggle(plan.id)}
                >
                  <div className="w-3 h-3 rounded-full flex-shrink-0" style={{ background: plan.color_hex }} />
                  <div className="flex-1">
                    <p className="text-sm font-medium text-white/80">{plan.display_name}</p>
                    <p className="text-[10px] text-white/30 mt-0.5">{plan.description || "No description"}</p>
                  </div>
                  {expanded === plan.id
                    ? <ChevronUp className="w-4 h-4 text-white/30" />
                    : <ChevronDown className="w-4 h-4 text-white/30" />}
                </button>

                {/* Feature rows */}
                {expanded === plan.id && (
                  <div className="border-t border-white/[0.06] p-4 space-y-2">
                    {planFeatures[plan.id]
                      ? planFeatures[plan.id].map((f) => {
                          const isBool = f.value_type === "boolean";
                          const current = f.feature_value ?? f.default_value ?? "false";
                          const isOn = current !== "false" && current !== "0" && current !== "";
                          return (
                            <div key={f.key} className="flex items-center gap-3 px-3 py-2 rounded-xl"
                              style={{ background: "rgba(255,255,255,0.02)" }}>
                              <div className="flex-1">
                                <p className="text-xs text-white/65">{f.display_name}</p>
                                <p className="text-[9px] font-mono text-white/25 mt-0.5">{f.key}</p>
                              </div>
                              {isBool ? (
                                <button
                                  onClick={(e) => { e.stopPropagation(); saveFeature(plan.id, f.id, isOn ? "false" : "true"); }}
                                  disabled={savingKey === `${plan.id}-${f.id}`}
                                  className="relative rounded-full transition-all flex-shrink-0 cursor-pointer"
                                  style={{ height: "22px", width: "40px", background: isOn ? plan.color_hex : "rgba(255,255,255,0.12)", opacity: savingKey === `${plan.id}-${f.id}` ? 0.6 : 1 }}>
                                  {savingKey === `${plan.id}-${f.id}` ? (
                                    <span className="absolute inset-0 flex items-center justify-center">
                                      <Loader2 className="w-3 h-3 text-white animate-spin" />
                                    </span>
                                  ) : (
                                    <span className="absolute top-0.5 w-4 h-4 rounded-full bg-white shadow transition-all duration-200"
                                      style={{ left: isOn ? "calc(100% - 18px)" : "2px" }} />
                                  )}
                                </button>
                              ) : (
                                <div className="flex items-center gap-2">
                                  <input
                                    type="text"
                                    defaultValue={current}
                                    className="w-20 h-7 rounded-lg px-2 text-xs text-white font-mono focus:outline-none text-center"
                                    style={{ background: "rgba(255,255,255,0.06)", border: "1px solid rgba(255,255,255,0.1)" }}
                                    onClick={(e) => e.stopPropagation()}
                                    onBlur={(e) => {
                                      e.stopPropagation();
                                      if (e.target.value !== current) saveFeature(plan.id, f.id, e.target.value);
                                    }}
                                  />
                                </div>
                              )}
                            </div>
                          );
                        })
                      : <div className="flex items-center gap-2 text-white/25 py-2"><Loader2 className="w-3 h-3 animate-spin" /> Loading features…</div>
                    }
                  </div>
                )}
              </motion.div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
