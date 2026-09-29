import { createApp } from "./app";
import { pool } from "./config/database";
import { env } from "./config/env";

// Entry point: open the network port (ENVIRONMENT_SETUP §24: backend = 4000).
const app = createApp();

const server = app.listen(env.port, () => {
  console.log(`[backend] listening on port ${env.port} (${env.nodeEnv})`);
});

// Graceful shutdown: `docker stop` sends SIGTERM, Ctrl+C sends SIGINT.
// Stop accepting requests, then close database connections, then exit.
function shutdown(signal: string): void {
  console.log(`[backend] ${signal} received, shutting down`);
  server.close(() => {
    pool.end().finally(() => process.exit(0));
  });
}

process.on("SIGTERM", () => shutdown("SIGTERM"));
process.on("SIGINT", () => shutdown("SIGINT"));
