/**
 * Phase 1: Authentication & Protected Routes - Task 1.3
 * Middleware Route Protection
 * 
 * Protects /dashboard routes from unauthorized access.
 * Redirects unauthenticated users to /login page.
 * Uses NextAuth middleware to validate JWT tokens.
 */
import { withAuth } from "next-auth/middleware";

export default withAuth({
  pages: {
    signIn: "/login",
  },
  callbacks: {
    authorized: ({ token }) => !!token,
  },
});

export const config = {
  matcher: ["/dashboard/:path*"],
};

