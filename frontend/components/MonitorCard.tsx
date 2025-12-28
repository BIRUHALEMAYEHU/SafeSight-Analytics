/**
 * Phase 2: The Live Feed Component
 * MonitorCard Component
 * 
 * Implements glassmorphism design with MJPEG stream integration.
 * Features: live status indicator, snapshot, recording, and fullscreen capabilities.
 */
"use client";

import { useState, useRef, useEffect } from "react";

interface MonitorCardProps {
  cameraId?: number;
  cameraName: string;
  streamUrl?: string;
  isOnline?: boolean;
  priority?: "high" | "normal";
}

export default function MonitorCard({
  cameraId,
  cameraName,
  streamUrl = "http://localhost:5000/video_feed",
  isOnline = true,
  priority = "normal",
}: MonitorCardProps) {
  const [isRecording, setIsRecording] = useState(false);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [streamError, setStreamError] = useState(false);
  const [showControls, setShowControls] = useState(false);
  const [recordingTime, setRecordingTime] = useState(0);
  const [toast, setToast] = useState<{ message: string; type: "success" | "error" } | null>(null);
  const cardRef = useRef<HTMLDivElement>(null);
  const videoRef = useRef<HTMLImageElement>(null);
  const recordingIntervalRef = useRef<NodeJS.Timeout | null>(null);

  // Add camera_id query param if provided
  const streamSrc = cameraId
    ? `${streamUrl}?camera_id=${cameraId}`
    : streamUrl;

  // Recording timer
  useEffect(() => {
    if (isRecording) {
      recordingIntervalRef.current = setInterval(() => {
        setRecordingTime((prev) => prev + 1);
      }, 1000);
    } else {
      if (recordingIntervalRef.current) {
        clearInterval(recordingIntervalRef.current);
        recordingIntervalRef.current = null;
      }
      setRecordingTime(0);
    }
    return () => {
      if (recordingIntervalRef.current) {
        clearInterval(recordingIntervalRef.current);
      }
    };
  }, [isRecording]);

  // Format recording time as MM:SS
  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, "0")}:${secs.toString().padStart(2, "0")}`;
  };

  // Toast notification
  const showToast = (message: string, type: "success" | "error" = "success") => {
    setToast({ message, type });
    setTimeout(() => setToast(null), 3000);
  };

  const toggleFullscreen = async () => {
    if (!cardRef.current) return;

    try {
      if (!isFullscreen) {
        if (cardRef.current.requestFullscreen) {
          await cardRef.current.requestFullscreen();
        }
      } else {
        if (document.exitFullscreen) {
          await document.exitFullscreen();
        }
      }
    } catch (error) {
      console.error("Fullscreen error:", error);
      showToast("Fullscreen not supported", "error");
    }
  };

  useEffect(() => {
    const handleFullscreenChange = () => {
      setIsFullscreen(!!document.fullscreenElement);
    };

    document.addEventListener("fullscreenchange", handleFullscreenChange);
    return () => {
      document.removeEventListener("fullscreenchange", handleFullscreenChange);
    };
  }, []);

  const handleSnapshot = () => {
    if (videoRef.current && !streamError) {
      try {
        const canvas = document.createElement("canvas");
        const ctx = canvas.getContext("2d");
        if (ctx && videoRef.current) {
          canvas.width = videoRef.current.naturalWidth || 640;
          canvas.height = videoRef.current.naturalHeight || 480;
          ctx.drawImage(videoRef.current, 0, 0);
          canvas.toBlob((blob) => {
            if (blob) {
              const url = URL.createObjectURL(blob);
              const a = document.createElement("a");
              a.href = url;
              a.download = `snapshot-${cameraName.replace(/\s+/g, "-")}-${Date.now()}.jpg`;
              document.body.appendChild(a);
              a.click();
              document.body.removeChild(a);
              URL.revokeObjectURL(url);
              showToast("Snapshot captured successfully");
            }
          }, "image/jpeg");
        }
      } catch (error) {
        console.error("Snapshot error:", error);
        showToast("Failed to capture snapshot", "error");
      }
    } else {
      showToast("Camera offline - cannot capture snapshot", "error");
    }
  };

  const handleRecordToggle = () => {
    setIsRecording(!isRecording);
    if (!isRecording) {
      showToast("Recording started");
    } else {
      showToast(`Recording stopped - ${formatTime(recordingTime)}`);
    }
  };

  return (
    <>
      <div
        ref={cardRef}
        className={`relative group rounded-lg overflow-hidden border border-slate-800 bg-slate-900/40 backdrop-blur-md shadow-lg shadow-cyan-500/5 transition-all hover:border-cyan-500/30 hover:shadow-cyan-500/10 ${
          priority === "high" ? "ring-2 ring-cyan-500/50" : ""
        }`}
        onMouseEnter={() => setShowControls(true)}
        onMouseLeave={() => setShowControls(false)}
      >
        {/* Header with Status Bar */}
        <div className="absolute top-0 left-0 right-0 z-20 flex items-center justify-between px-4 py-2.5 bg-gradient-to-b from-slate-950/95 to-transparent">
          <div className="flex items-center gap-3">
            {/* Pulsing Status Indicator */}
            <div className="flex items-center gap-2">
              <span
                className={`h-2.5 w-2.5 rounded-full ${
                  isOnline && !streamError
                    ? "bg-green-500 animate-pulse shadow-[0_0_8px_rgba(34,197,94,0.8)]"
                    : "bg-red-500"
                }`}
                style={{
                  animation: isOnline && !streamError ? "pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite" : "none",
                }}
              />
              <span className="text-xs font-semibold text-slate-200 font-mono tracking-wider">
                {isOnline && !streamError ? "LIVE" : "OFFLINE"}
              </span>
            </div>
            <span className="text-sm text-slate-400 font-mono">
              {cameraName}
            </span>
            {priority === "high" && (
              <span className="px-2 py-0.5 rounded text-xs font-mono bg-cyan-500/20 text-cyan-400 border border-cyan-500/30">
                HIGH PRIORITY
              </span>
            )}
          </div>

          {/* Fullscreen Button */}
          <button
            onClick={toggleFullscreen}
            className="p-1.5 rounded-md bg-slate-800/60 hover:bg-slate-700/80 text-slate-300 hover:text-cyan-400 transition-colors"
            aria-label="Toggle fullscreen"
          >
            <svg
              className="w-4 h-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              {isFullscreen ? (
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M6 18L18 6M6 6l12 12"
                />
              ) : (
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4"
                />
              )}
            </svg>
          </button>
        </div>

        {/* Video Stream Container */}
        <div className="relative w-full aspect-video bg-slate-950">
          {streamError ? (
            <div className="flex items-center justify-center h-full bg-slate-900/50 relative overflow-hidden">
              {/* Glitch Effect Placeholder */}
              <div className="absolute inset-0 bg-gradient-to-br from-red-900/20 to-slate-900/50 animate-pulse" />
              <div className="relative text-center z-10">
                <div className="text-5xl mb-3 animate-pulse">📷</div>
                <p className="text-slate-400 font-mono text-sm tracking-wider">
                  SIGNAL LOST
                </p>
                <p className="text-slate-500 font-mono text-xs mt-1">
                  Camera Offline
                </p>
              </div>
            </div>
          ) : (
            <img
              ref={videoRef}
              src={streamSrc}
              alt={`${cameraName} stream`}
              className="w-full h-full object-cover"
              onError={() => setStreamError(true)}
              crossOrigin="anonymous"
            />
          )}
        </div>

        {/* Control Overlay */}
        <div
          className={`absolute bottom-0 left-0 right-0 z-20 flex items-center justify-center gap-3 px-4 py-3 bg-gradient-to-t from-slate-950/98 to-transparent transition-opacity duration-300 ${
            showControls ? "opacity-100" : "opacity-0"
          }`}
        >
          {/* Snapshot Button */}
          <button
            onClick={handleSnapshot}
            className="flex items-center gap-2 px-4 py-2 rounded-lg bg-slate-800/80 hover:bg-slate-700/90 text-slate-200 hover:text-cyan-400 transition-colors border border-slate-700/50 hover:border-cyan-500/50 font-mono text-xs"
            aria-label="Take snapshot"
          >
            <svg
              className="w-4 h-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z"
              />
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M15 13a3 3 0 11-6 0 3 3 0 016 0z"
              />
            </svg>
            <span>Snapshot</span>
          </button>

          {/* Record Button with Timer */}
          <button
            onClick={handleRecordToggle}
            className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-colors border font-mono text-xs ${
              isRecording
                ? "bg-red-600/80 hover:bg-red-700/90 text-white border-red-500/50"
                : "bg-slate-800/80 hover:bg-slate-700/90 text-slate-200 hover:text-red-400 border-slate-700/50 hover:border-red-500/50"
            }`}
            aria-label={isRecording ? "Stop recording" : "Start recording"}
          >
            <div
              className={`w-3 h-3 rounded-full ${
                isRecording
                  ? "bg-white animate-pulse shadow-[0_0_8px_rgba(239,68,68,0.8)]"
                  : "bg-red-500"
              }`}
              style={{
                animation: isRecording
                  ? "pulse 1s cubic-bezier(0.4, 0, 0.6, 1) infinite"
                  : "none",
              }}
            />
            <span>
              {isRecording ? `REC ${formatTime(recordingTime)}` : "Record"}
            </span>
          </button>
        </div>

        {/* Timestamp (bottom right) */}
        <div className="absolute bottom-2 right-2 z-10 px-2 py-1 rounded bg-slate-950/90 border border-slate-800/50 backdrop-blur-sm">
          <span className="text-xs text-slate-400 font-mono">
            {new Date().toLocaleTimeString()}
          </span>
        </div>
      </div>

      {/* Toast Notification */}
      {toast && (
        <div
          className={`fixed bottom-4 left-1/2 transform -translate-x-1/2 z-50 px-4 py-2 rounded-lg border font-mono text-sm shadow-lg backdrop-blur-md transition-all ${
            toast.type === "success"
              ? "bg-green-500/20 border-green-500/50 text-green-400"
              : "bg-red-500/20 border-red-500/50 text-red-400"
          }`}
        >
          {toast.message}
        </div>
      )}
    </>
  );
}


