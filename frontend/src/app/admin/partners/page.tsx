"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import Link from "next/link";
import { apiBase } from "@/lib/api";
import { useAuthGuard } from "@/hooks/useAuthGuard";
import { useAuthStore } from "@/store/authStore";
import { Plus, Loader2, CheckCircle2, XCircle, Search } from "lucide-react";

interface Partner {
  id: string;
  name: string;
  email: string;
  centre_name?: string;
  city?: string;
  plan_id?: string;
  is_active: number;
  session_count?: number;
  created_at: string;
}

interface Plan { id: string; name: string; display_name: string; color_hex: string; }

export default function AdminPartnersPage() {
  const { user, isLoading: authLoading } = useAuthGuard("admin");
  const accessToken = useAuthStore((s) => s.accessToken);
  const [partners, setPartners] = useState<Partner[]>([]);
  const [plans, setPlans] = useState<Plan[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [showCreate, setShowCreate] = useState(false);

  const headers = { Authorization: `Bearer ${accessToken}` };

  const load = () => {
    if (!accessToken) return;    Promise.all([
      fetch(`${apiBase()}/admin/partners`, { headers }).then((r) => r.json()),
      fetch(`${apiBase()}/admin/plans`, { headers }).then((r) => r.json()),
    ])
      .then(([p, pl]) => { setPartners(p); setPlans(pl); })
      .finally(() => setLoading(false));
  };

  useEffect(load, [accessToken]);

  if (authLoading || !user) {
    return <div className="flex items-center justify-center min-h-[60vh]"><div className="w-7 h-7 rounded-full border-2 border-[#c4a574] border-t-transparent animate-spin" /></div>;
  }

  const toggle = async (id: string, active: boolean) => {
    await fetch(`${apiBase()}/admin/partners/${id}/${active ? "deactivate" : "activate"}`, {
      method: "PATCH", headers,
    });
    load();
  };

  const filtered = partners.filter(
    (p) => !search || p.name.toLowerCase().includes(search.toLowerCase())
      || p.email.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="min-h-screen p-8">
      <div className="max-w-5xl mx-auto">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="font-serif-display text-2xl text-white">Partners</h1>
            <p className="text-white/30 text-sm mt-0.5">{partners.length} registered</p>
          </div>
          <button onClick={() => setShowCreate(true)}
            className="flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-medium transition-all"
            style={{ background: "linear-gradient(135deg, #e8dcc8 0%, #c4a574 100%)", color: "#1a1510" }}>
            <Plus className="w-4 h-4" /> New Partner
          </button>
        </div>

        {/* Search */}
        <div className="relative mb-6">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-white/25 pointer-events-none" />
          <input type="text" placeholder="Search by name or email…"
            value={search} onChange={(e) => setSearch(e.target.value)}
            className="w-full max-w-sm h-10 pl-9 pr-4 rounded-xl text-sm text-white placeholder:text-white/25 focus:outline-none transition-all"
            style={{ background: "rgba(255,255,255,0.04)", border: "1px solid rgba(255,255,255,0.08)" }}
          />
        </div>

        {loading ? (
          <div className="flex items-center gap-2 text-white/30 py-12">
            <Loader2 className="w-4 h-4 animate-spin" /> Loading partners…
          </div>
        ) : (
          <div className="space-y-2">
            {filtered.map((p) => {
              const plan = plans.find((pl) => pl.id === p.plan_id);
              return (
                <motion.div key={p.id}
                  className="flex items-center gap-4 px-5 py-4 rounded-2xl"
                  style={{ background: "rgba(255,255,255,0.02)", border: "1px solid rgba(255,255,255,0.05)" }}
                  initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}
                  whileHover={{ background: "rgba(255,255,255,0.03)" }}
                >
                  {/* Active indicator */}
                  <div className={`w-2 h-2 rounded-full flex-shrink-0 ${p.is_active ? "bg-green-400" : "bg-white/15"}`} />

                  <Link href={`/admin/partners/${p.id}`} className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-white/80">{p.name}</p>
                    <p className="text-[10px] text-white/30 font-mono mt-0.5">
                      {p.email} · {p.centre_name || "No centre"} · {p.city || "—"}
                    </p>
                  </Link>

                  <div className="flex items-center gap-3 flex-shrink-0">
                    {plan && (
                      <span className="text-[9px] font-mono px-2 py-0.5 rounded-full uppercase tracking-wide"
                        style={{ color: plan.color_hex, background: `${plan.color_hex}15`, border: `1px solid ${plan.color_hex}30` }}>
                        {plan.display_name}
                      </span>
                    )}
                    <span className="text-[10px] text-white/30 font-mono">
                      {p.session_count ?? 0} sessions
                    </span>
                    <button onClick={() => toggle(p.id, !!p.is_active)}
                      className="text-white/25 hover:text-white/70 transition-colors"
                      title={p.is_active ? "Deactivate" : "Activate"}>
                      {p.is_active
                        ? <CheckCircle2 className="w-4 h-4 text-green-400" />
                        : <XCircle className="w-4 h-4 text-white/25" />}
                    </button>
                  </div>
                </motion.div>
              );
            })}
            {filtered.length === 0 && (
              <p className="text-white/25 text-sm py-8 text-center">No partners found.</p>
            )}
          </div>
        )}

        {/* Create partner modal */}
        {showCreate && (
          <CreatePartnerModal
            plans={plans}
            token={accessToken ?? ""}
            onClose={() => setShowCreate(false)}
            onCreated={() => { setShowCreate(false); load(); }}
          />
        )}
      </div>
    </div>
  );
}

