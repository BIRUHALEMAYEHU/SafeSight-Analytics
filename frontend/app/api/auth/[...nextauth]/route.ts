/**
 * Phase 1: Authentication & Protected Routes - Task 1.1
 * NextAuth.js Configuration
 * 
 * Route handler for NextAuth authentication.
 * Implements Credentials Provider for username/password login.
 * Issues JWT session tokens for authenticated users.
 * 
 * Environment variables required:
 * - AUTH_USERNAME: Username for authentication
 * - AUTH_PASSWORD: Password for authentication
 * - NEXTAUTH_SECRET: Secret key for JWT signing
 */
import NextAuth, { type NextAuthOptions } from "next-auth";
import CredentialsProvider from "next-auth/providers/credentials";

export const authOptions: NextAuthOptions = {
  providers: [
    CredentialsProvider({
      name: "Credentials",
      credentials: {
        username: { label: "Username", type: "text" },
        password: { label: "Password", type: "password" },
      },
      async authorize(credentials) {
        try {
          // Default credentials (can be overridden by environment variables)
          const configuredUsername = process.env.AUTH_USERNAME || "admin";
          const configuredPassword = process.env.AUTH_PASSWORD || "admin123";

          if (!credentials?.username || !credentials?.password) {
            return null;
          }

          if (
            credentials.username === configuredUsername &&
            credentials.password === configuredPassword
          ) {
            return {
              id: configuredUsername,
              name: configuredUsername,
              email: `${configuredUsername}@safesight.local`,
            };
          }

          return null;
        } catch (error) {
          console.error("Authorization error:", error);
          return null;
        }
      },
    }),
  ],
  session: {
    strategy: "jwt",
    maxAge: 30 * 24 * 60 * 60, // 30 days
  },
  pages: {
    signIn: "/login",
  },
  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.sub = user.id;
        token.name = user.name;
        token.email = user.email;
      }
      return token;
    },
    async session({ session, token }) {
      if (session.user && token) {
        if (token.sub) {
          (session.user as any).id = token.sub;
        }
        if (token.name) {
          session.user.name = token.name as string;
        }
        if (token.email) {
          session.user.email = token.email as string;
        }
      }
      return session;
    },
  },
  secret: process.env.NEXTAUTH_SECRET || "fallback-secret-key-change-in-production",
  debug: process.env.NODE_ENV === "development",
};

const handler = NextAuth(authOptions);

export { handler as GET, handler as POST };
