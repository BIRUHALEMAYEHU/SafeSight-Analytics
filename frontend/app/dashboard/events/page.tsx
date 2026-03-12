"use client";

import { useAuth } from "@/contexts/AuthContext";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import Sidebar from "@/components/Sidebar";

interface Event {
  id: number;
  camera_id: number;
  type: string;
  timestamp: string;
  event_metadata: Record<string, unknown>;
}

interface Alert {
  id: number;
  event_id: number;
  type: string;
  priority: string;
  status: string;
  created_at: string;
}

const API_URL =
  process.env.NEXT_PUBLIC_API_URL
    ? `${process.env.NEXT_PUBLIC_API_URL}/api/v1`
    : typeof window !== "undefined" && window.location.hostname !== "localhost"
    ? "https://safesight-backend.onrender.com/api/v1"
    : "http://localhost:8000/api/v1";

const PRIORITY_STYLE: Record<string, string> = {
  critical: "bg-red-500/20 text-red-400 border-red-800",
  warning: "bg-yellow-500/20 text-yellow-400 border-yellow-800",
  info: "bg-blue-500/20 text-blue-400 border-blue-800",
};

const STATUS_STYLE: Record<string, string> = {
  new: "bg-red-500/20 text-red-400",
  acknowledged: "bg-yellow-500/20 text-yellow-400",
  resolved: "bg-green-500/20 text-green-400",
};

const EVENT_ICON: Record<string, string> = {
  person_detected: "👤",
  unknown_face: "❓",
  weapon_detected: "⚠️",
  face_detected: "👁️",
};

function formatTime(ts: string) {
  try {
    return new Date(ts).toLocaleString();
  } catch {
    return ts;
  }
}

