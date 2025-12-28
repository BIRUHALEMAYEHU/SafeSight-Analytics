/**
 * Phase 1: Authentication & Protected Routes - Task 1.4
 * Auth Provider Wrapper
 * 
 * Client component wrapper for NextAuth SessionProvider.
 * Provides session context to all dashboard components.
 * Wraps children in layout.tsx to enable useSession() hook.
 */
"use client";

import { SessionProvider } from "next-auth/react";
import type { ReactNode } from "react";
import type { Session } from "next-auth";

type AuthProviderProps = {
  children: ReactNode;
  session?: Session | null;
};

export default function AuthProvider({ children, session }: AuthProviderProps) {
  return <SessionProvider session={session}>{children}</SessionProvider>;
}
