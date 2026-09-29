import { aiConfig } from "../config/ai";

// The only place in the backend that talks to the Python AI Service
// (docs/decisions/0001-repository-layout.md §5, API.md §64).

interface AiHealthResponse {
  success?: boolean;
  data?: { status?: string };
}

/** Resolves when the AI Service reports healthy; throws otherwise. */
export async function checkHealth(): Promise<void> {
  const response = await fetch(`${aiConfig.baseUrl}/health`, {
    signal: AbortSignal.timeout(aiConfig.healthTimeoutMs),
  });
  if (!response.ok) {
    throw new Error(`AI Service responded with HTTP ${response.status}`);
  }
  const body = (await response.json()) as AiHealthResponse;
  if (body.success !== true || body.data?.status !== "ok") {
    throw new Error("AI Service reported unhealthy");
  }
}
