import os
from pathlib import Path
import threading
import time
from dataclasses import dataclass, field
from typing import Any, Dict, Optional

import cv2
import numpy as np
import requests
from flask import Flask, Response, jsonify, request
from flask_cors import CORS


BACKEND_API_URL = os.getenv("BACKEND_API_URL", "http://localhost:8000/api/v1")
BACKEND_ACCESS_TOKEN = os.getenv("BACKEND_ACCESS_TOKEN")
BACKEND_USERNAME = os.getenv("BACKEND_USERNAME")
BACKEND_PASSWORD = os.getenv("BACKEND_PASSWORD")
VISION_API_URL = os.getenv("VISION_API_URL")
ENABLE_ANALYSIS = os.getenv("ENABLE_ANALYSIS", "false").lower() == "true"
ANALYZE_INTERVAL = float(os.getenv("ANALYZE_INTERVAL", "2.0"))
RECONNECT_DELAY = float(os.getenv("RECONNECT_DELAY", "2.0"))
FRAME_SLEEP = float(os.getenv("FRAME_SLEEP", "0.05"))
JPEG_QUALITY = int(os.getenv("JPEG_QUALITY", "80"))
DEMO_ASSETS_DIR = Path(os.getenv("DEMO_ASSETS_DIR", Path(__file__).resolve().parent / "assets"))


app = Flask(__name__)
CORS(app)


def _now() -> float:
    return time.time()


def _placeholder_frame(camera_id: int, message: str) -> bytes:
    frame = 255 * np.ones((480, 854, 3), dtype=np.uint8)
    cv2.rectangle(frame, (0, 0), (854, 480), (16, 24, 39), -1)
    cv2.putText(
        frame,
        f"SafeSight Relay - Camera {camera_id}",
        (24, 60),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        (34, 211, 238),
        2,
        cv2.LINE_AA,
    )
    cv2.putText(
        frame,
        message[:70],
        (24, 120),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.75,
        (248, 113, 113),
        2,
        cv2.LINE_AA,
    )
    ok, buffer = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), JPEG_QUALITY])
    return buffer.tobytes() if ok else b""


@dataclass
class CameraSession:
    camera_id: int
    thread: Optional[threading.Thread] = None
    latest_frame: Optional[bytes] = None
    latest_source: Optional[str] = None
    last_frame_at: Optional[float] = None
    last_error: Optional[str] = None
    status: str = "idle"
    viewers: int = 0
    captures_started: int = 0
    lock: threading.Lock = field(default_factory=threading.Lock)
    new_frame: threading.Event = field(default_factory=threading.Event)
    stop_event: threading.Event = field(default_factory=threading.Event)

    def to_dict(self) -> Dict[str, Any]:
        with self.lock:
            return {
                "camera_id": self.camera_id,
                "status": self.status,
                "viewers": self.viewers,
                "captures_started": self.captures_started,
                "last_frame_at": self.last_frame_at,
                "last_error": self.last_error,
                "latest_source": self.latest_source,
            }


SESSIONS: Dict[int, CameraSession] = {}
SESSIONS_LOCK = threading.Lock()
AUTH_LOCK = threading.Lock()
AUTH_TOKEN: Optional[str] = BACKEND_ACCESS_TOKEN


def _normalized_backend_api_url() -> str:
    base = BACKEND_API_URL.rstrip("/")
    return base if base.endswith("/api/v1") else f"{base}/api/v1"


def _camera_api_url(camera_id: int) -> str:
    return f"{_normalized_backend_api_url()}/cameras/{camera_id}"


def _resolve_source(source: str) -> str:
    if not isinstance(source, str):
        return source

    if not source.startswith("demo://"):
        return source

    demo_name = source[len("demo://") :].strip().strip("/")
    if not demo_name:
        raise RuntimeError("Demo source is missing a name")

    candidate = (DEMO_ASSETS_DIR / demo_name).resolve()
    if candidate.is_file():
        return str(candidate)

    for suffix in (".mp4", ".mov", ".avi"):
        video_file = candidate.with_suffix(suffix)
        if video_file.is_file():
            return str(video_file)

    raise RuntimeError(f"Demo video not found for source: {source}")


def _login_for_token() -> Optional[str]:
    if not BACKEND_USERNAME or not BACKEND_PASSWORD:
        return None

    response = requests.post(
        f"{_normalized_backend_api_url()}/auth/login",
        data={"username": BACKEND_USERNAME, "password": BACKEND_PASSWORD},
        timeout=10,
    )
    response.raise_for_status()
    payload = response.json()
    return payload.get("access_token")


def _auth_headers() -> Dict[str, str]:
    global AUTH_TOKEN

    if AUTH_TOKEN:
        return {"Authorization": f"Bearer {AUTH_TOKEN}"}

    with AUTH_LOCK:
        if AUTH_TOKEN:
            return {"Authorization": f"Bearer {AUTH_TOKEN}"}
        AUTH_TOKEN = _login_for_token()
        return {"Authorization": f"Bearer {AUTH_TOKEN}"} if AUTH_TOKEN else {}


def _fetch_camera(camera_id: int) -> Dict[str, Any]:
    global AUTH_TOKEN

    url = _camera_api_url(camera_id)
    headers = _auth_headers()
    response = requests.get(url, headers=headers, timeout=10)

    if response.status_code == 401 and BACKEND_USERNAME and BACKEND_PASSWORD:
        with AUTH_LOCK:
            AUTH_TOKEN = _login_for_token()
        headers = _auth_headers()
        response = requests.get(url, headers=headers, timeout=10)

    response.raise_for_status()
    return response.json()


