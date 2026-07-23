"use client";

import { useState, useCallback, useRef } from "react";
import { cn } from "@/lib/utils";
import { Upload, X, Fingerprint, AlertCircle } from "lucide-react";

interface UploadedFile {
  file: File;
  preview?: string;
  fingerLabel: string;
  id: string;
}

interface UploadZoneProps {
  onFilesChange: (files: File[]) => void;
  maxFiles?: number;
  className?: string;
}

const FINGER_ORDER = [
  { id: "R1", label: "Right Thumb" },
  { id: "R2", label: "Right Index" },
  { id: "R3", label: "Right Middle" },
  { id: "R4", label: "Right Ring" },
  { id: "R5", label: "Right Little" },
  { id: "L1", label: "Left Thumb" },
  { id: "L2", label: "Left Index" },
  { id: "L3", label: "Left Middle" },
  { id: "L4", label: "Left Ring" },
  { id: "L5", label: "Left Little" },
];

export function UploadZone({ onFilesChange, maxFiles = 10, className }: UploadZoneProps) {
  const [files, setFiles] = useState<UploadedFile[]>([]);
  const [dragging, setDragging] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  const addFiles = useCallback(
    (incoming: FileList | File[]) => {
      const arr = Array.from(incoming);
      const accepted = arr.filter(
        (f) => f.type.startsWith("image/") || f.name.endsWith(".bmp")
      );

      const newEntries: UploadedFile[] = accepted.map((file, i) => {
        const assigned = FINGER_ORDER[files.length + i] ?? { id: "UNK", label: "Unknown" };
        const preview = URL.createObjectURL(file);
        return {
          file,
          preview,
          fingerLabel: assigned.label,
          id: assigned.id,
        };
      });

      const merged = [...files, ...newEntries].slice(0, maxFiles);
      setFiles(merged);
      onFilesChange(merged.map((f) => f.file));
    },
    [files, maxFiles, onFilesChange]
  );

  const removeFile = (index: number) => {
    const next = files.filter((_, i) => i !== index);
    // Reassign finger labels
    const reassigned = next.map((f, i) => ({
      ...f,
      fingerLabel: FINGER_ORDER[i]?.label ?? "Unknown",
      id: FINGER_ORDER[i]?.id ?? "UNK",
    }));
    setFiles(reassigned);
    onFilesChange(reassigned.map((f) => f.file));
  };

  const onDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setDragging(false);
    if (e.dataTransfer.files) addFiles(e.dataTransfer.files);
  };

  return (
    <div className={cn("space-y-4", className)}>
      {/* Drop zone */}
      <div
        onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
        onDragLeave={() => setDragging(false)}
        onDrop={onDrop}
        onClick={() => inputRef.current?.click()}
        className={cn(
          "relative border-2 border-dashed rounded-lg cursor-pointer transition-all duration-200 flex flex-col items-center justify-center py-10 px-6 text-center",
          dragging
            ? "border-blue-500 bg-blue-950/20"
            : "border-slate-700 hover:border-slate-600 bg-slate-900/50 hover:bg-slate-900"
        )}
      >
        <input
          ref={inputRef}
          type="file"
          accept="image/*,.bmp"
          multiple
          className="hidden"
          onChange={(e) => e.target.files && addFiles(e.target.files)}
        />
        <div className="w-10 h-10 rounded-full bg-slate-800 flex items-center justify-center mb-3">
          <Upload className="w-5 h-5 text-slate-400" />
        </div>
        <p className="text-sm font-medium text-slate-300">
          Drop fingerprint images or{" "}
          <span className="text-blue-400">browse files</span>
        </p>
        <p className="text-xs text-slate-500 mt-1">
          BMP, JPG, PNG — up to {maxFiles} images (one per finger)
        </p>
        {files.length > 0 && (
          <p className="text-xs text-emerald-500 mt-2 font-medium">
            {files.length} of {maxFiles} images loaded
          </p>
        )}
      </div>

      {/* File grid */}
      {files.length > 0 && (
        <div>
          <p className="text-xs text-slate-500 mb-2 uppercase tracking-widest font-medium">
            Loaded Images
          </p>
          <div className="grid grid-cols-5 gap-2">
            {files.map((f, i) => (
              <div
                key={i}
                className="relative group rounded-md overflow-hidden border border-slate-800 bg-slate-900"
              >
                {f.preview ? (
                  <img
                    src={f.preview}
                    alt={f.fingerLabel}
                    className="w-full h-16 object-cover filter grayscale"
                  />
                ) : (
                  <div className="w-full h-16 flex items-center justify-center bg-slate-800">
                    <Fingerprint className="w-6 h-6 text-slate-600" />
                  </div>
                )}
                <div className="px-1.5 py-1 bg-slate-900">
                  <p className="text-[9px] text-slate-400 font-medium leading-tight truncate">
                    {f.fingerLabel}
                  </p>
                  <p className="text-[8px] text-slate-600 truncate">{f.file.name}</p>
                </div>
                <button
                  onClick={(e) => { e.stopPropagation(); removeFile(i); }}
                  className="absolute top-1 right-1 w-4 h-4 rounded-full bg-slate-900/90 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity"
                >
                  <X className="w-2.5 h-2.5 text-slate-300" />
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      {files.length > 0 && files.length < 10 && (
        <div className="flex items-start gap-2 p-3 rounded-md bg-amber-950/30 border border-amber-900/40">
          <AlertCircle className="w-4 h-4 text-amber-500 flex-shrink-0 mt-0.5" />
          <p className="text-xs text-amber-400">
            For complete analysis, provide all 10 fingerprints (both hands). Partial results
            will be computed from available images only.
          </p>
        </div>
      )}
    </div>
  );
}
