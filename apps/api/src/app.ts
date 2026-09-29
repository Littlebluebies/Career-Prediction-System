import cors from "cors";
import express, { type Express } from "express";
import helmet from "helmet";

import { env } from "./config/env";
import { errorHandler, notFoundHandler } from "./middlewares/error.middleware";
import { healthRouter } from "./routes/health.routes";

// Builds the Express application. Kept separate from server.ts so the app
// can be created without opening a network port (e.g. in future tests).
export function createApp(): Express {
  const app = express();

  // Security headers
  app.use(helmet());
  // Allow the Next.js frontend (browser) to call this API
  app.use(cors({ origin: env.corsOrigin }));
  // Parse JSON request bodies
  app.use(express.json());

  app.use(healthRouter);
  // Feature routes will be mounted under /api (API.md §3) in later phases.

  // Must be registered last
  app.use(notFoundHandler);
  app.use(errorHandler);

  return app;
}