def _session_for(camera_id: int) -> CameraSession:
    with SESSIONS_LOCK:
        session = SESSIONS.get(camera_id)
        if session is None:
            session = CameraSession(camera_id=camera_id)
            SESSIONS[camera_id] = session
        return session


def _store_frame(session: CameraSession, frame_bytes: bytes, status: str, error: Optional[str] = None) -> None:
    with session.lock:
        session.latest_frame = frame_bytes
        session.last_frame_at = _now()
        session.status = status
        session.last_error = error
    session.new_frame.set()


def _maybe_analyze(camera_id: int, frame_bytes: bytes, last_sent_at: float) -> float:
    if not ENABLE_ANALYSIS or not VISION_API_URL:
        return last_sent_at
    if _now() - last_sent_at < ANALYZE_INTERVAL:
        return last_sent_at

    try:
        requests.post(
            VISION_API_URL,
            files={"file": ("frame.jpg", frame_bytes, "image/jpeg")},
            params={"camera_id": camera_id},
            timeout=5,
        )
        return _now()
    except Exception:
        return last_sent_at


def _capture_loop(session: CameraSession) -> None:
    last_sent_at = 0.0

    while not session.stop_event.is_set():
        capture = None
        try:
            camera = _fetch_camera(session.camera_id)
            source = camera.get("rtsp_url")
            if not source:
                raise RuntimeError("Camera has no source URL configured")
            resolved_source = _resolve_source(source)

            with session.lock:
                session.latest_source = source
                session.status = "connecting"
                session.last_error = None
                session.captures_started += 1

            capture = cv2.VideoCapture(resolved_source)
            if not capture.isOpened():
                raise RuntimeError(f"Unable to open source: {source}")

            with session.lock:
                session.status = "streaming"
                session.last_error = None

            while not session.stop_event.is_set():
                ok, frame = capture.read()
                if not ok or frame is None:
                    # If it's a local video file like .mp4, loop it!
                    if isinstance(resolved_source, str) and resolved_source.lower().endswith((".mp4", ".mov", ".avi")):
                        capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
                        continue
                    raise RuntimeError("Stream read failed or video ended")

                encoded, buffer = cv2.imencode(
                    ".jpg",
                    frame,
                    [int(cv2.IMWRITE_JPEG_QUALITY), JPEG_QUALITY],
                )
                if not encoded:
                    raise RuntimeError("Frame encoding failed")

                frame_bytes = buffer.tobytes()
                _store_frame(session, frame_bytes, "streaming")
                last_sent_at = _maybe_analyze(session.camera_id, frame_bytes, last_sent_at)
                time.sleep(FRAME_SLEEP)
        except Exception as exc:
            message = str(exc)
            placeholder = _placeholder_frame(session.camera_id, message)
            _store_frame(session, placeholder, "offline", message)
            time.sleep(RECONNECT_DELAY)
        finally:
            try:
                capture.release()  # type: ignore[name-defined]
            except Exception:
                pass


def _ensure_capture(camera_id: int) -> CameraSession:
    session = _session_for(camera_id)
    with session.lock:
        if session.thread and session.thread.is_alive():
            return session
        session.stop_event.clear()
        session.thread = threading.Thread(
            target=_capture_loop,
            args=(session,),
            daemon=True,
            name=f"camera-relay-{camera_id}",
        )
        session.thread.start()
    return session


def _frame_generator(session: CameraSession):
    with session.lock:
        session.viewers += 1

    try:
        while True:
            frame = session.latest_frame
            if frame is None:
                session.new_frame.wait(timeout=1.0)
                session.new_frame.clear()
                frame = session.latest_frame or _placeholder_frame(session.camera_id, "Waiting for first frame")

            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"
            )
            time.sleep(FRAME_SLEEP)
    finally:
        with session.lock:
            session.viewers = max(0, session.viewers - 1)


@app.get("/")
def root():
    return jsonify(
        {
            "service": "SafeSight Camera Relay",
            "status": "running",
            "analysis_enabled": ENABLE_ANALYSIS,
            "backend_api_url": BACKEND_API_URL,
            "normalized_backend_api_url": _normalized_backend_api_url(),
            "active_sessions": len(SESSIONS),
        }
    )


@app.get("/health")
def health():
    return jsonify(
        {
            "status": "healthy",
            "active_sessions": len(SESSIONS),
            "analysis_enabled": ENABLE_ANALYSIS,
        }
    )


@app.get("/sessions")
def list_sessions():
    return jsonify({"items": [session.to_dict() for session in SESSIONS.values()]})


@app.get("/sessions/<int:camera_id>")
def get_session(camera_id: int):
    session = _session_for(camera_id)
    return jsonify(session.to_dict())


@app.get("/video_feed")
def video_feed():
    camera_id = request.args.get("camera_id", type=int)
    if camera_id is None:
        return jsonify({"detail": "camera_id is required"}), 400

    session = _ensure_capture(camera_id)
    return Response(
        _frame_generator(session),
        mimetype="multipart/x-mixed-replace; boundary=frame",
    )


if __name__ == "__main__":
    print("=" * 60)
    print("SafeSight Camera Relay Node")
    print("=" * 60)
    print(f"Backend API: {_normalized_backend_api_url()}")
    print(f"Analysis enabled: {ENABLE_ANALYSIS}")
    print("Relay feed format: /video_feed?camera_id=<id>")
    print("=" * 60)
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False, threaded=True)
