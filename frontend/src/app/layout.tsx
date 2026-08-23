import type { Metadata } from "next";
import { Cormorant_Garamond, Inter, JetBrains_Mono } from "next/font/google";
import "./globals.css";
import { CinematicNav } from "@/components/layout/CinematicNav";
import { AmbientOrbs } from "@/components/effects/AmbientOrbs";
import { CursorGlow } from "@/components/effects/CursorGlow";
import { SmoothScroll } from "@/components/layout/SmoothScroll";
import { AuthBootstrap } from "@/components/layout/AuthBootstrap";
import { MainContent } from "@/components/layout/MainContent";

const cormorant = Cormorant_Garamond({
  subsets: ["latin"],
  variable: "--font-serif-display",
  display: "swap",
  weight: ["300", "400", "500", "600", "700"],
  style: ["normal", "italic"],
});

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
});

const jetbrainsMono = JetBrains_Mono({
  subsets: ["latin"],
  variable: "--font-mono-var",
  display: "swap",
  weight: ["300", "400", "500"],
});

export const metadata: Metadata = {
  title: "DMIT — Biometric Intelligence Platform",
  description:
    "Dermatoglyphics Multiple Intelligence Test: cinematic fingerprint-based cognitive profiling, neural mapping, and intelligence analysis.",
  icons: { icon: "/favicon.ico" },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={`${cormorant.variable} ${inter.variable} ${jetbrainsMono.variable}`}>
      <body className="bg-[#020208] text-[#eef2ff] antialiased overflow-x-hidden grain">
        <SmoothScroll>
          {/* Fixed ambient background */}
          <AmbientOrbs />

          {/* Fixed grid lines background */}
          <div className="fixed inset-0 grid-lines pointer-events-none z-0 opacity-60" />

          {/* Custom cursor */}
          <CursorGlow />

          {/* Auth boot-refresh — silently restores session from httpOnly refresh cookie */}
          <AuthBootstrap />

          {/* Navigation */}
          <CinematicNav />

          {/* Page content */}
          <MainContent>{children}</MainContent>
        </SmoothScroll>
      </body>
    </html>
  );
}
