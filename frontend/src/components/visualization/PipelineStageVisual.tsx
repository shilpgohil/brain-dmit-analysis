"use client";

import { motion } from "framer-motion";

export type PipelineStageId =
  | "capture"
  | "extraction"
  | "mapping"
  | "profile"
  | "report";

interface PipelineStageVisualProps {
  stage: PipelineStageId;
  index: number;
  accent: string;
}

/** Rich stage visuals — photographic textures + scientific SVG overlays */
export function PipelineStageVisual({ stage, index, accent }: PipelineStageVisualProps) {
  return (
    <div className="relative w-full aspect-[4/3] rounded-lg overflow-hidden mb-4 border border-white/[0.06]">
      {/* Base photographic layer where available */}
      {(stage === "capture" || stage === "extraction") && (
        // eslint-disable-next-line @next/next/no-img-element
        <img
          src={stage === "capture" ? "/images/pipeline-capture.bmp" : "/images/pipeline-extract.bmp"}
          alt=""
          className="absolute inset-0 w-full h-full object-cover opacity-50"
          style={{
            filter: "contrast(1.2) grayscale(100%) brightness(0.7)",
          }}
        />
      )}

      {/* Stage-specific illustrated overlay */}
      <div className="absolute inset-0">
        {stage === "capture" && <CaptureOverlay accent={accent} />}
        {stage === "extraction" && <ExtractionOverlay accent={accent} />}
        {stage === "mapping" && <MappingOverlay accent={accent} />}
        {stage === "profile" && <ProfileOverlay accent={accent} />}
        {stage === "report" && <ReportOverlay accent={accent} />}
      </div>

      {/* Gradient fade */}
      <div
        className="absolute inset-0 pointer-events-none"
        style={{
          background: `linear-gradient(to top, rgba(2,2,8,0.85) 0%, transparent 50%), linear-gradient(135deg, ${accent}08 0%, transparent 60%)`,
        }}
      />

      {/* Step number watermark */}
      <span
        className="absolute top-2 right-3 font-mono text-[10px] opacity-40"
        style={{ color: accent }}
      >
        {String(index + 1).padStart(2, "0")}
      </span>
    </div>
  );
}

function CaptureOverlay({ accent }: { accent: string }) {
  return (
    <svg className="absolute inset-0 w-full h-full" viewBox="0 0 200 150" preserveAspectRatio="xMidYMid slice">
      <defs>
        <radialGradient id="capGlow" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stopColor={accent} stopOpacity="0.25" />
          <stop offset="100%" stopColor={accent} stopOpacity="0" />
        </radialGradient>
      </defs>
      <rect width="200" height="150" fill="url(#capGlow)" />
      {/* Scan corners */}
      <path d="M20 20 H50 M20 20 V50" stroke={accent} strokeWidth="1" fill="none" opacity="0.6" />
      <path d="M180 20 H150 M180 20 V50" stroke={accent} strokeWidth="1" fill="none" opacity="0.6" />
      <path d="M20 130 H50 M20 130 V100" stroke={accent} strokeWidth="1" fill="none" opacity="0.6" />
      <path d="M180 130 H150 M180 130 V100" stroke={accent} strokeWidth="1" fill="none" opacity="0.6" />
      <motion.line
        x1="0" y1="75" x2="200" y2="75"
        stroke="rgba(255,255,255,0.8)"
        strokeWidth="0.5"
        animate={{ y1: [30, 120, 30], y2: [30, 120, 30] }}
        transition={{ duration: 3, repeat: Infinity, ease: "easeInOut" }}
      />
    </svg>
  );
}

function ExtractionOverlay({ accent }: { accent: string }) {
  return (
    <svg className="absolute inset-0 w-full h-full opacity-80" viewBox="0 0 200 150">
      {/* Minutiae points */}
      {Array.from({ length: 24 }).map((_, i) => {
        const x = 30 + (i % 6) * 28 + (i % 3) * 4;
        const y = 25 + Math.floor(i / 6) * 28;
        return (
          <circle key={i} cx={x} cy={y} r="1.2" fill={accent} opacity={0.4 + (i % 5) * 0.1} />
        );
      })}
      {/* Ridge flow lines */}
      {Array.from({ length: 8 }).map((_, i) => (
        <path
          key={i}
          d={`M ${15 + i * 3} ${20 + i * 8} Q ${80 + i * 5} ${40 + i * 6} ${185 - i * 2} ${25 + i * 12}`}
          stroke={accent}
          strokeWidth="0.4"
          fill="none"
          opacity={0.25}
        />
      ))}
      <text x="100" y="140" textAnchor="middle" fill="rgba(255,255,255,0.5)" fontSize="8" fontFamily="monospace">
        85 metrics
      </text>
    </svg>
  );
}

