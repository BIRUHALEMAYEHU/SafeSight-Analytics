/**
 * Root Homepage
 * 
 * Redirects unauthenticated users to login page.
 * If authenticated, redirects to dashboard.
 */
import { redirect } from "next/navigation";

export default function Home() {
  // Redirect to login page
  // The middleware will handle redirecting authenticated users to dashboard
  redirect("/login");
}
