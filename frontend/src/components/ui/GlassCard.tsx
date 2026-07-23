"use client";

import { motion, HTMLMotionProps } from "framer-motion";
import { cn } from "@/lib/utils";

interface GlassCardProps extends Omit<HTMLMotionProps<"div">, "children"> {
  children: React.ReactNode;
  glow?: "none" | "cyan" | "violet" | "blue" | "amber";
  hover?: boolean;
  gradient?: boolean;
  padding?: "none" | "sm" | "md" | "lg";
  className?: string;
}

const GLOW_MAP = {
  none: "",
  cyan: "hover:shadow-[0_0_40px_-5px_rgba(0,212,255,0.25)] hover:border-[rgba(0,212,255,0.25)]",
  violet: "hover:shadow-[0_0_40px_-5px_rgba(139,92,246,0.25)] hover:border-[rgba(139,92,246,0.25)]",
  blue: "hover:shadow-[0_0_40px_-5px_rgba(59,130,246,0.25)] hover:border-[rgba(59,130,246,0.25)]",
  amber: "hover:shadow-[0_0_40px_-5px_rgba(245,158,11,0.25)] hover:border-[rgba(245,158,11,0.25)]",
};

export function GlassCard({
  children,
  glow = "none",
  hover = true,
  gradient = false,
  padding = "md",
  className,
  ...props
}: GlassCardProps) {
  return (
    <motion.div
      className={cn(
        "relative rounded-xl overflow-hidden transition-all duration-500",
        "glass border border-white/[0.07]",
        hover && "hover:bg-white/[0.06] cursor-default",
        glow !== "none" && GLOW_MAP[glow],
        padding === "sm" && "p-4",
        padding === "md" && "p-5",
        padding === "lg" && "p-7",
        padding === "none" && "",
        className
      )}
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
      {...props}
    >
      {/* Gradient top edge */}
      {gradient && (
        <div className="absolute top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-white/20 to-transparent" />
      )}
      {/* Holo shimmer on hover */}
      <div className="absolute inset-0 opacity-0 hover:opacity-100 transition-opacity duration-700 pointer-events-none holo-shimmer rounded-xl" />
      {children}
    </motion.div>
  );
}
