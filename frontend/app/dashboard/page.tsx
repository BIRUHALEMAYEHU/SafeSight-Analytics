"use client";

import { useAuth } from "@/contexts/AuthContext";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import Sidebar from "@/components/Sidebar";
import HeroFeed from "@/components/HeroFeed";
import MonitorCard from "@/components/MonitorCard";

interface Camera {
  id: number;
  name: string;
  rtsp_url: string;
  location: string;
  is_active: boolean;
}

const API_URL =
  process.env.NEXT_PUBLIC_API_URL
    ? `${process.env.NEXT_PUBLIC_API_URL}/api/v1`
    : typeof window !== "undefined" && window.location.hostname !== "localhost"
    ? "https://safesight-backend.onrender.com/api/v1"
    : "http://localhost:8000/api/v1";

export default function DashboardPage() {
  const { user, status } = useAuth();
  const router = useRouter();
  const [cameras, setCameras] = useState<Camera[]>([]);
  const [loadingCameras, setLoadingCameras] = useState(true);

  useEffect(() => {
    if (status === "unauthenticated") {
      router.push("/login");
    }
  }, [status, router]);

  useEffect(() => {
    if (status === "authenticated") {
      fetchCameras();
    }
  }, [status]);

  async function fetchCameras() {
    setLoadingCameras(true);
    try {
      const token = localStorage.getItem("access_token");
      const res = await fetch(`${API_URL}/cameras`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (res.ok) {
        const data: Camera[] = await res.json();
        setCameras(data);
      }
    } catch (e) {
      console.error("Failed to fetch cameras", e);
    } finally {
      setLoadingCameras(false);
    }
  }

  if (status === "loading") {
    return (
      <div className="flex min-h-screen items-center justify-center bg-slate-950">
        <div className="text-slate-400 font-mono">Loading SafeSight Analytics...</div>
      </div>
    );
  }

  if (!user) return null;

  const activeCameras = cameras.filter((c) => c.is_active);
  const heroCam = activeCameras[0] ?? null;
  const gridCameras = activeCameras.slice(1);

  return (
    <div className="min-h-screen bg-slate-950">
      <Sidebar />

      <div className="ml-80 min-h-screen p-6">
        {/* Header */}
        <div className="mb-6 flex items-center justify-between">
          <div>
            <h1 className="mb-1 font-mono text-3xl font-bold text-cyan-400">
              SafeSight Analytics Dashboard
            </h1>
            <p className="font-mono text-sm text-slate-500">
              Real-time video surveillance and monitoring system
            </p>
          </div>
          <div className="font-mono text-xs text-slate-600">
            {activeCameras.length} active node{activeCameras.length !== 1 ? "s" : ""} online
          </div>
        </div>

        {/* No cameras state */}
        {!loadingCameras && activeCameras.length === 0 && (
          <div className="flex flex-col items-center justify-center rounded border border-dashed border-slate-700 bg-slate-900/50 p-16 text-center">
            <div className="mb-2 text-4xl">📹</div>
            <p className="mb-1 font-mono text-lg text-slate-400">No cameras configured</p>
            <p className="font-mono text-sm text-slate-600">
              Go to{" "}
              <button
                onClick={() => router.push("/dashboard/cameras")}
                className="text-cyan-500 underline hover:text-cyan-400"
              >
                Vision Nodes
              </button>{" "}
              to add your first camera feed.
            </p>
          </div>
        )}

        {/* Hero Feed — Primary Camera */}
        {heroCam && (
          <div className="mb-6">
            <HeroFeed
              cameraId={heroCam.id}
              cameraName={`${heroCam.name} — ${heroCam.location}`}
              streamUrl={heroCam.rtsp_url}
              isOnline={heroCam.is_active}
            />
          </div>
        )}

        {/* Vision Intelligence Grid — remaining cameras */}
        {gridCameras.length > 0 && (
          <div className="mb-6">
            <h2 className="mb-4 font-mono text-lg font-semibold text-indigo-400">
              Vision Nodes
            </h2>
            <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
              {gridCameras.map((cam) => (
                <MonitorCard
                  key={cam.id}
                  cameraId={cam.id}
                  cameraName={`${cam.name} — ${cam.location}`}
                  streamUrl={cam.rtsp_url}
                  isOnline={cam.is_active}
                />
              ))}
            </div>
          </div>
        )}

        {/* Loading skeleton */}
        {loadingCameras && (
          <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
            {[1, 2, 3].map((i) => (
              <div
                key={i}
                className="h-48 animate-pulse rounded border border-slate-800 bg-slate-900"
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
