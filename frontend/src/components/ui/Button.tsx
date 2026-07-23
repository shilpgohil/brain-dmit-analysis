import { cn } from "@/lib/utils";
import { forwardRef, ButtonHTMLAttributes } from "react";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "ghost" | "danger" | "outline";
  size?: "sm" | "md" | "lg";
  loading?: boolean;
  icon?: React.ReactNode;
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ variant = "primary", size = "md", loading, icon, children, className, disabled, ...props }, ref) => {
    return (
      <button
        ref={ref}
        disabled={disabled || loading}
        className={cn(
          "inline-flex items-center justify-center gap-2 font-medium transition-all duration-150 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 focus-visible:ring-offset-slate-950 disabled:opacity-50 disabled:cursor-not-allowed select-none",
          size === "sm" && "h-7 px-3 text-xs rounded",
          size === "md" && "h-9 px-4 text-sm rounded-md",
          size === "lg" && "h-11 px-6 text-sm rounded-md",
          variant === "primary" && "bg-blue-600 text-white hover:bg-blue-500 active:bg-blue-700",
          variant === "secondary" && "bg-slate-800 text-slate-200 hover:bg-slate-700 border border-slate-700",
          variant === "outline" && "border border-slate-700 text-slate-300 hover:bg-slate-800 hover:border-slate-600",
          variant === "ghost" && "text-slate-400 hover:text-slate-200 hover:bg-slate-800",
          variant === "danger" && "bg-red-900/50 text-red-400 hover:bg-red-900 border border-red-800",
          className
        )}
        {...props}
      >
        {loading ? (
          <svg className="animate-spin h-3.5 w-3.5" viewBox="0 0 24 24" fill="none">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
          </svg>
        ) : icon}
        {children}
      </button>
    );
  }
);
Button.displayName = "Button";
