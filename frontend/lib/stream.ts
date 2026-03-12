const DEFAULT_RELAY_URL =
  process.env.NEXT_PUBLIC_CAMERA_RELAY_URL ||
  (typeof window !== "undefined" && window.location.hostname !== "localhost"
    ? "https://safesight-camera-relay.onrender.com"
    : "http://localhost:5000");

export function getCameraRelayBaseUrl(): string {
  return DEFAULT_RELAY_URL.replace(/\/$/, "");
}

export function getCameraStreamUrl(cameraId: number): string {
  return `${getCameraRelayBaseUrl()}/video_feed?camera_id=${cameraId}`;
}