export default function EventsPage() {
  const { user, status } = useAuth();
  const router = useRouter();
  const [events, setEvents] = useState<Event[]>([]);
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [loading, setLoading] = useState(true);
  const [tab, setTab] = useState<"alerts" | "events">("alerts");

  useEffect(() => {
    if (status === "unauthenticated") router.push("/login");
  }, [status, router]);

  useEffect(() => {
    if (status === "authenticated") {
      fetchData();
      const interval = setInterval(fetchData, 10000); // poll every 10s
      return () => clearInterval(interval);
    }
  }, [status]);

  async function fetchData() {
    const token = localStorage.getItem("access_token");
    const headers = { Authorization: `Bearer ${token}` };
    try {
      const [evRes, alRes] = await Promise.all([
        fetch(`${API_URL}/events/?limit=50`, { headers }),
        fetch(`${API_URL}/alerts/?limit=50`, { headers }),
      ]);
      if (evRes.ok) {
        const d = await evRes.json();
        setEvents(d.items ?? d);
      }
      if (alRes.ok) setAlerts(await alRes.json());
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  }

  async function updateAlertStatus(alertId: number, action: "acknowledge" | "resolve") {
    const token = localStorage.getItem("access_token");
    await fetch(`${API_URL}/alerts/${alertId}/${action}`, {
      method: "PUT",
      headers: { Authorization: `Bearer ${token}` },
    });
    fetchData();
  }

  if (status === "loading") return <div className="flex min-h-screen items-center justify-center bg-slate-950 text-slate-400 font-mono">Loading...</div>;
  if (!user) return null;

  const activeAlerts = alerts.filter((a) => a.status !== "resolved");

  return (
    <div className="min-h-screen bg-slate-950">
      <Sidebar />
      <div className="ml-80 min-h-screen p-6">
        {/* Header */}
        <div className="mb-6">
          <h1 className="font-mono text-3xl font-bold text-cyan-400">Security Events</h1>
          <p className="font-mono text-sm text-slate-500">Detection events and generated alerts</p>
        </div>

        {/* Stats Row */}
        <div className="mb-6 grid grid-cols-3 gap-4">
          {[
            { label: "Total Events", value: events.length, color: "text-cyan-400" },
            { label: "Active Alerts", value: activeAlerts.length, color: activeAlerts.length > 0 ? "text-red-400" : "text-green-400" },
            { label: "Resolved", value: alerts.filter((a) => a.status === "resolved").length, color: "text-green-400" },
          ].map(({ label, value, color }) => (
            <div key={label} className="rounded border border-slate-800 bg-slate-900 p-4 text-center">
              <div className={`font-mono text-2xl font-bold ${color}`}>{value}</div>
              <div className="font-mono text-xs text-slate-500">{label}</div>
            </div>
          ))}
        </div>

        {/* Tabs */}
        <div className="mb-4 flex gap-1 rounded border border-slate-800 bg-slate-900/50 p-1 w-fit">
          {(["alerts", "events"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`rounded px-4 py-1.5 font-mono text-sm transition-colors ${
                tab === t ? "bg-cyan-500/20 text-cyan-400" : "text-slate-500 hover:text-slate-300"
              }`}
            >
              {t === "alerts" ? `🔔 Alerts (${alerts.length})` : `📋 Events (${events.length})`}
            </button>
          ))}
        </div>

        {loading ? (
          <div className="font-mono text-slate-400">Loading data...</div>
        ) : tab === "alerts" ? (
          /* Alerts List */
          alerts.length === 0 ? (
            <div className="rounded border border-slate-800 bg-slate-900 p-8 text-center font-mono text-slate-500">
              No alerts generated yet. Alerts appear automatically when detection rules match.
            </div>
          ) : (
            <div className="space-y-3">
              {alerts.map((alert) => (
                <div key={alert.id} className="rounded border border-slate-800 bg-slate-900 p-4">
                  <div className="flex items-start justify-between gap-4">
                    <div className="flex-1">
                      <div className="mb-1 flex items-center gap-2">
                        <span className={`rounded border px-2 py-0.5 font-mono text-xs ${PRIORITY_STYLE[alert.priority] || PRIORITY_STYLE.info}`}>
                          {alert.priority.toUpperCase()}
                        </span>
                        <span className={`rounded px-2 py-0.5 font-mono text-xs ${STATUS_STYLE[alert.status] || ""}`}>
                          {alert.status.toUpperCase()}
                        </span>
                        <span className="font-mono text-xs text-slate-500">Event #{alert.event_id}</span>
                      </div>
                      <p className="font-mono text-sm text-slate-300">{alert.type.replace(/_/g, " ")}</p>
                      <p className="font-mono text-xs text-slate-600">{formatTime(alert.created_at)}</p>
                    </div>
                    <div className="flex gap-2">
                      {alert.status === "new" && (
                        <button
                          onClick={() => updateAlertStatus(alert.id, "acknowledge")}
                          className="rounded border border-yellow-800 bg-yellow-900/20 px-3 py-1 font-mono text-xs text-yellow-400 hover:bg-yellow-900/40 transition-colors"
                        >
                          Acknowledge
                        </button>
                      )}
                      {alert.status !== "resolved" && (
                        <button
                          onClick={() => updateAlertStatus(alert.id, "resolve")}
                          className="rounded border border-green-800 bg-green-900/20 px-3 py-1 font-mono text-xs text-green-400 hover:bg-green-900/40 transition-colors"
                        >
                          Resolve
                        </button>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )
        ) : (
          /* Events List */
          events.length === 0 ? (
            <div className="rounded border border-slate-800 bg-slate-900 p-8 text-center font-mono text-slate-500">
              No detection events yet. Events are created when the vision service analyzes frames.
            </div>
          ) : (
            <div className="space-y-2">
              {events.map((ev) => (
                <div key={ev.id} className="flex items-center gap-4 rounded border border-slate-800 bg-slate-900 p-3">
                  <span className="text-xl">{EVENT_ICON[ev.type] || "📡"}</span>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2">
                      <span className="font-mono text-sm text-slate-200">{ev.type.replace(/_/g, " ")}</span>
                      <span className="font-mono text-xs text-slate-500">Cam #{ev.camera_id}</span>
                    </div>
                    {ev.event_metadata?.person_name != null && (
                      <p className="font-mono text-xs text-cyan-600">
                        {String(ev.event_metadata.person_name)}
                        {ev.event_metadata.confidence != null && ` (${(Number(ev.event_metadata.confidence) * 100).toFixed(0)}%)`}
                      </p>
                    )}
                  </div>
                  <span className="font-mono text-xs text-slate-600 whitespace-nowrap">{formatTime(ev.timestamp)}</span>
                </div>
              ))}
            </div>
          )
        )}
      </div>
    </div>
  );
}
