"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import Image from "next/image";
import { loginAdmin, loginPartner } from "@/lib/auth-api";
import { useAuthStore } from "@/store/authStore";
import { FingerprintField } from "@/components/effects/FingerprintField";
import { Eye, EyeOff, Lock, Mail, Loader2, ArrowRight, Shield, Zap, BarChart3 } from "lucide-react";
import { cn } from "@/lib/utils";

const FEATURES = [
  { icon: Zap, text: "46-module extension analysis from real ridge biometrics" },
  { icon: BarChart3, text: "10-Quotient intelligence profile (IQ, EQ, CQ and 7 more)" },
  { icon: Shield, text: "Science-backed — grounded in dermatoglyphics research" },
];

export default function LoginPage() {
  const router = useRouter();
  const { user, scope, isLoading } = useAuthStore();

  const [email, setEmail] = useState("");
  const [password, setPass] = useState("");
  const [showPass, setShow] = useState(false);
  const [mode, setMode] = useState<"partner" | "admin">("partner");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Redirect already-logged-in users; show spinner during auth boot
  useEffect(() => {
    if (isLoading) return;
    if (user && scope === "admin") router.replace("/admin");
    else if (user && scope === "partner") router.replace("/sessions");
  }, [user, scope, isLoading, router]);

  // Show spinner while auth state is being restored from refresh cookie
  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="w-8 h-8 rounded-full border-2 border-[#c4a574] border-t-transparent animate-spin" />
      </div>
    );
  }

  // Already authenticated — render nothing while redirect fires
  if (user) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (submitting) return;
    setError(null);
    setSubmitting(true);
    try {
      if (mode === "admin") {
        await loginAdmin(email, password);
        router.push("/admin");
      } else {
        await loginPartner(email, password);
        router.push("/sessions");
      }
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Invalid credentials. Please try again.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen flex">
      {/* ── LEFT PANEL — brand story ─────────────────────────────────── */}
      <div
        className="hidden lg:flex lg:w-[52%] xl:w-[55%] flex-col justify-between p-14 relative overflow-hidden"
        style={{
          background:
            "linear-gradient(135deg, rgba(8,8,22,1) 0%, rgba(4,4,14,1) 100%)",
          borderRight: "1px solid rgba(196,165,116,0.10)",
        }}
      >
        {/* Animated fingerprint background */}
        <div className="absolute inset-0 opacity-[0.07]">
          <FingerprintField animated color="196, 165, 116" opacity={1} />
        </div>

        {/* Radial glow */}
        <div
          className="absolute inset-0 pointer-events-none"
          style={{
            background:
              "radial-gradient(ellipse 70% 60% at 30% 50%, rgba(196,165,116,0.06) 0%, transparent 65%)",
          }}
        />

        <div className="relative z-10">
          {/* Logo */}
          <div className="flex items-center gap-3">
            <div
              className="w-10 h-10 rounded-full overflow-hidden flex-shrink-0"
              style={{ boxShadow: "0 0 20px rgba(196,165,116,0.25)" }}
            >
              <Image
                src="/images/logo.png"
                alt="DMIT"
                width={40}
                height={40}
                className="object-contain"
                priority
              />
            </div>
            <div>
              <p className="font-serif-display text-white text-lg leading-none">DMIT Platform</p>
              <p className="text-[9px] font-mono uppercase tracking-[0.22em] text-white/30 mt-0.5">
                Biometric Intelligence
              </p>
            </div>
          </div>
        </div>

        {/* Hero text */}
        <div className="relative z-10">
          <motion.div
            initial={{ opacity: 0, y: 24 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
          >
            <p className="text-[10px] font-mono uppercase tracking-[0.22em] mb-4"
              style={{ color: "#c4a574" }}>
              Dermatoglyphics · AI · Intelligence
            </p>
            <h1 className="font-serif-display text-4xl xl:text-5xl text-white leading-[1.1] mb-6">
              Unlock potential<br />
              <span style={{ color: "#c4a574" }}>written in ridges.</span>
            </h1>
            <p className="text-white/40 text-sm leading-relaxed max-w-sm">
              The most advanced DMIT platform — from fingerprint capture to a
              95-page personalised intelligence report, powered by 46 biometric
              analysis modules.
            </p>
          </motion.div>

          {/* Feature list */}
          <motion.div
            className="mt-10 space-y-4"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.3, duration: 0.6 }}
          >
            {FEATURES.map(({ icon: Icon, text }, i) => (
              <motion.div
                key={i}
                className="flex items-start gap-3"
                initial={{ opacity: 0, x: -12 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.4 + i * 0.1 }}
              >
                <div
                  className="w-7 h-7 rounded-lg flex items-center justify-center flex-shrink-0 mt-0.5"
                  style={{ background: "rgba(196,165,116,0.1)", border: "1px solid rgba(196,165,116,0.2)" }}
                >
                  <Icon className="w-3.5 h-3.5" style={{ color: "#c4a574" }} />
                </div>
                <p className="text-sm text-white/50 leading-snug">{text}</p>
              </motion.div>
            ))}
          </motion.div>
        </div>

        {/* Bottom quote */}
        <div className="relative z-10">
          <div
            className="h-px mb-6"
            style={{ background: "linear-gradient(90deg, rgba(196,165,116,0.3), transparent)" }}
          />
          <p className="text-xs text-white/20 leading-relaxed max-w-sm">
            "Fingerprints begin forming at week 13 of gestation — the same window as
            the cerebral cortex. Ridge patterns are a biometric map of the developing brain."
          </p>
          <p className="text-[10px] text-white/15 font-mono mt-2">
            — Dermatoglyphics Research, University of Malaya
          </p>
        </div>
      </div>

      {/* ── RIGHT PANEL — login form ─────────────────────────────────── */}
      <div className="flex-1 flex flex-col items-center justify-center px-6 py-12 relative">
        {/* Mobile logo */}
        <div className="lg:hidden flex items-center gap-3 mb-10">
          <div className="w-9 h-9 rounded-full overflow-hidden">
            <Image src="/images/logo.png" alt="DMIT" width={36} height={36} className="object-contain" />
          </div>
          <p className="font-serif-display text-white text-xl">DMIT Platform</p>
        </div>

        <motion.div
          className="w-full max-w-md"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
        >
          {/* Header */}
          <div className="mb-8">
            <h2 className="font-serif-display text-3xl text-white mb-1.5">Welcome back</h2>
            <p className="text-white/35 text-sm">Sign in to your DMIT console</p>
          </div>

          {/* Mode toggle */}
          <div
            className="flex rounded-xl p-1 mb-8 gap-1"
            style={{ background: "rgba(255,255,255,0.03)", border: "1px solid rgba(255,255,255,0.07)" }}
          >
            {(["partner", "admin"] as const).map((m) => (
              <button
                key={m}
                type="button"
                onClick={() => { setMode(m); setError(null); }}
                className={cn(
                  "flex-1 py-2.5 rounded-lg text-xs font-mono uppercase tracking-widest transition-all",
                  mode === m ? "text-[#1a1510] font-semibold" : "text-white/30 hover:text-white/55"
                )}
                style={
                  mode === m
                    ? { background: "linear-gradient(135deg, #e8dcc8 0%, #c4a574 45%, #9a7b4f 100%)" }
                    : undefined
                }
              >
                {m === "partner" ? "Partner" : "Admin"}
              </button>
            ))}
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-[10px] font-mono uppercase tracking-widest text-white/30 mb-2">
                Email address
              </label>
              <div className="relative">
                <Mail className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-white/20 pointer-events-none" />
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="you@example.com"
                  className="w-full h-12 pl-11 pr-4 rounded-xl text-sm text-white placeholder:text-white/15 focus:outline-none transition-all"
                  style={{ background: "rgba(255,255,255,0.04)", border: "1px solid rgba(255,255,255,0.08)" }}
                  onFocus={(e) => (e.target.style.borderColor = "rgba(196,165,116,0.5)")}
                  onBlur={(e) => (e.target.style.borderColor = "rgba(255,255,255,0.08)")}
                />
              </div>
            </div>

            <div>
              <label className="block text-[10px] font-mono uppercase tracking-widest text-white/30 mb-2">
                Password
              </label>
              <div className="relative">
                <Lock className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-white/20 pointer-events-none" />
                <input
                  type={showPass ? "text" : "password"}
                  required
                  value={password}
                  onChange={(e) => setPass(e.target.value)}
                  placeholder="••••••••"
                  className="w-full h-12 pl-11 pr-11 rounded-xl text-sm text-white placeholder:text-white/15 focus:outline-none transition-all"
                  style={{ background: "rgba(255,255,255,0.04)", border: "1px solid rgba(255,255,255,0.08)" }}
                  onFocus={(e) => (e.target.style.borderColor = "rgba(196,165,116,0.5)")}
                  onBlur={(e) => (e.target.style.borderColor = "rgba(255,255,255,0.08)")}
                />
                <button
                  type="button"
                  onClick={() => setShow(!showPass)}
                  className="absolute right-3.5 top-1/2 -translate-y-1/2 text-white/20 hover:text-white/60 transition-colors"
                >
                  {showPass ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                </button>
              </div>
            </div>

            <AnimatePresence>
              {error && (
                <motion.div
                  className="px-4 py-3 rounded-xl text-sm text-rose-400"
                  style={{ background: "rgba(244,63,94,0.07)", border: "1px solid rgba(244,63,94,0.2)" }}
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: "auto" }}
                  exit={{ opacity: 0, height: 0 }}
                >
                  {error}
                </motion.div>
              )}
            </AnimatePresence>

            <button
              type="submit"
              disabled={submitting}
              className="w-full h-12 rounded-xl font-medium text-sm flex items-center justify-center gap-2 transition-all mt-2"
              style={{
                background: "linear-gradient(135deg, #e8dcc8 0%, #c4a574 45%, #9a7b4f 100%)",
                color: "#1a1510",
                boxShadow: submitting ? "none" : "0 4px 24px rgba(196,165,116,0.25)",
                opacity: submitting ? 0.7 : 1,
              }}
            >
              {submitting ? (
                <Loader2 className="w-4 h-4 animate-spin" />
              ) : (
                <>
                  Sign In
                  <ArrowRight className="w-4 h-4" />
                </>
              )}
            </button>
          </form>

          {/* Footer */}
          <div className="mt-8 pt-6" style={{ borderTop: "1px solid rgba(255,255,255,0.06)" }}>
            <p className="text-xs text-white/25 text-center">
              New to the platform?{" "}
              <a href="/request-access" className="text-[#c4a574] hover:text-[#e8dcc8] transition-colors">
                Request access
              </a>
            </p>
          </div>
        </motion.div>
      </div>
    </div>
  );
}
