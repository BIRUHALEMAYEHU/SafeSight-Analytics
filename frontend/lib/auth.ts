export interface User {
    id: string;
    username: string;
    email: string;
    full_name: string | null;
    role: string;
}

const API_URL = process.env.NEXT_PUBLIC_API_URL
    ? `${process.env.NEXT_PUBLIC_API_URL}/api/v1`
    : (typeof window !== "undefined" && window.location.hostname !== "localhost"
        ? "https://safesight-backend.onrender.com/api/v1"
        : "http://localhost:8000/api/v1");

export async function login(username: string, password: string): Promise<void> {
    const formData = new URLSearchParams();
    formData.append("username", username);
    formData.append("password", password);

    const response = await fetch(`${API_URL}/auth/login`, {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
        body: formData.toString(),
    });

    if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: "Login failed" }));
        throw new Error(error.detail || "Login failed");
    }

    const data = await response.json();
    localStorage.setItem("access_token", data.access_token);
}

export function logout(): void {
    localStorage.removeItem("access_token");
    // Force a storage event for cross-tab sync
    window.dispatchEvent(new Event("storage"));
}

export async function ensureSession(): Promise<User | null> {
    if (typeof window === "undefined") return null;

    const token = localStorage.getItem("access_token");
    if (!token) return null;

    try {
        const response = await fetch(`${API_URL}/auth/me`, {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        });

        if (!response.ok) {
            localStorage.removeItem("access_token");
            return null;
        }

        return await response.json();
    } catch (error) {
        console.error("Session check failed:", error);
        return null;
    }
}