function MappingOverlay({ accent }: { accent: string }) {
  return (
    <svg className="absolute inset-0 w-full h-full" viewBox="0 0 200 150">
      <defs>
        <linearGradient id="brainGrad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor={accent} stopOpacity="0.3" />
          <stop offset="100%" stopColor="#8b5cf6" stopOpacity="0.1" />
        </linearGradient>
      </defs>
      {/* Stylized brain silhouette */}
      <path
        d="M100 25 C70 25 55 45 55 70 C45 75 40 90 45 105 C50 120 65 128 80 125 C85 140 95 145 100 145 C105 145 115 140 120 125 C135 128 150 120 155 105 C160 90 155 75 145 70 C145 45 130 25 100 25 Z"
        fill="url(#brainGrad)"
        stroke={accent}
        strokeWidth="0.8"
        opacity="0.9"
      />
      {/* Lobe connection lines */}
      {[
        [100, 55, 60, 30],
        [100, 55, 140, 30],
        [100, 75, 40, 100],
        [100, 75, 160, 100],
        [100, 95, 70, 130],
      ].map(([x1, y1, x2, y2], i) => (
        <line key={i} x1={x1} y1={y1} x2={x2} y2={y2} stroke={accent} strokeWidth="0.4" opacity="0.35" />
      ))}
      {/* Finger nodes */}
      {[
        [60, 30], [140, 30], [40, 100], [160, 100], [70, 130],
      ].map(([cx, cy], i) => (
        <g key={i}>
          <circle cx={cx} cy={cy} r="4" fill={accent} opacity="0.5" />
          <circle cx={cx} cy={cy} r="7" stroke={accent} strokeWidth="0.4" fill="none" opacity="0.3" />
        </g>
      ))}
    </svg>
  );
}

function ProfileOverlay({ accent }: { accent: string }) {
  return (
    <svg className="absolute inset-0 w-full h-full" viewBox="0 0 200 150">
      {/* Radar web */}
      <g transform="translate(100, 75)" opacity="0.85">
        {[0.35, 0.55, 0.75, 1].map((r, i) => (
          <circle key={i} r={55 * r} fill="none" stroke={accent} strokeWidth="0.4" opacity={0.2 + i * 0.1} />
        ))}
        {Array.from({ length: 9 }).map((_, i) => {
          const a = (i * Math.PI * 2) / 9 - Math.PI / 2;
          return (
            <line
              key={i}
              x1={0}
              y1={0}
              x2={Math.cos(a) * 55}
              y2={Math.sin(a) * 55}
              stroke={accent}
              strokeWidth="0.3"
              opacity="0.25"
            />
          );
        })}
        <motion.polygon
          points="0,-40 35,-12 28,32 -8,38 -32,8"
          fill={`${accent}22`}
          stroke={accent}
          strokeWidth="1"
          animate={{ scale: [1, 1.05, 1] }}
          transition={{ duration: 4, repeat: Infinity }}
        />
      </g>
    </svg>
  );
}

function ReportOverlay({ accent }: { accent: string }) {
  return (
    <svg className="absolute inset-0 w-full h-full" viewBox="0 0 200 150">
      {/* Document stack */}
      <rect x="55" y="28" width="90" height="110" rx="3" fill="rgba(255,255,255,0.04)" stroke="rgba(255,255,255,0.15)" strokeWidth="0.6" />
      <rect x="62" y="22" width="90" height="110" rx="3" fill="rgba(255,255,255,0.02)" stroke="rgba(255,255,255,0.08)" strokeWidth="0.5" />
      {/* Content lines */}
      {Array.from({ length: 6 }).map((_, i) => (
        <rect
          key={i}
          x="72"
          y={45 + i * 14}
          width={60 - (i % 3) * 12}
          height="4"
          rx="1"
          fill={i === 0 ? accent : "rgba(255,255,255,0.12)"}
          opacity={0.5 + (6 - i) * 0.08}
        />
      ))}
      {/* Chart mini */}
      <rect x="72" y="115" width="70" height="18" fill="rgba(0,0,0,0.3)" rx="2" />
      {[12, 18, 10, 22, 16].map((h, i) => (
        <rect key={i} x={76 + i * 12} y={130 - h} width="6" height={h} fill={accent} opacity="0.5" />
      ))}
    </svg>
  );
}
