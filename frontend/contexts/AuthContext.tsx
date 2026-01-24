/**
 * Commit: Create AuthContext to replace NextAuth SessionProvider
 * 
 * Replaces NextAuth's useSession hook with custom useAuth hook.
 * Provides authentication state management without NextAuth dependency.
 * 
 * Changes:
 * - Created React Context for authentication state
 * - Replaces NextAuth SessionProvider
 * - Listens to localStorage changes for cross-tab sync
 * - Provides user, status, and logout function
 * 
 * Simple Auth Context
 * Provides authentication state to all components.
 * Replaces NextAuth SessionProvider.
 */
"use client";

import { createContext, useContext, useState, useEffect, ReactNode } from "react";
import { useRouter, usePathname } from "next/navigation";
import { ensureSession, logout as logoutUser, type User } from "@/lib/auth";

interface AuthContextType {
  user: User | null;
  status: "loading" | "authenticated" | "unauthenticated";
  logout: () => void;
}

const AuthContext = createContext<AuthContextType>({
  user: null,
  status: "unauthenticated",
  logout: () => {},
});

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [status, setStatus] = useState<"loading" | "authenticated" | "unauthenticated">("loading");
  const router = useRouter();
  const pathname = usePathname();

  useEffect(() => {
    let active = true;

    const syncSession = async () => {
      setStatus("loading");
      const currentUser = await ensureSession();
      if (!active) return;

      setUser(currentUser);
      setStatus(currentUser ? "authenticated" : "unauthenticated");

      if (!currentUser && pathname?.startsWith("/dashboard")) {
        router.push("/login");
      }
    };

    syncSession();

    const handleStorageChange = () => {
      syncSession();
    };

    window.addEventListener("storage", handleStorageChange);
    return () => {
      active = false;
      window.removeEventListener("storage", handleStorageChange);
    };
  }, [pathname, router]);

  const logout = () => {
    logoutUser();
    setUser(null);
    setStatus("unauthenticated");
    router.push("/login");
  };

  return (
    <AuthContext.Provider value={{ user, status, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}

