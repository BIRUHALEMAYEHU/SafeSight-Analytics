/**
 * Commit: Replace NextAuth SessionProvider with custom AuthProvider
 * 
 * Updated to use custom AuthContext instead of NextAuth SessionProvider.
 * Enables useAuth() hook throughout the application.
 * 
 * Changes:
 * - Removed NextAuth SessionProvider import
 * - Now uses AuthContext from contexts/AuthContext.tsx
 * - Simplified props (removed session prop)
 * 
 * Auth Provider Wrapper
 * Client component wrapper for AuthContext.
 * Provides authentication state to all dashboard components.
 * Wraps children in layout.tsx to enable useAuth() hook.
 */
"use client";

import { AuthProvider as AuthContextProvider } from "@/contexts/AuthContext";
import type { ReactNode } from "react";

type AuthProviderProps = {
  children: ReactNode;
};

export default function AuthProvider({ children }: AuthProviderProps) {
  return <AuthContextProvider>{children}</AuthContextProvider>;
}
