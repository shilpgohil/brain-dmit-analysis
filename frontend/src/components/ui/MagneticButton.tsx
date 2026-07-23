"use client";

import { useRef, useState, MouseEvent } from "react";
import { motion, useSpring, useTransform } from "framer-motion";
import { cn } from "@/lib/utils";

interface MagneticButtonProps {
  children: React.ReactNode;
  variant?: "primary" | "secondary" | "ghost" | "danger";
  size?: "sm" | "md" | "lg";
  loading?: boolean;
  icon?: React.ReactNode;
  className?: string;
  onClick?: () => void;
  disabled?: boolean;
  strength?: number;
  href?: string;
  type?: "button" | "submit" | "reset";
}

export function MagneticButton({
  children,
  variant = "primary",
  size = "md",
  loading,
  icon,
  className,
  onClick,
  disabled,
  strength = 0.3,
  type = "button",
}: MagneticButtonProps) {
  const ref = useRef<HTMLButtonElement>(null);
  const [hovered, setHovered] = useState(false);

  const x = useSpring(0, { stiffness: 400, damping: 30 });
  const y = useSpring(0, { stiffness: 400, damping: 30 });

  const handleMouseMove = (e: MouseEvent<HTMLButtonElement>) => {
    if (!ref.current) return;
    const rect = ref.current.getBoundingClientRect();
    const centerX = rect.left + rect.width / 2;
    const centerY = rect.top + rect.height / 2;
    x.set((e.clientX - centerX) * strength);
    y.set((e.clientY - centerY) * strength);
  };

  const handleMouseLeave = () => {
    x.set(0);
    y.set(0);
    setHovered(false);
  };

  return (
    <motion.button
      ref={ref}
      type={type}
      disabled={disabled || loading}
      style={{ x, y }}
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
      onMouseEnter={() => setHovered(true)}
      onClick={onClick}
      className={cn(
        "relative inline-flex items-center justify-center gap-2 font-medium transition-colors duration-200 select-none focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-[rgba(196,165,116,0.5)] disabled:opacity-40 disabled:cursor-not-allowed rounded-lg overflow-hidden",
        size === "sm" && "h-8 px-3.5 text-xs",
        size === "md" && "h-10 px-5 text-sm",
        size === "lg" && "h-12 px-7 text-sm",
        variant === "primary" && [
          "text-[#0a0a12]",
          "bg-gradient-to-br from-[#e8dcc8] via-[#c4a574] to-[#9d8bb5]",
          "shadow-[0_0_24px_rgba(196,165,116,0.35)]",
          "hover:shadow-[0_0_32px_rgba(196,165,116,0.5)]",
        ],
        variant === "secondary" && [
          "glass border border-white/[0.10] text-white/80",
          "hover:bg-white/[0.08] hover:text-white",
        ],
        variant === "ghost" && "text-white/40 hover:text-white/70",
        variant === "danger" && [
          "bg-rose-950/40 text-rose-400 border border-rose-800/40",
          "hover:bg-rose-950/60",
        ],
        className
      )}
      whileTap={{ scale: 0.97 }}
    >
      {/* Primary shimmer overlay */}
      {variant === "primary" && (
        <motion.div
          className="absolute inset-0 bg-white/20 rounded-lg"
          initial={{ opacity: 0 }}
          animate={{ opacity: hovered ? 0.1 : 0 }}
          transition={{ duration: 0.2 }}
        />
      )}
      {loading ? (
        <svg className="animate-spin h-3.5 w-3.5" viewBox="0 0 24 24" fill="none">
          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
        </svg>
      ) : icon}
      {children}
    </motion.button>
  );
}
