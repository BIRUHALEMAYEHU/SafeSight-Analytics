/**
 * Commit: Update dashboard branding and replace NextAuth with useAuth
 * 
 * Updated dashboard header and replaced NextAuth with custom auth.
 * Changed branding from "Tactical Command Center" to "SafeSight Analytics Dashboard".
 * 
 * Changes:
 * - Replaced useSession() with useAuth() hook
 * - Updated header: "Tactical Command Center" → "SafeSight Analytics Dashboard"
 * - Removed "AI-powered threat detection" text
 * - Updated loading message to "Loading SafeSight Analytics..."
 * 
 * SafeSight Analytics Dashboard
 * Main monitoring dashboard featuring:
 * - Sidebar (Navigation, Telemetry, Events)
 * - Hero Feed (Primary Monitoring Channel)
 * - Visual Intelligence Grid (Camera Nodes)
 */
"use client";

import { useAuth } from "@/contexts/AuthContext";
import { useRouter } from "next/navigation";
import { useEffect } from "react";
import Sidebar from "@/components/Sidebar";
import HeroFeed from "@/components/HeroFeed";
import MonitorCard from "@/components/MonitorCard";

export default function DashboardPage() {
  const { user, status } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (status === "unauthenticated") {
      router.push("/login");
    }
  }, [status, router]);

  if (status === "loading") {
    return (
      <div className="flex min-h-screen items-center justify-center bg-slate-950">
        <div className="text-slate-400 font-mono">Loading SafeSight Analytics...</div>
      </div>
    );
  }

  if (!user) {
    return null;
  }

  return (
    <div className="min-h-screen bg-slate-950">
      {/* Unified Sidebar */}
      <Sidebar />

      {/* Main Content Area */}
      <div className="ml-80 min-h-screen p-6">
        {/* Header */}
        <div className="mb-6">
          <h1 className="mb-2 font-mono text-3xl font-bold text-cyan-400">
            SafeSight Analytics Dashboard
          </h1>
          <p className="font-mono text-sm text-slate-500">
            Real-time video surveillance and monitoring system
          </p>
        </div>

        {/* Hero Feed - Primary Monitoring Channel */}
        <div className="mb-6">
          <HeroFeed
            cameraId={1}
            cameraName="Primary Monitoring Channel"
            isOnline={true}
          />
        </div>

        {/* Visual Intelligence Grid - Camera Nodes */}
        <div className="mb-6">
          <h2 className="mb-4 font-mono text-lg font-semibold text-indigo-400">
            Vision Nodes
          </h2>
          <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
            <MonitorCard
              cameraId={2}
              cameraName="Camera 02 - Back Entrance"
              isOnline={true}
            />
            <MonitorCard
              cameraId={3}
              cameraName="Camera 03 - Parking Lot"
              isOnline={true}
            />
            <MonitorCard
              cameraId={4}
              cameraName="Camera 04 - Main Hall"
              isOnline={true}
            />
            <MonitorCard
              cameraId={5}
              cameraName="Camera 05 - Side Entrance"
              isOnline={true}
            />
            <MonitorCard
              cameraId={6}
              cameraName="Camera 06 - Loading Dock"
              isOnline={true}
            />
            <MonitorCard
              cameraId={7}
              cameraName="Camera 07 - Perimeter North"
              isOnline={true}
            />
          </div>
        </div>
      </div>
    </div>
  );
}


