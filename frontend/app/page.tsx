/**
 * Commit: Keep root page redirect to login
 * 
 * Root page redirects to login page.
 * Authentication check handled by dashboard component.
 * 
 * Root Homepage
 * Redirects unauthenticated users to login page.
 * If authenticated, redirects to dashboard.
 */
import { redirect } from "next/navigation";

export default function Home() {
  // Redirect to login page
  // The middleware will handle redirecting authenticated users to dashboard
  redirect("/login");
}
