import dotenv from "dotenv";

// Local development reads apps/api/.env (ENVIRONMENT_SETUP §17).
// In Docker, variables come from docker-compose.yml and no file is needed.
// Values are never hard-coded here (CLAUDE.md §13).
dotenv.config({ quiet: true });

function required(name: string): string {
  const value = process.env[name];
  if (!value) {
    // Fail fast at startup instead of failing later on the first request.
    throw new Error(`Missing required environment variable: ${name}`);
  }
  return value;
}

const frontendPort = process.env.FRONTEND_PORT ?? "3000";

export const env = {
  nodeEnv: process.env.NODE_ENV ?? "development",
  port: Number(process.env.BACKEND_PORT ?? "4000"),
  databaseUrl: required("DATABASE_URL"),
  aiServiceUrl: required("AI_SERVICE_URL"),
  // The browser loads the frontend from this origin (ENVIRONMENT_SETUP §24).
  corsOrigin: `http://localhost:${frontendPort}`,
} as const;
