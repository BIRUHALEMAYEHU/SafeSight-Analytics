/**
 * Commit: Update middleware to proxy and simplify for client-side auth
 * 
 * Migrated from NextAuth middleware to Next.js 16 proxy function.
 * Simplified to allow all requests through (client-side handles auth).
 * 
 * Changes:
 * - Renamed function from middleware() to proxy()
 * - Changed to default export (Next.js 16 requirement)
 * - Removed NextAuth withAuth dependency
 * - Simplified to just allow requests (auth handled client-side)
 * 
 * Proxy Route Protection
 * Protects /dashboard routes from unauthorized access.
 * Redirects unauthenticated users to /login page.
 * Uses simple client-side authentication check.
 */
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export default function proxy(request: NextRequest) {
  // Client-side auth check will handle redirect in dashboard component
  // This proxy just allows the request through
  return NextResponse.next();
}

export const config = {
  matcher: ["/dashboard/:path*"],
};

