"use client";

import { useAuth } from "@/contexts/AuthContext";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import Sidebar from "@/components/Sidebar";

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

export default function CamerasPage() {
  const { user, status } = useAuth();
  const router = useRouter();
  const [cameras, setCameras] = useState<Camera[]>([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [editCamera, setEditCamera] = useState<Camera | null>(null);
  const [form, setForm] = useState({ name: "", rtsp_url: "", location: "", is_active: true });
  const [error, setError] = useState("");

  useEffect(() => {
    if (status === "unauthenticated") router.push("/login");
  }, [status, router]);

  useEffect(() => {
    if (status === "authenticated") fetchCameras();
  }, [status]);

  async function fetchCameras() {
    setLoading(true);
    try {
      const token = localStorage.getItem("access_token");
      const res = await fetch(`${API_URL}/cameras`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (res.ok) setCameras(await res.json());
    } catch (e) {
      console.error("Failed to fetch cameras", e);
    } finally {
      setLoading(false);
    }
  }

  function openAdd() {
    setEditCamera(null);
    setForm({ name: "", rtsp_url: "", location: "", is_active: true });
    setError("");
    setShowModal(true);
  }

  function openEdit(cam: Camera) {
    setEditCamera(cam);
    setForm({ name: cam.name, rtsp_url: cam.rtsp_url, location: cam.location, is_active: cam.is_active });
    setError("");
    setShowModal(true);
  }

  async function handleSave() {
    setError("");
    const token = localStorage.getItem("access_token");
    try {
      const res = await fetch(
        editCamera ? `${API_URL}/cameras/${editCamera.id}` : `${API_URL}/cameras`,
        {
          method: editCamera ? "PUT" : "POST",
          headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
          body: JSON.stringify(form),
        }
      );
      if (!res.ok) {
        const err = await res.json();
        setError(err.detail || "Failed to save camera");
        return;
      }
      setShowModal(false);
      fetchCameras();
    } catch {
      setError("Network error");
    }
  }

  async function handleDelete(id: number) {
    if (!confirm("Delete this camera?")) return;
    const token = localStorage.getItem("access_token");
    await fetch(`${API_URL}/cameras/${id}`, {
      method: "DELETE",
      headers: { Authorization: `Bearer ${token}` },
    });
    fetchCameras();
  }

  if (status === "loading") return <div className="flex min-h-screen items-center justify-center bg-slate-950 text-slate-400 font-mono">Loading...</div>;
  if (!user) return null;

  return (
    <div className="min-h-screen bg-slate-950">
      <Sidebar />
      <div className="ml-80 min-h-screen p-6">
        {/* Header */}
        <div className="mb-6 flex items-center justify-between">
          <div>
            <h1 className="font-mono text-3xl font-bold text-cyan-400">Vision Nodes</h1>
            <p className="font-mono text-sm text-slate-500">Manage surveillance camera feeds</p>
          </div>
          <button
            onClick={openAdd}
            className="rounded border border-cyan-500 bg-cyan-500/10 px-4 py-2 font-mono text-sm text-cyan-400 hover:bg-cyan-500/20 transition-colors"
          >
            + Add Camera
          </button>
        </div>

        {/* Camera Grid */}
        {loading ? (
          <div className="font-mono text-slate-400">Scanning nodes...</div>
        ) : cameras.length === 0 ? (
          <div className="rounded border border-slate-800 bg-slate-900 p-8 text-center font-mono text-slate-500">
            No cameras registered. Add your first camera above.
          </div>
        ) : (
          <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
            {cameras.map((cam) => (
              <div key={cam.id} className="rounded border border-slate-800 bg-slate-900 p-4">
                <div className="mb-3 flex items-center justify-between">
                  <span className="font-mono text-sm font-semibold text-cyan-300">{cam.name}</span>
                  <span className={`rounded px-2 py-0.5 font-mono text-xs ${cam.is_active ? "bg-green-500/20 text-green-400" : "bg-red-500/20 text-red-400"}`}>
                    {cam.is_active ? "● ACTIVE" : "● OFFLINE"}
                  </span>
                </div>
                <p className="mb-1 font-mono text-xs text-slate-500">📍 {cam.location || "Unknown"}</p>
                <p className="mb-4 truncate font-mono text-xs text-slate-600">{cam.rtsp_url}</p>
                <div className="flex gap-2">
                  <button
                    onClick={() => openEdit(cam)}
                    className="flex-1 rounded border border-slate-700 bg-slate-800 py-1.5 font-mono text-xs text-slate-300 hover:bg-slate-700 transition-colors"
                  >
                    Edit
                  </button>
                  <button
                    onClick={() => handleDelete(cam.id)}
                    className="flex-1 rounded border border-red-900 bg-red-900/20 py-1.5 font-mono text-xs text-red-400 hover:bg-red-900/40 transition-colors"
                  >
                    Delete
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70">
          <div className="w-full max-w-md rounded border border-slate-700 bg-slate-900 p-6">
            <h2 className="mb-4 font-mono text-lg font-semibold text-cyan-400">
              {editCamera ? "Edit Camera" : "Add Camera"}
            </h2>
            <div className="space-y-3">
              {[
                { label: "Camera Name", key: "name", placeholder: "e.g. Front Entrance" },
                { label: "RTSP URL", key: "rtsp_url", placeholder: "rtsp://..." },
                { label: "Location", key: "location", placeholder: "e.g. Building A - Floor 1" },
              ].map(({ label, key, placeholder }) => (
                <div key={key}>
                  <label className="mb-1 block font-mono text-xs text-slate-400">{label}</label>
                  <input
                    className="w-full rounded border border-slate-700 bg-slate-800 px-3 py-2 font-mono text-sm text-slate-200 focus:border-cyan-500 focus:outline-none"
                    value={form[key as keyof typeof form] as string}
                    onChange={(e) => setForm({ ...form, [key]: e.target.value })}
                    placeholder={placeholder}
                  />
                </div>
              ))}
              <div className="flex items-center gap-2">
                <input
                  type="checkbox"
                  id="is_active"
                  checked={form.is_active}
                  onChange={(e) => setForm({ ...form, is_active: e.target.checked })}
                  className="accent-cyan-500"
                />
                <label htmlFor="is_active" className="font-mono text-xs text-slate-400">Active</label>
              </div>
              {error && <p className="font-mono text-xs text-red-400">{error}</p>}
            </div>
            <div className="mt-4 flex gap-3">
              <button onClick={handleSave} className="flex-1 rounded bg-cyan-500 py-2 font-mono text-sm font-semibold text-slate-900 hover:bg-cyan-400 transition-colors">
                Save
              </button>
              <button onClick={() => setShowModal(false)} className="flex-1 rounded border border-slate-700 py-2 font-mono text-sm text-slate-400 hover:bg-slate-800 transition-colors">
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
