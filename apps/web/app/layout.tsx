import type { Metadata } from "next";

import "./globals.css";

export const metadata: Metadata = {
  title: "Career Prediction System",
  description:
    "Career Prediction and Skill Gap Analysis System for Mass Communication Technology Students",
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="th">
      <body className="antialiased">{children}</body>
    </html>
  );
}
