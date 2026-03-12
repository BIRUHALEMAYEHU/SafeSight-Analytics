"use client";

import { useAuth } from "@/contexts/AuthContext";
import { useRouter } from "next/navigation";
import { useEffect, useState, useRef } from "react";
import Sidebar from "@/components/Sidebar";

interface Person {
  id: number;
  name: string;
  type: string;
  notes: string | null;
  photo_path: string | null;
  created_at: string;
}

const API_URL =
  process.env.NEXT_PUBLIC_API_URL
    ? `${process.env.NEXT_PUBLIC_API_URL}/api/v1`
    : typeof window !== "undefined" && window.location.hostname !== "localhost"
    ? "https://safesight-backend.onrender.com/api/v1"
    : "http://localhost:8000/api/v1";

const BACKEND_BASE =
  process.env.NEXT_PUBLIC_API_URL ||
  (typeof window !== "undefined" && window.location.hostname !== "localhost"
    ? "https://safesight-backend.onrender.com"
    : "http://localhost:8000");

const TYPE_COLORS: Record<string, string> = {
  wanted: "bg-red-500/20 text-red-400 border-red-800",
  vip: "bg-yellow-500/20 text-yellow-400 border-yellow-800",
  banned: "bg-orange-500/20 text-orange-400 border-orange-800",
  staff: "bg-blue-500/20 text-blue-400 border-blue-800",
};

