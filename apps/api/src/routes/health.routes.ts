import { Router } from "express";

import { getHealth } from "../controllers/health.controller";

// Route Layer: map HTTP method + path to a controller (CLAUDE.md §12).
export const healthRouter = Router();

// GET /health lives at the root, not under /api (ENVIRONMENT_SETUP §32).
healthRouter.get("/health", getHealth);
