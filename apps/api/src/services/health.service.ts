import * as pythonClient from "../clients/python.client";
import * as healthRepository from "../repositories/health.repository";

// Service Layer: decides what "healthy" means (CLAUDE.md §12).
// Response shape combines ENVIRONMENT_SETUP §32 (status) and §40 (per component).

export type ComponentStatus = "ok" | "error";

export interface HealthReport {
  status: "ok" | "degraded";
  backend: "ok";
  database: ComponentStatus;
  ai_service: ComponentStatus;
}

// Turns "resolves / throws" into "ok / error".
// The error detail is intentionally dropped: health output must not
// expose sensitive information (ENVIRONMENT_SETUP §40).
async function check(probe: () => Promise<void>): Promise<ComponentStatus> {
  try {
    await probe();
    return "ok";
  } catch {
    return "error";
  }
}

export async function getHealth(): Promise<HealthReport> {
  // Both checks run in parallel, so the slowest one sets the total time.
  const [database, aiService] = await Promise.all([
    check(healthRepository.ping),
    check(pythonClient.checkHealth),
  ]);

  return {
    status: database === "ok" && aiService === "ok" ? "ok" : "degraded",
    backend: "ok",
    database,
    ai_service: aiService,
  };
}