function CreatePartnerModal({ plans, token, onClose, onCreated }: {
  plans: Plan[]; token: string; onClose: () => void; onCreated: () => void;
}) {
  const [form, setForm] = useState({
    name: "", email: "", password: "", centre_name: "",
    phone: "", city: "", state: "", plan_id: "", notes: "",
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const set = (k: string, v: string) => setForm((p) => ({ ...p, [k]: v }));

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${apiBase()}/admin/partners`, {
        method: "POST",
        headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
        body: JSON.stringify(form),
      });
      if (!res.ok) {
        const d = await res.json();
        throw new Error(d.detail ?? "Failed");
      }
      onCreated();
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Error creating partner");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      <button className="absolute inset-0 bg-black/70 backdrop-blur-sm" onClick={onClose} />
      <motion.div
        className="relative w-full max-w-lg rounded-2xl p-6"
        style={{ background: "#0c0c18", border: "1px solid rgba(196,165,116,0.25)" }}
        initial={{ scale: 0.96, y: 12 }} animate={{ scale: 1, y: 0 }}
      >
        <h3 className="font-serif-display text-xl text-white mb-5">Create Partner Account</h3>
        <form onSubmit={submit} className="space-y-3">
          <div className="grid grid-cols-2 gap-3">
            {["name", "email", "password", "centre_name", "phone", "city"].map((k) => (
              <div key={k}>
                <label className="block text-[9px] font-mono uppercase tracking-widest text-white/30 mb-1">
                  {k.replace(/_/g, " ")}
                </label>
                <input
                  type={k === "password" ? "password" : k === "email" ? "email" : "text"}
                  required={["name", "email", "password"].includes(k)}
                  value={(form as Record<string, string>)[k]}
                  onChange={(e) => set(k, e.target.value)}
                  className="w-full h-9 rounded-lg px-3 text-sm text-white focus:outline-none transition-all"
                  style={{ background: "rgba(255,255,255,0.04)", border: "1px solid rgba(255,255,255,0.08)" }}
                />
              </div>
            ))}
          </div>
          <div>
            <label className="block text-[9px] font-mono uppercase tracking-widest text-white/30 mb-1">Plan</label>
            <select value={form.plan_id} onChange={(e) => set("plan_id", e.target.value)}
              className="w-full h-9 rounded-lg px-3 text-sm text-white/70 focus:outline-none"
              style={{ background: "rgba(255,255,255,0.04)", border: "1px solid rgba(255,255,255,0.08)", color: "rgba(255,255,255,0.7)" }}>
              <option value="" style={{ background: "#0d0d1a" }}>No plan</option>
              {plans.map((p) => <option key={p.id} value={p.id} style={{ background: "#0d0d1a" }}>{p.display_name}</option>)}
            </select>
          </div>
          {error && <p className="text-sm text-rose-400">{error}</p>}
          <div className="flex gap-3 pt-2">
            <button type="button" onClick={onClose}
              className="flex-1 py-2.5 rounded-xl text-sm text-white/40 border border-white/[0.08] hover:bg-white/[0.04] transition-colors">
              Cancel
            </button>
            <button type="submit" disabled={loading}
              className="flex-1 py-2.5 rounded-xl text-sm font-medium transition-all"
              style={{ background: "linear-gradient(135deg, #e8dcc8 0%, #c4a574 100%)", color: "#1a1510" }}>
              {loading ? "Creating…" : "Create Partner"}
            </button>
          </div>
        </form>
      </motion.div>
    </div>
  );
}
