"use client";

import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { apiBase } from "@/lib/api";
import { CheckCircle2, Loader2, Send, Fingerprint } from "lucide-react";

interface PartnerInfo {
  name: string; centre_name?: string; city?: string; state?: string; phone?: string;
}

const PURPOSES = ["Self", "Child", "Career Guidance", "Couple", "Corporate", "Other"] as const;

export default function PartnerIntakePage() {
  const { slug } = useParams<{ slug: string }>();
  const [partner, setPartner] = useState<PartnerInfo | null>(null);
  const [notFound, setNotFound] = useState(false);
  const [form, setForm] = useState({ subject_name: "", subject_age: "", subject_phone: "", purpose: "Self", note: "" });
  const [loading, setLoading] = useState(false);
  const [done, setDone] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch(`${apiBase()}/public/partner/${slug}/intake`)
      .then((r) => { if (!r.ok) throw new Error(); return r.json(); })
      .then(setPartner)
      .catch(() => setNotFound(true));
  }, [slug]);

  const set = (k: string, v: string) => setForm((p) => ({ ...p, [k]: v }));

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${apiBase()}/public/partner/${slug}/intake`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ...form,
          subject_age: form.subject_age ? parseInt(form.subject_age) : undefined,
          purpose: form.purpose.toLowerCase(),
        }),
      });
      if (!res.ok) throw new Error();
      setDone(true);
    } catch {
      setError("Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  if (notFound) return (
    <div className="min-h-screen flex items-center justify-center px-4">
      <div className="text-center">
        <Fingerprint className="w-10 h-10 mx-auto mb-4 text-white/20" />
        <p className="text-white/40 text-sm">This partner link is not active.</p>
      </div>
    </div>
  );

  if (!partner) return (
    <div className="min-h-screen flex items-center justify-center">
      <Loader2 className="w-6 h-6 animate-spin text-[#c4a574]" />
    </div>
  );

  if (done) return (
    <div className="min-h-screen flex items-center justify-center px-4">
      <motion.div className="text-center max-w-sm"
        initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }}>
        <CheckCircle2 className="w-12 h-12 mx-auto mb-4 text-green-400" />
        <h2 className="font-serif-display text-2xl text-white mb-2">Request Sent!</h2>
        <p className="text-white/40 text-sm leading-relaxed">
          <strong className="text-white/70">{partner.centre_name ?? partner.name}</strong> will
          contact you to schedule your DMIT session.
        </p>
      </motion.div>
    </div>
  );

  return (
    <div className="min-h-screen px-4 py-12"
      style={{ background: "radial-gradient(ellipse at 50% 0%, rgba(196,165,116,0.06) 0%, rgba(2,2,8,1) 60%)" }}>
      <div className="max-w-md mx-auto">
        {/* Partner branding */}
        <motion.div className="text-center mb-10"
          initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }}>
          <div className="w-16 h-16 rounded-2xl mx-auto mb-4 flex items-center justify-center"
            style={{ background: "rgba(196,165,116,0.1)", border: "1px solid rgba(196,165,116,0.2)" }}>
            <Fingerprint className="w-8 h-8 text-[#c4a574]" strokeWidth={1} />
          </div>
          <h1 className="font-serif-display text-2xl text-white">{partner.centre_name ?? partner.name}</h1>
          {partner.city && (
            <p className="text-white/30 text-sm mt-1">{partner.city}{partner.state ? `, ${partner.state}` : ""}</p>
          )}
          <p className="text-xs text-white/25 mt-1">DMIT Biometric Analysis Centre</p>
        </motion.div>

        {/* Form */}
        <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }}>
          <p className="text-[10px] font-mono uppercase tracking-widest text-[#c4a574] mb-4">
            Book a DMIT Analysis
          </p>
          <form onSubmit={submit} className="space-y-4">
            <div>
              <label className="block text-[10px] font-mono uppercase tracking-widest text-white/35 mb-1.5">Your Name</label>
              <input type="text" required value={form.subject_name} onChange={(e) => set("subject_name", e.target.value)}
                placeholder="Full name"
                className="w-full h-10 rounded-xl px-3 text-sm text-white placeholder:text-white/20 focus:outline-none transition-all"
                style={{ background: "rgba(255,255,255,0.04)", border: "1px solid rgba(255,255,255,0.08)" }}
              />
            </div>
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-[10px] font-mono uppercase tracking-widest text-white/35 mb-1.5">Age</label>
                <input type="number" value={form.subject_age} onChange={(e) => set("subject_age", e.target.value)}
                  placeholder="e.g. 12"
                  className="w-full h-10 rounded-xl px-3 text-sm text-white placeholder:text-white/20 focus:outline-none"
                  style={{ background: "rgba(255,255,255,0.04)", border: "1px solid rgba(255,255,255,0.08)" }}
                />
              </div>
              <div>
                <label className="block text-[10px] font-mono uppercase tracking-widest text-white/35 mb-1.5">Phone</label>
                <input type="tel" value={form.subject_phone} onChange={(e) => set("subject_phone", e.target.value)}
                  placeholder="Mobile number"
                  className="w-full h-10 rounded-xl px-3 text-sm text-white placeholder:text-white/20 focus:outline-none"
                  style={{ background: "rgba(255,255,255,0.04)", border: "1px solid rgba(255,255,255,0.08)" }}
                />
              </div>
            </div>
            <div>
              <label className="block text-[10px] font-mono uppercase tracking-widest text-white/35 mb-1.5">Purpose</label>
              <div className="flex flex-wrap gap-2">
                {PURPOSES.map((p) => (
                  <button key={p} type="button" onClick={() => set("purpose", p)}
                    className="px-3 py-1.5 rounded-lg text-[11px] font-mono transition-all"
                    style={form.purpose === p
                      ? { background: "rgba(196,165,116,0.14)", color: "#e8dcc8", border: "1px solid rgba(196,165,116,0.35)" }
                      : { color: "rgba(255,255,255,0.4)", border: "1px solid rgba(255,255,255,0.08)" }}>
                    {p}
                  </button>
                ))}
              </div>
            </div>
            <div>
              <label className="block text-[10px] font-mono uppercase tracking-widest text-white/35 mb-1.5">Additional Note</label>
              <textarea rows={2} value={form.note} onChange={(e) => set("note", e.target.value)}
                placeholder="Any specific concerns or questions…"
                className="w-full rounded-xl px-3 py-2 text-sm text-white placeholder:text-white/20 focus:outline-none resize-none"
                style={{ background: "rgba(255,255,255,0.04)", border: "1px solid rgba(255,255,255,0.08)" }}
              />
            </div>
            {error && <p className="text-sm text-rose-400">{error}</p>}
            <button type="submit" disabled={loading}
              className="w-full h-11 rounded-xl font-medium text-sm flex items-center justify-center gap-2 transition-all"
              style={{
                background: "linear-gradient(135deg, #e8dcc8 0%, #c4a574 45%, #9a7b4f 100%)",
                color: "#1a1510", opacity: loading ? 0.7 : 1,
              }}>
              {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4" />}
              {loading ? "Sending…" : "Request DMIT Analysis"}
            </button>
          </form>
        </motion.div>
      </div>
    </div>
  );
}
