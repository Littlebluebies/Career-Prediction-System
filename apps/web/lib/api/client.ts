import type { BackendHealth } from "@/types/health";

// HTTP configuration for calling the Express backend (FOLDER_STRUCTURE §9).
// Components must not call fetch() directly; they call functions from lib/api/.
// The frontend never talks to PostgreSQL or the Python service (CLAUDE.md §5).

// Inlined into the browser bundle at build time because of the NEXT_PUBLIC_ prefix
// (API.md §3, ENVIRONMENT_SETUP §16).
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;

function requireBaseUrl(): string {
  if (!API_BASE_URL) {
    throw new Error("NEXT_PUBLIC_API_BASE_URL is not set");
  }
  return API_BASE_URL;
}

interface SuccessResponse<T> {
  success: true;
  data: T;
}

/** Calls the backend health check (ENVIRONMENT_SETUP §32, §40). */
export async function getBackendHealth(): Promise<BackendHealth> {
  // Feature APIs live under /api, but /health is at the backend root,
  // so use only the origin (scheme + host + port) of the base URL.
  const origin = new URL(requireBaseUrl()).origin;

  const response = await fetch(`${origin}/health`, { cache: "no-store" });
  if (!response.ok) {
    throw new Error(`Backend responded with HTTP ${response.status}`);
  }
  const body = (await response.json()) as SuccessResponse<BackendHealth>;
  return body.data;
}
