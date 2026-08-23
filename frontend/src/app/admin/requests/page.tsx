"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { apiBase } from "@/lib/api";
import { useAuthGuard } from "@/hooks/useAuthGuard";
import { useAuthStore } from "@/store/authStore";
import { CheckCircle2, XCircle, Loader2, UserPlus } from "lucide-react";

interface Request {
  id: string; name: string; email: string; phone?: string;
  centre_name?: string; city?: string; plan_interest?: string;
  message?: string; submitted_at: string; status: string;
}
interface Plan { id: string; display_name: string; }

export default function AdminRequestsPage() {
  const { user, isLoading: authLoading } = useAuthGuard("admin");
  const accessToken = useAuthStore((s) => s.accessToken);
  const [requests, setRequests] = useState<Request[]>([]);
  const [plans, setPlans] = useState<Plan[]>([]);
  const [loading, setLoading] = useState(true);
  const [approvingId, setApprovingId] = useState<string | null>(null);
  const [showApprove, setShowApprove] = useState<Request | null>(null);
  const [newPass, setNewPass] = useState("");
  const [selectedPlan, setSelectedPlan] = useState("");
  const [error, setError] = useState<string | null>(null);

  const headers = { Authorization: `Bearer ${accessToken}` };

  const load = () => {
    if (!accessToken) return;
    Promise.all([
      fetch(`${apiBase()}/admin/requests?status_filter=pending`, { headers }).then((r) => r.json()),
      fetch(`${apiBase()}/admin/plans`, { headers }).then((r) => r.json()),
    ]).then(([reqs, pl]) => { setRequests(reqs); setPlans(pl); setLoading(false); });
  };

  useEffect(load, [accessToken]);

  if (authLoading || !user) {
    return <div className="flex items-center justify-center min-h-[60vh]"><div className="w-7 h-7 rounded-full border-2 border-[#c4a574] border-t-transparent animate-spin" /></div>;
  }

  const approve = async () => {
    if (!showApprove || !newPass) return;
    setApprovingId(showApprove.id);
    setError(null);
    try {
      const res = await fetch(`${apiBase()}/admin/requests/${showApprove.id}/approve`, {
        method: "POST",
        headers: { ...headers, "Content-Type": "application/json" },
        body: JSON.stringify({ password: newPass, plan_id: selectedPlan || null }),
      });
      if (!res.ok) throw new Error((await res.json()).detail);
      setShowApprove(null);
      setNewPass("");
      load();
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : "Error");
    } finally {
      setApprovingId(null);
    }
  };

  const reject = async (id: string) => {
    await fetch(`${apiBase()}/admin/requests/${id}/reject`, { method: "PATCH", headers });
    load();
  };

  return (
    <div className="min-h-screen p-8">
      <div className="max-w-3xl mx-auto">
        <h1 className="font-serif-display text-2xl text-white mb-1">Partner Requests</h1>
        <p className="text-white/30 text-sm mb-8">Pending applications to join the platform</p>

        {loading ? (
          <div className="flex items-center gap-2 text-white/30 py-8">
            <Loader2 className="w-4 h-4 animate-spin" /> Loading…
          </div>
        ) : requests.length === 0 ? (
          <p className="text-white/25 text-sm py-12 text-center">No pending requests.</p>
        ) : (
          <div className="space-y-3">
            {requests.map((r) => (
              <motion.div key={r.id}
                className="rounded-2xl p-5"
                style={{ background: "rgba(255,255,255,0.02)", border: "1px solid rgba(255,255,255,0.06)" }}
                initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}
              >
                <div className="flex items-start justify-between gap-4">
                  <div>
                    <p className="text-sm font-medium text-white/80">{r.name}</p>
                    <p className="text-[10px] text-white/30 font-mono mt-0.5">
                      {r.email} · {r.centre_name ?? "—"} · {r.city ?? "—"}
                    </p>
                    {r.plan_interest && (
                      <p className="text-xs text-[#c4a574] mt-1">Interested: {r.plan_interest}</p>
                    )}
                    {r.message && (
                      <p className="text-xs text-white/40 mt-2 leading-relaxed">{r.message}</p>
                    )}
                  </div>
                  <div className="flex items-center gap-2 flex-shrink-0">
                    <button onClick={() => setShowApprove(r)}
                      className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-all"
                      style={{ background: "rgba(16,185,129,0.12)", color: "#10b981", border: "1px solid rgba(16,185,129,0.2)" }}>
                      <UserPlus className="w-3.5 h-3.5" /> Approve
                    </button>
                    <button onClick={() => reject(r.id)}
                      className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-all"
                      style={{ background: "rgba(244,63,94,0.08)", color: "#f43f5e", border: "1px solid rgba(244,63,94,0.15)" }}>
                      <XCircle className="w-3.5 h-3.5" /> Reject
                    </button>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        )}

        {/* Approve modal */}
        {showApprove && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
            <button className="absolute inset-0 bg-black/70 backdrop-blur-sm" onClick={() => setShowApprove(null)} />
            <motion.div
              className="relative w-full max-w-md rounded-2xl p-6"
              style={{ background: "#0c0c18", border: "1px solid rgba(16,185,129,0.3)" }}
              initial={{ scale: 0.96, y: 12 }} animate={{ scale: 1, y: 0 }}
            >
              <h3 className="font-serif-display text-xl text-white mb-1">Approve Partner</h3>
              <p className="text-white/40 text-sm mb-5">
                Create an account for <strong className="text-white/70">{showApprove.name}</strong>
              </p>
              <div className="space-y-4">
                <div>
                  <label className="block text-[9px] font-mono uppercase tracking-widest text-white/30 mb-1">Initial Password</label>
                  <input type="text" value={newPass} onChange={(e) => setNewPass(e.target.value)}
                    placeholder="Set a secure initial password"
                    className="w-full h-10 rounded-lg px-3 text-sm text-white focus:outline-none transition-all"
                    style={{ background: "rgba(255,255,255,0.04)", border: "1px solid rgba(255,255,255,0.08)" }}
                  />
                </div>
                <div>
                  <label className="block text-[9px] font-mono uppercase tracking-widest text-white/30 mb-1">Assign Plan</label>
                  <select value={selectedPlan} onChange={(e) => setSelectedPlan(e.target.value)}
                    className="w-full h-10 rounded-lg px-3 text-sm focus:outline-none"
                    style={{ background: "rgba(8,8,24,0.9)", border: "1px solid rgba(255,255,255,0.08)", color: "rgba(255,255,255,0.7)" }}>
                    <option value="" style={{ background: "#0d0d1a" }}>No plan</option>
                    {plans.map((p) => <option key={p.id} value={p.id} style={{ background: "#0d0d1a" }}>{p.display_name}</option>)}
                  </select>
                </div>
                {error && <p className="text-sm text-rose-400">{error}</p>}
                <div className="flex gap-3">
                  <button onClick={() => setShowApprove(null)}
                    className="flex-1 py-2.5 rounded-xl text-sm text-white/40 border border-white/[0.08]">
                    Cancel
                  </button>
                  <button onClick={approve} disabled={!newPass || !!approvingId}
                    className="flex-1 py-2.5 rounded-xl text-sm font-medium"
                    style={{ background: "rgba(16,185,129,0.9)", color: "white" }}>
                    {approvingId ? "Creating…" : "Create Account"}
                  </button>
                </div>
              </div>
            </motion.div>
          </div>
        )}
      </div>
    </div>
  );
}
