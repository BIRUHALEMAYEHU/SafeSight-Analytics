/**
 * Commit: Update layout to use custom AuthProvider instead of NextAuth
 * 
 * Updated root layout to use custom AuthProvider wrapper.
 * Enables useAuth() hook throughout the application.
 * 
 * Changes:
 * - Updated comment to reflect useAuth() instead of useSession()
 * - AuthProvider now wraps app with custom AuthContext
 * 
 * Root Layout with Auth Provider
 * Wraps entire app with AuthProvider to enable authentication access.
 * All dashboard components can now use useAuth() hook.
 */
import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import AuthProvider from "../components/auth-provider";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "SafeSight Analytics",
  description: "Secure dashboard access for SafeSight Analytics",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <AuthProvider>{children}</AuthProvider>
      </body>
    </html>
  );
}
