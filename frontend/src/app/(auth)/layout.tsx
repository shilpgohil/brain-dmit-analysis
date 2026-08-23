// Auth route group — provides NO nav, NO pt-14.
// Root layout already supplies html/body, AmbientOrbs, CursorGlow, AuthBootstrap.
// This segment layout only overrides the <main> wrapper so auth pages get full-height
// with zero top padding (no fixed nav on these routes).
export default function AuthLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="relative z-10 min-h-screen">
      {children}
    </div>
  );
}
