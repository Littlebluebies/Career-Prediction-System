import type { ErrorRequestHandler, RequestHandler } from "express";

// Error responses follow the Standard Response Format (API.md §6).

export const notFoundHandler: RequestHandler = (_req, res) => {
  res.status(404).json({
    success: false,
    error: { code: "NOT_FOUND", message: "Resource not found", details: null },
  });
};

// eslint-disable-next-line @typescript-eslint/no-unused-vars -- Express recognises an error handler only when it has 4 parameters
export const errorHandler: ErrorRequestHandler = (err, _req, res, _next) => {
  // Full detail goes to the server log only, never to the client.
  console.error(err);
  res.status(500).json({
    success: false,
    error: {
      code: "INTERNAL_SERVER_ERROR",
      message: "Internal server error",
      details: null,
    },
  });
};
