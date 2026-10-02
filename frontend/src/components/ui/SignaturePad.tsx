"use client";

import { useRef, useState, useEffect, useCallback, MouseEvent, TouchEvent } from "react";
import { Eraser, Check, PenTool } from "lucide-react";
import { cn } from "@/lib/utils";

interface SignaturePadProps {
  label: string;
  subtitle?: string;
  value?: string;
  onChange: (dataUrl: string | undefined) => void;
  className?: string;
  strokeColor?: string;
}

export function SignaturePad({
  label,
  subtitle,
  value,
  onChange,
  className,
  strokeColor = "#D4AF37",
}: SignaturePadProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [isDrawing, setIsDrawing] = useState(false);
  const [hasContent, setHasContent] = useState(Boolean(value));

  const getCanvasCoords = (e: MouseEvent<HTMLCanvasElement> | TouchEvent<HTMLCanvasElement>) => {
    const canvas = canvasRef.current;
    if (!canvas) return { x: 0, y: 0 };
    const rect = canvas.getBoundingClientRect();
    const scaleX = rect.width > 0 ? canvas.width / rect.width : 1;
    const scaleY = rect.height > 0 ? canvas.height / rect.height : 1;
    if ("touches" in e) {
      const touch = e.touches[0];
      if (!touch) return { x: 0, y: 0 };
      return {
        x: (touch.clientX - rect.left) * scaleX,
        y: (touch.clientY - rect.top) * scaleY,
      };
    }
    return {
      x: (e.clientX - rect.left) * scaleX,
      y: (e.clientY - rect.top) * scaleY,
    };
  };

  const startDrawing = (e: MouseEvent<HTMLCanvasElement> | TouchEvent<HTMLCanvasElement>) => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;
    setIsDrawing(true);
    const { x, y } = getCanvasCoords(e);
    ctx.beginPath();
    ctx.moveTo(x, y);
    ctx.strokeStyle = strokeColor;
    ctx.lineWidth = 2.2;
    ctx.lineCap = "round";
    ctx.lineJoin = "round";
  };

  const draw = (e: MouseEvent<HTMLCanvasElement> | TouchEvent<HTMLCanvasElement>) => {
    if (!isDrawing) return;
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;
    const { x, y } = getCanvasCoords(e);
    ctx.lineTo(x, y);
    ctx.stroke();
    setHasContent(true);
  };

  const stopDrawing = () => {
    if (!isDrawing) return;
    setIsDrawing(false);
    const canvas = canvasRef.current;
    if (!canvas) return;
    const dataUrl = canvas.toDataURL("image/png");
    onChange(dataUrl);
  };

  const clear = () => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    setHasContent(false);
    onChange(undefined);
  };

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    if (value && value.startsWith("data:image")) {
      const img = new Image();
      img.onload = () => {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
        setHasContent(true);
      };
      img.src = value;
    } else if (!value) {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      setHasContent(false);
    }
  }, [value]);

  return (
    <div className={cn("space-y-1.5", className)}>
      <div className="flex items-center justify-between">
        <div>
          <label className="text-[11px] font-medium text-white/60 flex items-center gap-1.5">
            <PenTool className="w-3 h-3 text-[#D4AF37]" />
            {label}
          </label>
          {subtitle && <p className="text-[9px] text-white/35 font-mono">{subtitle}</p>}
        </div>
        {hasContent && (
          <button
            type="button"
            onClick={clear}
            className="text-[10px] text-white/40 hover:text-rose-400 flex items-center gap-1 transition-colors"
          >
            <Eraser className="w-3 h-3" />
            Clear
          </button>
        )}
      </div>

      <div
        className="relative rounded-lg overflow-hidden border border-white/[0.08] bg-black/40 hover:border-white/[0.15] transition-colors"
        style={{ height: 96 }}
      >
        <canvas
          ref={canvasRef}
          width={460}
          height={96}
          onMouseDown={startDrawing}
          onMouseMove={draw}
          onMouseUp={stopDrawing}
          onMouseLeave={stopDrawing}
          onTouchStart={startDrawing}
          onTouchMove={draw}
          onTouchEnd={stopDrawing}
          className="w-full h-full cursor-crosshair touch-none"
        />

        {!hasContent && (
          <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
            <span className="text-[11px] text-white/20 font-mono tracking-widest uppercase">
              Draw Signature Here
            </span>
          </div>
        )}

        <div className="absolute bottom-2 left-4 right-4 border-b border-white/[0.08] pointer-events-none" />
      </div>
    </div>
  );
}
