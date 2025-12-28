/**
 * Phase 2: The Live Feed Component
 * Dashboard Integration
 * 
 * Protected dashboard page displaying live camera feeds.
 * Features MonitorCard components in a responsive grid layout.
 * Demonstrates high-priority feed alongside standard feeds.
 */
"use client";

import { useSession } from "next-auth/react";
import { useRouter } from "next/navigation";
import { useEffect } from "react";
import MonitorCard from "@/components/MonitorCard";

export default function DashboardPage() {
  const { data: session, status } = useSession();
  const router = useRouter();

  useEffect(() => {
    if (status === "unauthenticated") {
      router.push("/login");
    }
  }, [status, router]);

  if (status === "loading") {
    return (
      <div className="flex min-h-screen items-center justify-center bg-slate-950">
        <div className="text-slate-400 font-mono">Loading...</div>
      </div>
    );
  }

  if (!session) {
    return null;
  }

  return (
    <div className="min-h-screen bg-slate-950 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-6">
          <h1 className="text-2xl font-semibold text-slate-100 mb-2 font-mono">
            Live Monitoring Dashboard
          </h1>
          <p className="text-slate-400 font-mono text-sm">
            Real-time camera feeds • Secure access
          </p>
        </div>

        {/* Monitor Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* High Priority Feed */}
          <MonitorCard
            cameraId={1}
            cameraName="Camera 01 - Front Door"
            isOnline={true}
            priority="high"
          />
          
          {/* Standard Feeds */}
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
        </div>
      </div>
    </div>
  );
}


