"use client";

import { useEffect, useRef } from "react";

interface FingerprintFieldProps {
  opacity?: number;
  animated?: boolean;
  color?: string;
  className?: string;
}

export function FingerprintField({
  opacity = 0.08,
  animated = true,
  color = "0, 212, 255",
  className = "",
}: FingerprintFieldProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const frameRef = useRef<number>(0);
  const timeRef = useRef(0);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const resize = () => {
      canvas.width = canvas.offsetWidth * window.devicePixelRatio;
      canvas.height = canvas.offsetHeight * window.devicePixelRatio;
      ctx.scale(window.devicePixelRatio, window.devicePixelRatio);
    };

    resize();
    window.addEventListener("resize", resize);

    // Draw procedural concentric ridge patterns (fingerprint-inspired)
    const draw = (t: number) => {
      const w = canvas.offsetWidth;
      const h = canvas.offsetHeight;
      ctx.clearRect(0, 0, w, h);

      const cx = w * 0.5;
      const cy = h * 0.45;
      const maxR = Math.max(w, h) * 0.7;
      const ridgeSpacing = 18;
      const waveAmp = animated ? 6 * Math.sin(t * 0.0003) : 0;

      ctx.lineWidth = 0.6;

      // Draw loop-style ridges (fingerprint whorls/loops)
      for (let r = ridgeSpacing; r < maxR; r += ridgeSpacing) {
        const phase = animated ? (r * 0.04 + t * 0.0008) : r * 0.04;
        ctx.beginPath();

        for (let a = 0; a <= Math.PI * 2; a += 0.02) {
          // Distort the radius to create loop-like patterns
          const distortion =
            waveAmp * Math.sin(a * 3 + phase) +
            (waveAmp * 0.5) * Math.cos(a * 5 - phase * 1.3) +
            (waveAmp * 0.3) * Math.sin(a * 7 + phase * 0.7);

          const rx = (r + distortion) * (1 + 0.15 * Math.cos(a * 2));
          const ry = r + distortion;

          const x = cx + rx * Math.cos(a);
          const y = cy + ry * Math.sin(a) * 0.85 + (r * 0.1 * Math.sin(a + phase * 0.5));

          if (a === 0) ctx.moveTo(x, y);
          else ctx.lineTo(x, y);
        }
        ctx.closePath();

        // Fade out toward edges
        const alpha = (opacity * (1 - r / maxR)) * (r > ridgeSpacing * 2 ? 1 : r / (ridgeSpacing * 2));
        ctx.strokeStyle = `rgba(${color}, ${alpha})`;
        ctx.stroke();
      }

      // Delta points (triangle triradius markers)
      const deltas = [
        { x: cx - maxR * 0.22, y: cy + maxR * 0.18 },
        { x: cx + maxR * 0.22, y: cy + maxR * 0.18 },
      ];
      for (const d of deltas) {
        ctx.beginPath();
        ctx.arc(d.x, d.y, 3, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(${color}, ${opacity * 1.5})`;
        ctx.fill();
      }

      // Core point
      ctx.beginPath();
      ctx.arc(cx, cy - maxR * 0.05, 4, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(${color}, ${opacity * 2})`;
      ctx.fill();
    };

    const tick = (time: number) => {
      timeRef.current = time;
      draw(time);
      if (animated) frameRef.current = requestAnimationFrame(tick);
    };

    if (animated) {
      frameRef.current = requestAnimationFrame(tick);
    } else {
      draw(0);
    }

    return () => {
      window.removeEventListener("resize", resize);
      cancelAnimationFrame(frameRef.current);
    };
  }, [opacity, animated, color]);

  return (
    <canvas
      ref={canvasRef}
      className={`absolute inset-0 w-full h-full pointer-events-none ${className}`}
      style={{ mixBlendMode: "screen" }}
    />
  );
}