export default function PersonsPage() {
  const { user, status } = useAuth();
  const router = useRouter();
  const [persons, setPersons] = useState<Person[]>([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [form, setForm] = useState({ name: "", type: "wanted", notes: "" });
  const [photoFile, setPhotoFile] = useState<File | null>(null);
  const [error, setError] = useState("");
  const fileRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (status === "unauthenticated") router.push("/login");
  }, [status, router]);

  useEffect(() => {
    if (status === "authenticated") fetchPersons();
  }, [status]);

  async function fetchPersons() {
    setLoading(true);
    try {
      const token = localStorage.getItem("access_token");
      const res = await fetch(`${API_URL}/persons`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (res.ok) setPersons(await res.json());
    } catch (e) {
      console.error("Failed to fetch persons", e);
    } finally {
      setLoading(false);
    }
  }

  async function handleAdd() {
    setError("");
    const token = localStorage.getItem("access_token");
    const data = new FormData();
    data.append("name", form.name);
    data.append("type", form.type);
    if (form.notes) data.append("notes", form.notes);
    if (photoFile) data.append("photo", photoFile);

    try {
      const res = await fetch(`${API_URL}/persons`, {
        method: "POST",
        headers: { Authorization: `Bearer ${token}` },
        body: data,
      });
      if (!res.ok) {
        const err = await res.json();
        setError(err.detail || "Failed to add person");
        return;
      }
      setShowModal(false);
      setForm({ name: "", type: "wanted", notes: "" });
      setPhotoFile(null);
      fetchPersons();
    } catch {
      setError("Network error");
    }
  }

  async function handleDelete(id: number) {
    if (!confirm("Remove this person from the database?")) return;
    const token = localStorage.getItem("access_token");
    await fetch(`${API_URL}/persons/${id}`, {
      method: "DELETE",
      headers: { Authorization: `Bearer ${token}` },
    });
    fetchPersons();
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
            <h1 className="font-mono text-3xl font-bold text-cyan-400">Threat Database</h1>
            <p className="font-mono text-sm text-slate-500">Known persons of interest for face recognition</p>
          </div>
          <button
            onClick={() => { setShowModal(true); setError(""); }}
            className="rounded border border-cyan-500 bg-cyan-500/10 px-4 py-2 font-mono text-sm text-cyan-400 hover:bg-cyan-500/20 transition-colors"
          >
            + Add Person
          </button>
        </div>

        {/* Persons Grid */}
        {loading ? (
          <div className="font-mono text-slate-400">Loading records...</div>
        ) : persons.length === 0 ? (
          <div className="rounded border border-slate-800 bg-slate-900 p-8 text-center font-mono text-slate-500">
            No persons in database. Add a person above to enable face recognition.
          </div>
        ) : (
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
            {persons.map((p) => (
              <div key={p.id} className="rounded border border-slate-800 bg-slate-900 p-4">
                {/* Photo */}
                <div className="mb-3 flex h-24 items-center justify-center rounded border border-slate-700 bg-slate-800 overflow-hidden">
                  {p.photo_path ? (
                    <img
                      src={`${BACKEND_BASE}${p.photo_path}`}
                      alt={p.name}
                      className="h-full w-full object-cover"
                    />
                  ) : (
                    <span className="text-3xl">👤</span>
                  )}
                </div>
                <p className="mb-1 font-mono text-sm font-semibold text-slate-200">{p.name}</p>
                <span className={`mb-2 inline-block rounded border px-2 py-0.5 font-mono text-xs ${TYPE_COLORS[p.type] || "bg-slate-700 text-slate-400"}`}>
                  {p.type.toUpperCase()}
                </span>
                {p.notes && <p className="mb-2 font-mono text-xs text-slate-500 line-clamp-2">{p.notes}</p>}
                <button
                  onClick={() => handleDelete(p.id)}
                  className="mt-2 w-full rounded border border-red-900 bg-red-900/20 py-1 font-mono text-xs text-red-400 hover:bg-red-900/40 transition-colors"
                >
                  Remove
                </button>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Add Modal */}
      {showModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70">
          <div className="w-full max-w-md rounded border border-slate-700 bg-slate-900 p-6">
            <h2 className="mb-4 font-mono text-lg font-semibold text-cyan-400">Add Person of Interest</h2>
            <div className="space-y-3">
              <div>
                <label className="mb-1 block font-mono text-xs text-slate-400">Full Name</label>
                <input
                  className="w-full rounded border border-slate-700 bg-slate-800 px-3 py-2 font-mono text-sm text-slate-200 focus:border-cyan-500 focus:outline-none"
                  value={form.name}
                  onChange={(e) => setForm({ ...form, name: e.target.value })}
                  placeholder="e.g. John Doe"
                />
              </div>
              <div>
                <label className="mb-1 block font-mono text-xs text-slate-400">Classification</label>
                <select
                  className="w-full rounded border border-slate-700 bg-slate-800 px-3 py-2 font-mono text-sm text-slate-200 focus:border-cyan-500 focus:outline-none"
                  value={form.type}
                  onChange={(e) => setForm({ ...form, type: e.target.value })}
                >
                  <option value="wanted">Wanted</option>
                  <option value="vip">VIP</option>
                  <option value="banned">Banned</option>
                  <option value="staff">Staff</option>
                </select>
              </div>
              <div>
                <label className="mb-1 block font-mono text-xs text-slate-400">Notes (optional)</label>
                <textarea
                  className="w-full rounded border border-slate-700 bg-slate-800 px-3 py-2 font-mono text-sm text-slate-200 focus:border-cyan-500 focus:outline-none"
                  value={form.notes}
                  onChange={(e) => setForm({ ...form, notes: e.target.value })}
                  rows={2}
                  placeholder="Additional information..."
                />
              </div>
              <div>
                <label className="mb-1 block font-mono text-xs text-slate-400">Photo (optional — required for recognition)</label>
                <button
                  className="w-full rounded border border-dashed border-slate-600 bg-slate-800 py-3 font-mono text-xs text-slate-400 hover:border-cyan-500 hover:text-cyan-400 transition-colors"
                  onClick={() => fileRef.current?.click()}
                >
                  {photoFile ? `✓ ${photoFile.name}` : "Click to upload photo"}
                </button>
                <input
                  ref={fileRef}
                  type="file"
                  accept="image/*"
                  className="hidden"
                  onChange={(e) => setPhotoFile(e.target.files?.[0] || null)}
                />
              </div>
              {error && <p className="font-mono text-xs text-red-400">{error}</p>}
            </div>
            <div className="mt-4 flex gap-3">
              <button onClick={handleAdd} className="flex-1 rounded bg-cyan-500 py-2 font-mono text-sm font-semibold text-slate-900 hover:bg-cyan-400 transition-colors">
                Add
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
