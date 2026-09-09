import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({
  subsets: ["latin"],
  display: "swap",
  variable: "--font-inter",
});

export const metadata: Metadata = {
  title: {
    default: "Financial Crime Knowledge Engine",
    template: "%s | Financial Crime Knowledge Engine",
  },
  description:
    "A comprehensive knowledge engine for financial crime prevention, AML compliance, and regulatory intelligence.",
  keywords: [
    "financial crime",
    "AML",
    "anti-money laundering",
    "compliance",
    "knowledge engine",
    "regulatory intelligence",
  ],
  authors: [{ name: "FCKE Team" }],
  creator: "Financial Crime Knowledge Engine",
  openGraph: {
    type: "website",
    locale: "en_US",
    siteName: "Financial Crime Knowledge Engine",
    title: "Financial Crime Knowledge Engine",
    description:
      "A comprehensive knowledge engine for financial crime prevention, AML compliance, and regulatory intelligence.",
  },
  robots: {
    index: true,
    follow: true,
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={inter.variable}>
      <body className="min-h-screen bg-background font-sans antialiased">
        {children}
      </body>
    </html>
  );
}
