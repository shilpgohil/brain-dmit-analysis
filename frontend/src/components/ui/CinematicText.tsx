"use client";

import { motion } from "framer-motion";

interface CinematicTextProps {
  text: string;
  className?: string;
  delay?: number;
  duration?: number;
  stagger?: number;
  by?: "word" | "char" | "line";
}

export function CinematicText({
  text,
  className = "",
  delay = 0,
  duration = 0.6,
  stagger = 0.04,
  by = "word",
}: CinematicTextProps) {
  const units = by === "char" ? text.split("") : text.split(" ");

  return (
    <span className={`inline-flex flex-wrap gap-x-[0.25em] ${className}`} aria-label={text}>
      {units.map((unit, i) => (
        <motion.span
          key={i}
          className="inline-block overflow-hidden"
          initial={{ opacity: 0, y: "110%", rotateX: -20 }}
          animate={{ opacity: 1, y: 0, rotateX: 0 }}
          transition={{
            duration,
            delay: delay + i * stagger,
            ease: [0.16, 1, 0.3, 1],
          }}
          style={{ transformOrigin: "bottom center" }}
        >
          {unit === " " ? "\u00A0" : unit}
        </motion.span>
      ))}
    </span>
  );
}

export function RevealBlock({
  children,
  delay = 0,
  className = "",
}: {
  children: React.ReactNode;
  delay?: number;
  className?: string;
}) {
  return (
    <motion.div
      className={`overflow-hidden ${className}`}
      initial={{ opacity: 0, y: 24 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.7, delay, ease: [0.16, 1, 0.3, 1] }}
    >
      {children}
    </motion.div>
  );
}
