import { env } from "./env";

// Settings for calling the internal Python AI Service (API.md §34-35).
export const aiConfig = {
  baseUrl: env.aiServiceUrl,
  healthTimeoutMs: 3000,
} as const;
