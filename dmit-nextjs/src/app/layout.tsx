import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "DMIT Analysis System",
  description: "Advanced Dermatoglyphics Multiple Intelligence Test Analysis",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}