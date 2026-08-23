"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { CheckCircle2, Send } from "lucide-react";
import { apiBase } from "@/lib/api";

const PLANS = ["Basic", "Standard", "Premium", "Enterprise"];

export default function RequestAccessPage() {
  const [form, setForm] = useState({
    name: "", email: "", phone: "", centre_name: "",
    city: "", state: "", plan_interest: "Standard", message: "",
  });
  const [loading, setLoading] = useState(false);
  const [done, setDone] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const set = (k: string, v: string) => setForm((p) => ({ ...p, [k]: v }));

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${apiBase()}/public/request-access`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });
      if (!res.ok) throw new Error("Submission failed");
      setDone(true);
    } catch {
      setError("Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  if (done) {
    return (
      <div className="min-h-screen flex items-center justify-center px-4">
        <motion.div className="text-center max-w-md"
          initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }}>
          <CheckCircle2 className="w-12 h-12 mx-auto mb-4 text-green-400" />
          <h2 className="font-serif-display text-2xl text-white mb-2">Request Received</h2>
          <p className="text-white/40 text-sm leading-relaxed">
            Thank you! Our team will review your application and reach out within 24 hours
            with your login credentials.
          </p>
          <a href="/login" className="inline-block mt-6 text-[#c4a574] text-sm hover:underline">
            Already have an account? Sign in
          </a>
        </motion.div>
      </div>
    );
  }

  return (
    <div className="min-h-screen px-4 py-16"
      style={{ background: "radial-gradient(ellipse at 50% 0%, rgba(196,165,116,0.06) 0%, rgba(2,2,8,1) 60%)" }}>
      <div className="max-w-xl mx-auto">
        <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }} className="mb-10">
          <p className="text-[10px] font-mono uppercase tracking-widest text-[#c4a574] mb-2">
            Partnership Programme
          </p>
          <h1 className="font-serif-display text-3xl text-white mb-2">Request Platform Access</h1>
          <p className="text-white/35 text-sm leading-relaxed">
            Tell us about your practice. Our admin team reviews every application and
            sends your credentials within 24 hours.
          </p>
        </motion.div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <Field label="Your Name" value={form.name} onChange={(v) => set("name", v)} required />
            <Field label="Email" type="email" value={form.email} onChange={(v) => set("email", v)} required />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <Field label="Phone" value={form.phone} onChange={(v) => set("phone", v)} />
            <Field label="Centre / Practice Name" value={form.centre_name} onChange={(v) => set("centre_name", v)} />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <Field label="City" value={form.city} onChange={(v) => set("city", v)} />
            <Field label="State" value={form.state} onChange={(v) => set("state", v)} />
          </div>
          <div>
            <label className="block text-[10px] font-mono uppercase tracking-widest text-white/35 mb-2">
              Interested Plan
            </label>
            <div className="flex flex-wrap gap-2">
              {PLANS.map((p) => (
                <button key={p} type="button" onClick={() => set("plan_interest", p)}
                  className="px-3 py-1.5 rounded-lg text-[11px] font-mono transition-all"
                  style={form.plan_interest === p
                    ? { background: "rgba(196,165,116,0.14)", color: "#e8dcc8", border: "1px solid rgba(196,165,116,0.35)" }
                    : { color: "rgba(255,255,255,0.4)", border: "1px solid rgba(255,255,255,0.08)" }}>
                  {p}
                </button>
              ))}
            </div>
          </div>
          <div>
            <label className="block text-[10px] font-mono uppercase tracking-widest text-white/35 mb-2">
              Message (optional)
            </label>
            <textarea rows={3} value={form.message}
              onChange={(e) => set("message", e.target.value)}
              placeholder="Tell us about your practice and how you plan to use DMIT..."
              className="w-full rounded-xl px-3 py-2.5 text-sm text-white placeholder:text-white/20 focus:outline-none resize-none transition-all"
              style={{ background: "rgba(255,255,255,0.04)", border: "1px solid rgba(255,255,255,0.08)" }}
              onFocus={(e) => (e.target.style.borderColor = "rgba(196,165,116,0.5)")}
              onBlur={(e) => (e.target.style.borderColor = "rgba(255,255,255,0.08)")}
            />
          </div>
          {error && <p className="text-sm text-rose-400">{error}</p>}
          <button type="submit" disabled={loading}
            className="w-full h-11 rounded-xl font-medium text-sm flex items-center justify-center gap-2 transition-all"
            style={{
              background: "linear-gradient(135deg, #e8dcc8 0%, #c4a574 45%, #9a7b4f 100%)",
              color: "#1a1510", opacity: loading ? 0.7 : 1,
            }}>
            <Send className="w-4 h-4" />
            {loading ? "Submitting..." : "Submit Request"}
          </button>
          <p className="text-center text-xs text-white/25">
            Already have an account?{" "}
            <a href="/login" className="text-[#c4a574] hover:underline">Sign in</a>
          </p>
        </form>
      </div>
    </div>
  );
}

function Field({ label, value, onChange, type = "text", required = false }: {
  label: string; value: string; onChange: (v: string) => void;
  type?: string; required?: boolean;
}) {
  return (
    <div>
      <label className="block text-[10px] font-mono uppercase tracking-widest text-white/35 mb-2">{label}</label>
      <input type={type} value={value} required={required}
        onChange={(e) => onChange(e.target.value)}
        className="w-full h-10 rounded-lg px-3 text-sm text-white placeholder:text-white/15 focus:outline-none transition-all"
        style={{ background: "rgba(255,255,255,0.04)", border: "1px solid rgba(255,255,255,0.08)" }}
        onFocus={(e) => (e.target.style.borderColor = "rgba(196,165,116,0.5)")}
        onBlur={(e) => (e.target.style.borderColor = "rgba(255,255,255,0.08)")}
      />
    </div>
  );
}
