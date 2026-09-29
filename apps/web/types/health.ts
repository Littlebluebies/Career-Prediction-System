// Shape of `data` returned by the backend GET /health
// (apps/api/src/services/health.service.ts, ENVIRONMENT_SETUP §32, §40).

export type ComponentStatus = "ok" | "error";

export interface BackendHealth {
  status: "ok" | "degraded";
  backend: "ok";
  database: ComponentStatus;
  ai_service: ComponentStatus;
}
