"use client";

import { useEffect, useRef } from "react";
import { motion, useMotionValue, useSpring } from "framer-motion";

export function CursorGlow() {
  const mouseX = useMotionValue(0);
  const mouseY = useMotionValue(0);

  const springX = useSpring(mouseX, { stiffness: 300, damping: 30, mass: 0.5 });
  const springY = useSpring(mouseY, { stiffness: 300, damping: 30, mass: 0.5 });

  const outerX = useSpring(mouseX, { stiffness: 120, damping: 22, mass: 0.8 });
  const outerY = useSpring(mouseY, { stiffness: 120, damping: 22, mass: 0.8 });

  useEffect(() => {
    const handler = (e: MouseEvent) => {
      mouseX.set(e.clientX);
      mouseY.set(e.clientY);
    };
    window.addEventListener("mousemove", handler, { passive: true });
    return () => window.removeEventListener("mousemove", handler);
  }, [mouseX, mouseY]);

  return (
    <>
      {/* Outer diffuse glow */}
      <motion.div
        className="fixed pointer-events-none z-[9998] rounded-full mix-blend-screen"
        style={{
          x: outerX,
          y: outerY,
          translateX: "-50%",
          translateY: "-50%",
          width: 320,
          height: 320,
          background: "radial-gradient(circle, rgba(0, 212, 255, 0.04) 0%, transparent 70%)",
        }}
      />
      {/* Inner sharp cursor dot */}
      <motion.div
        className="fixed pointer-events-none z-[9999] rounded-full"
        style={{
          x: springX,
          y: springY,
          translateX: "-50%",
          translateY: "-50%",
          width: 6,
          height: 6,
          background: "rgba(0, 212, 255, 0.9)",
          boxShadow: "0 0 12px rgba(0, 212, 255, 0.8)",
        }}
      />
    </>
  );
}
