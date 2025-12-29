/**
 * Commit: Implement credential validation with simple auth
 * 
 * Restored credential validation using login() function.
 * Only redirects to dashboard if username and password match.
 * 
 * Changes:
 * - Uses login() function from lib/auth.ts for validation
 * - Validates credentials before redirecting
 * - Shows error message if credentials don't match
 * - Only redirects to dashboard on successful authentication
 * 
 * Login Page UI
 * Security-themed login form with dark aesthetics.
 * Uses simple client-side authentication with credential validation.
 */
"use client";

import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";
import { login } from "@/lib/auth";

export default function LoginPage() {
  const router = useRouter();
  const [formState, setFormState] = useState({ username: "", password: "" });
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError("");
    setSubmitting(true);

    // Validate credentials using login function
    const success = login(formState.username, formState.password);

    setSubmitting(false);

    if (!success) {
      setError("Invalid username or password.");
      return;
    }

    // Redirect to dashboard only on successful login
    router.push("/dashboard");
    router.refresh();
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 px-4 text-slate-100">
      <div className="w-full max-w-md space-y-8 rounded-2xl border border-slate-800/60 bg-slate-900/80 p-8 shadow-2xl shadow-cyan-500/10 backdrop-blur-md">
        <div className="flex flex-col items-center gap-2 text-center">
          <div className="flex items-center gap-2 text-cyan-400">
            <span className="h-3 w-3 rounded-full bg-cyan-400 shadow-[0_0_12px_rgba(34,211,238,0.7)]" />
            <span className="text-sm font-semibold uppercase tracking-[0.35em] text-cyan-300/90 font-mono">
              SafeSight
            </span>
          </div>
          <h1 className="text-2xl font-semibold text-slate-50 font-mono">
            Secure Dashboard Login
          </h1>
          <p className="text-sm text-slate-400 font-mono">
            Sign in to access the monitoring dashboard.
          </p>
        </div>

        <form className="space-y-5" onSubmit={handleSubmit}>
          <div className="space-y-2">
            <label
              htmlFor="username"
              className="text-sm font-medium text-slate-300 font-mono"
            >
              Username
            </label>
            <input
              id="username"
              name="username"
              type="text"
              autoComplete="username"
              required
              value={formState.username}
              onChange={(event) =>
                setFormState((prev) => ({
                  ...prev,
                  username: event.target.value,
                }))
              }
              className="w-full rounded-xl border border-slate-800 bg-slate-950/60 px-4 py-3 text-sm text-slate-100 outline-none transition focus:border-cyan-500/70 focus:ring-2 focus:ring-cyan-500/30 font-mono"
              placeholder="Enter your username"
            />
          </div>

          <div className="space-y-2">
            <label
              htmlFor="password"
              className="text-sm font-medium text-slate-300 font-mono"
            >
              Password
            </label>
            <input
              id="password"
              name="password"
              type="password"
              autoComplete="current-password"
              required
              value={formState.password}
              onChange={(event) =>
                setFormState((prev) => ({
                  ...prev,
                  password: event.target.value,
                }))
              }
              className="w-full rounded-xl border border-slate-800 bg-slate-950/60 px-4 py-3 text-sm text-slate-100 outline-none transition focus:border-cyan-500/70 focus:ring-2 focus:ring-cyan-500/30 font-mono"
              placeholder="Enter your password"
            />
          </div>

          {error ? (
            <div className="rounded-lg border border-red-500/30 bg-red-500/10 px-3 py-2 text-sm text-red-200 font-mono">
              {error}
            </div>
          ) : null}

          <button
            type="submit"
            disabled={submitting}
            className="flex w-full items-center justify-center rounded-xl bg-gradient-to-r from-cyan-500 to-blue-600 px-4 py-3 text-sm font-semibold text-white shadow-lg shadow-cyan-500/20 transition hover:shadow-cyan-400/30 disabled:cursor-not-allowed disabled:opacity-60 font-mono"
          >
            {submitting ? "Signing in..." : "Sign in securely"}
          </button>
        </form>

        <p className="text-center text-xs text-slate-500 font-mono">
          Protected access • Client-side authentication
        </p>
      </div>
    </div>
  );
}


