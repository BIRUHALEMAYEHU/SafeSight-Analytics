/**
 * Commit: Merge sidebars and add backend fallback with useAuth integration
 * 
 * Combined TacticalSidebar and IntelligenceSidebar into unified component.
 * Replaced NextAuth useSession with useAuth hook.
 * Added graceful fallback to mock data when backend is unavailable.
 * 
 * Changes:
 * - Merged two separate sidebar components into one
 * - Replaced useSession() with useAuth()
 * - Added fallback telemetry data when backend fetch fails
 * - Added fallback security events when backend fetch fails
 * - Updated branding: "Tactical Command" → "Analytics Dashboard"
 * - Fixed useEffect dependencies to prevent infinite loops
 * 
 * Unified Sidebar - Tactical Command & Intelligence
 * Combined sidebar featuring:
 * - Global Navigation (Control Center, Vision Nodes, Threat Database)
 * - Profile node with clearance level and session timer
 * - AI Daily Briefing
 * - Live Telemetry (Buffer, CPU, Network)
 * - Security Event Log with severity-based color coding
 */
"use client";

import { useAuth } from "@/contexts/AuthContext";
import { useRouter, usePathname } from "next/navigation";
import { useState, useEffect } from "react";

interface NavItem {
  name: string;
  path: string;
  icon: string;
}

interface TelemetryData {
  buffer: number;
  cpu: number;
  ping: number;
}

interface SecurityEvent {
  id: string;
  timestamp: string;
  message: string;
  severity: "low" | "medium" | "high" | "critical";
}

const navItems: NavItem[] = [
  { name: "Control Center", path: "/dashboard", icon: "⚡" },
  { name: "Vision Nodes", path: "/dashboard/cameras", icon: "📹" },
  { name: "Threat Database", path: "/dashboard/threats", icon: "🔍" },
];

