/**
 * Commit: Expand Hero Feed size and fix button overlay positioning
 * 
 * Improved primary monitoring channel layout and button visibility.
 * Fixed snapshot and record buttons overlapping with other elements.
 * 
 * Changes:
 * - Added min-h-[600px] to expand Hero Feed height
 * - Removed grid column constraints (col-span-2 row-span-2)
 * - Fixed button positioning with z-10 and better bottom placement
 * - Enhanced button styling with improved backdrop blur and shadows
 * - Changed overlay gradient to be more opaque at bottom (from-black/90)
 * - Improved button hover states and visibility
 * 
 * Primary Monitoring Channel (Hero Feed)
 * High-priority live monitor with:
 * - Scanning Line Overlay animation
 * - Real-time timestamp
 * - Interactive controls (Snapshot, Recording, Fullscreen)
 */
"use client";

import { useState, useRef, useEffect } from "react";

interface HeroFeedProps {
  cameraId?: number;
  cameraName: string;
  streamUrl?: string;
  isOnline?: boolean;
}

export default function HeroFeed({
  cameraId,
  cameraName,
  streamUrl = "http://localhost:5000/video_feed",
  isOnline = true,
}: HeroFeedProps) {
  const [isRecording, setIsRecording] = useState(false);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [streamError, setStreamError] = useState(false);
  const [recordingTime, setRecordingTime] = useState(0);
  const [currentTime, setCurrentTime] = useState(new Date());
  const cardRef = useRef<HTMLDivElement>(null);
  const videoRef = useRef<HTMLImageElement>(null);
  const recordingIntervalRef = useRef<NodeJS.Timeout | null>(null);

  const streamSrc = cameraId
    ? `${streamUrl}?camera_id=${cameraId}`
    : streamUrl;

  // Update timestamp every second
  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentTime(new Date());
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  // Recording timer
  useEffect(() => {
    if (isRecording) {
      setRecordingTime(0);
      recordingIntervalRef.current = setInterval(() => {
        setRecordingTime((prev) => prev + 1);
      }, 1000);
    } else {
      if (recordingIntervalRef.current) {
        clearInterval(recordingIntervalRef.current);
      }
    }
    return () => {
      if (recordingIntervalRef.current) {
        clearInterval(recordingIntervalRef.current);
      }
    };
  }, [isRecording]);

  const formatRecordingTime = (seconds: number) => {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes.toString().padStart(2, "0")}:${remainingSeconds
      .toString()
      .padStart(2, "0")}`;
  };

  const formatTimestamp = (date: Date) => {
    return date.toLocaleTimeString("en-US", {
      hour12: false,
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
    });
  };

  const toggleFullscreen = () => {
    if (!document.fullscreenElement) {
      cardRef.current?.requestFullscreen().catch((err) => {
        console.error(`Error attempting to enable full-screen mode: ${err.message}`);
      });
    } else {
      document.exitFullscreen();
    }
  };

  useEffect(() => {
    const handleFullscreenChange = () => {
      setIsFullscreen(!!document.fullscreenElement);
    };
    document.addEventListener("fullscreenchange", handleFullscreenChange);
    return () =>
      document.removeEventListener("fullscreenchange", handleFullscreenChange);
  }, []);

  const handleSnapshot = () => {
    if (videoRef.current) {
      const canvas = document.createElement("canvas");
      canvas.width = videoRef.current.naturalWidth;
      canvas.height = videoRef.current.naturalHeight;
      const ctx = canvas.getContext("2d");
      if (ctx) {
        ctx.drawImage(videoRef.current, 0, 0, canvas.width, canvas.height);
        const dataUrl = canvas.toDataURL("image/jpeg");
        const link = document.createElement("a");
        link.href = dataUrl;
        link.download = `${cameraName}_snapshot_${new Date().toISOString()}.jpg`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      }
    }
  };

  return (
    <div
      ref={cardRef}
      className={`relative flex flex-col rounded-2xl border border-cyan-500/30 bg-slate-900/40 p-6 shadow-2xl shadow-cyan-500/20 backdrop-blur-md ${
        isFullscreen ? "fixed inset-0 z-50 !rounded-none" : "min-h-[600px]"
      }`}
    >
      {/* Header with Timestamp */}
      <div className="mb-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2">
            <span
              className={`relative flex h-3 w-3 ${
                isOnline && !streamError ? "text-green-400" : "text-red-500"
              }`}
            >
              <span
                className={`absolute inline-flex h-full w-full rounded-full bg-current opacity-75 ${
                  isOnline && !streamError ? "animate-ping" : ""
                }`}
              ></span>
              <span className="relative inline-flex h-3 w-3 rounded-full bg-current"></span>
            </span>
            <h2 className="font-mono text-xl font-bold text-cyan-400">
              {cameraName}
            </h2>
          </div>
          <div className="rounded border border-slate-700/50 bg-slate-950/60 px-3 py-1 font-mono text-xs text-indigo-400">
            {formatTimestamp(currentTime)}
          </div>
        </div>
        <div className="flex items-center gap-2">
          {isRecording && (
            <span className="flex items-center gap-1 font-mono text-sm text-red-400">
              <span className="h-2 w-2 animate-pulse rounded-full bg-red-500"></span>
              REC {formatRecordingTime(recordingTime)}
            </span>
          )}
          <button
            onClick={toggleFullscreen}
            className="text-slate-400 transition-colors hover:text-cyan-400"
            title="Toggle Fullscreen"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              strokeWidth={1.5}
              stroke="currentColor"
              className="h-6 w-6"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M3.75 3.75v4.5m0-4.5h4.5m-4.5 0L9 9M3.75 20.25v-4.5m0 4.5h4.5m-4.5 0L9 15M20.25 3.75h-4.5m4.5 0v4.5m0-4.5L15 9m5.25 11.25h-4.5m4.5 0v-4.5m0 4.5L15 15"
              />
            </svg>
          </button>
        </div>
      </div>

      {/* Video Feed with Scanning Overlay */}
      <div className="relative flex-1 overflow-hidden rounded-xl border border-slate-700 bg-slate-950">
        {isOnline && !streamError ? (
          <>
            <img
              ref={videoRef}
              src={streamSrc}
              alt={`${cameraName} Live Feed`}
              className="h-full w-full object-cover"
              onError={() => setStreamError(true)}
            />
            {/* Scanning Line Overlay */}
            <div className="pointer-events-none absolute inset-0">
              <div className="h-full w-full animate-scan bg-gradient-to-b from-transparent via-cyan-500/20 to-transparent"></div>
            </div>
          </>
        ) : (
          <div className="flex h-full w-full items-center justify-center bg-slate-950 text-red-500">
            <div className="text-center font-mono">
              <p className="text-lg">SIGNAL LOST</p>
              <p className="text-sm text-slate-400">Camera Offline</p>
            </div>
          </div>
        )}

        {/* Controls Overlay - Fixed at bottom */}
        <div className="absolute bottom-0 left-0 right-0 flex items-center justify-center bg-gradient-to-t from-black/90 via-black/70 to-transparent p-4 pb-6">
          <div className="flex gap-3">
            <button
              onClick={handleSnapshot}
              className="z-10 rounded-lg border border-slate-700/50 bg-slate-900/90 px-4 py-2.5 font-mono text-sm font-medium text-slate-200 backdrop-blur-md transition-all hover:bg-slate-800/90 hover:border-cyan-500/50 hover:text-cyan-400"
              title="Take Snapshot"
            >
              📸 Snapshot
            </button>
            <button
              onClick={() => setIsRecording(!isRecording)}
              className={`z-10 rounded-lg border px-4 py-2.5 font-mono text-sm font-medium backdrop-blur-md transition-all ${
                isRecording
                  ? "border-red-500/70 bg-red-600/90 text-white hover:bg-red-500/90 shadow-lg shadow-red-500/30"
                  : "border-slate-700/50 bg-slate-900/90 text-slate-200 hover:bg-slate-800/90 hover:border-red-500/50 hover:text-red-400"
              }`}
              title={isRecording ? "Stop Recording" : "Start Recording"}
            >
              {isRecording ? "⏹ Stop" : "⏺ Record"}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

