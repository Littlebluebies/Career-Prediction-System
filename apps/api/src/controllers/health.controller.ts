import type { NextFunction, Request, Response } from "express";

import * as healthService from "../services/health.service";

// Controller Layer: parse request -> call service -> send response (FOLDER_STRUCTURE §13).
// No SQL and no business rules here.

export async function getHealth(
  _req: Request,
  res: Response,
  next: NextFunction,
): Promise<void> {
  try {
    const data = await healthService.getHealth();
    // Always 200: the backend itself is alive; per-component status is in `data`.
    res.status(200).json({ success: true, data });
  } catch (err) {
    // Express 4 does not catch rejected promises by itself.
    next(err);
  }
}