export default function Sidebar() {
  const { user } = useAuth();
  const router = useRouter();
  const pathname = usePathname();
  const [sessionTime, setSessionTime] = useState(0);
  const [telemetry, setTelemetry] = useState<TelemetryData>({
    buffer: 45,
    cpu: 62,
    ping: 12,
  });

  const [events, setEvents] = useState<SecurityEvent[]>([
    {
      id: "1",
      timestamp: "14:32:15",
      message: "Motion detected in Zone A",
      severity: "low",
    },
    {
      id: "2",
      timestamp: "14:28:42",
      message: "Face recognition: Unknown person",
      severity: "medium",
    },
    {
      id: "3",
      timestamp: "14:25:18",
      message: "Weapon detected in Zone C",
      severity: "critical",
    },
    {
      id: "4",
      timestamp: "14:20:05",
      message: "System backup completed",
      severity: "low",
    },
  ]);

  // Session timer
  useEffect(() => {
    const interval = setInterval(() => {
      setSessionTime((prev) => prev + 1);
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  // Fetch telemetry from backend (with fallback to mock data)
  useEffect(() => {
    const fetchTelemetry = async () => {
      try {
        const response = await fetch("http://localhost:5000/api/v1/telemetry");
        if (response.ok) {
          const data = await response.json();
          setTelemetry(data);
        } else {
          // Use mock data if backend is not available
          setTelemetry((prev) => ({
            buffer: Math.max(20, Math.min(90, prev.buffer + (Math.random() - 0.5) * 10)),
            cpu: Math.max(30, Math.min(85, prev.cpu + (Math.random() - 0.5) * 8)),
            ping: Math.max(5, Math.min(50, prev.ping + (Math.random() - 0.5) * 5)),
          }));
        }
      } catch (error) {
        // Backend not available - use simulated data
        setTelemetry((prev) => ({
          buffer: Math.max(20, Math.min(90, prev.buffer + (Math.random() - 0.5) * 10)),
          cpu: Math.max(30, Math.min(85, prev.cpu + (Math.random() - 0.5) * 8)),
          ping: Math.max(5, Math.min(50, prev.ping + (Math.random() - 0.5) * 5)),
        }));
      }
    };

    fetchTelemetry();
    const interval = setInterval(fetchTelemetry, 2000);
    return () => clearInterval(interval);
  }, []);

  // Fetch security events from backend (with fallback to mock data)
  useEffect(() => {
    const fetchEvents = async () => {
      try {
        const response = await fetch("http://localhost:5000/api/v1/events");
        if (response.ok) {
          const data = await response.json();
          setEvents(data);
        }
        // If backend fails, keep existing mock events
      } catch (error) {
        // Backend not available - keep mock events
        console.log("Backend not available, using mock events");
      }
    };

    fetchEvents();
    const interval = setInterval(fetchEvents, 5000);
    return () => clearInterval(interval);
  }, []);

  const formatSessionTime = (seconds: number) => {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    return `${hours.toString().padStart(2, "0")}:${minutes.toString().padStart(2, "0")}:${secs.toString().padStart(2, "0")}`;
  };

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case "critical":
        return "border-red-500/50 bg-red-500/10 text-red-400";
      case "high":
        return "border-orange-500/50 bg-orange-500/10 text-orange-400";
      case "medium":
        return "border-yellow-500/50 bg-yellow-500/10 text-yellow-400";
      default:
        return "border-slate-700/50 bg-slate-800/30 text-slate-400";
    }
  };

  const getSeverityPulse = (severity: string) => {
    return severity === "critical" || severity === "high"
      ? "animate-pulse border-red-500"
      : "";
  };

  return (
    <div className="fixed left-0 top-0 h-screen w-80 border-r border-slate-800/60 bg-slate-950/95 backdrop-blur-md overflow-y-auto">
      <div className="flex h-full flex-col p-6">
        {/* Logo/Header */}
        <div className="mb-6">
          <div className="flex items-center gap-2 text-cyan-500">
            <span className="text-2xl">🛡️</span>
            <span className="font-mono text-lg font-bold tracking-wider">
              SafeSight
            </span>
          </div>
          <p className="mt-1 font-mono text-xs text-slate-500">
            Analytics Dashboard
          </p>
        </div>

        {/* Navigation */}
        <nav className="mb-6 space-y-2">
          {navItems.map((item) => {
            const isActive = pathname === item.path;
            return (
              <button
                key={item.path}
                onClick={() => router.push(item.path)}
                className={`w-full rounded-lg border px-4 py-3 text-left font-mono text-sm transition-all ${
                  isActive
                    ? "border-cyan-500/50 bg-cyan-500/10 text-cyan-400 shadow-lg shadow-cyan-500/20"
                    : "border-slate-800/60 bg-slate-900/40 text-slate-400 hover:border-slate-700 hover:bg-slate-900/60 hover:text-slate-300"
                }`}
              >
                <span className="mr-2">{item.icon}</span>
                {item.name}
              </button>
            );
          })}
        </nav>

        {/* AI Daily Briefing */}
        <div className="mb-6 rounded-lg border border-indigo-500/30 bg-slate-900/40 p-4 backdrop-blur-sm">
          <div className="mb-3 flex items-center gap-2">
            <span className="text-indigo-400">🤖</span>
            <h3 className="font-mono text-sm font-semibold text-indigo-400">
              AI Daily Briefing
            </h3>
          </div>
          <p className="font-mono text-xs leading-relaxed text-slate-400">
            Last 24h: 3 critical alerts, 12 motion events, 2 unknown faces
            detected. System operating at 94% efficiency. All zones secured.
          </p>
        </div>

        {/* Live Telemetry */}
        <div className="mb-6 rounded-lg border border-slate-800/60 bg-slate-900/40 p-4 backdrop-blur-sm">
          <h3 className="mb-4 font-mono text-sm font-semibold text-cyan-400">
            Live Telemetry
          </h3>
          <div className="space-y-4">
            {/* Buffer Saturation */}
            <div>
              <div className="mb-1 flex justify-between font-mono text-xs">
                <span className="text-slate-400">Buffer Saturation</span>
                <span className="text-cyan-400">{telemetry.buffer.toFixed(0)}%</span>
              </div>
              <div className="h-2 overflow-hidden rounded-full bg-slate-800">
                <div
                  className="h-full bg-gradient-to-r from-cyan-500 to-blue-600 transition-all duration-500"
                  style={{ width: `${telemetry.buffer}%` }}
                ></div>
              </div>
            </div>

            {/* CPU Temperature */}
            <div>
              <div className="mb-1 flex justify-between font-mono text-xs">
                <span className="text-slate-400">CPU Temperature</span>
                <span className="text-orange-400">{telemetry.cpu.toFixed(0)}°C</span>
              </div>
              <div className="h-2 overflow-hidden rounded-full bg-slate-800">
                <div
                  className="h-full bg-gradient-to-r from-orange-500 to-red-600 transition-all duration-500"
                  style={{ width: `${telemetry.cpu}%` }}
                ></div>
              </div>
            </div>

            {/* Network Ping */}
            <div>
              <div className="mb-1 flex justify-between font-mono text-xs">
                <span className="text-slate-400">Network Ping</span>
                <span className="text-green-400">{telemetry.ping.toFixed(0)}ms</span>
              </div>
              <div className="h-2 overflow-hidden rounded-full bg-slate-800">
                <div
                  className="h-full bg-gradient-to-r from-green-500 to-emerald-600 transition-all duration-500"
                  style={{ width: `${(telemetry.ping / 50) * 100}%` }}
                ></div>
              </div>
            </div>
          </div>
        </div>

        {/* Security Event Log */}
        <div className="mb-6 flex-1 rounded-lg border border-slate-800/60 bg-slate-900/40 p-4 backdrop-blur-sm">
          <h3 className="mb-4 font-mono text-sm font-semibold text-cyan-400">
            Security Event Log
          </h3>
          <div className="space-y-2">
            {events.map((event) => (
              <div
                key={event.id}
                className={`rounded border p-3 font-mono text-xs transition-all ${getSeverityColor(
                  event.severity
                )} ${getSeverityPulse(event.severity)}`}
              >
                <div className="mb-1 flex justify-between">
                  <span className="font-semibold">{event.timestamp}</span>
                  <span className="uppercase">{event.severity}</span>
                </div>
                <p className="text-xs">{event.message}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Profile Node */}
        <div className="mt-auto rounded-lg border border-slate-800/60 bg-slate-900/40 p-4 backdrop-blur-sm">
          <div className="mb-3 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <div className="h-2 w-2 rounded-full bg-green-400 shadow-[0_0_8px_rgba(34,211,238,0.6)]"></div>
              <span className="font-mono text-xs text-slate-400">
                Clearance Level
              </span>
            </div>
            <span className="font-mono text-xs font-semibold text-cyan-400">
              ADMIN
            </span>
          </div>
          <div className="mb-2 font-mono text-xs text-slate-500">
            {user?.name || "Operator"}
          </div>
          <div className="flex items-center justify-between">
            <span className="font-mono text-xs text-slate-500">
              Session Time:
            </span>
            <span className="font-mono text-xs font-semibold text-indigo-400">
              {formatSessionTime(sessionTime)}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}

