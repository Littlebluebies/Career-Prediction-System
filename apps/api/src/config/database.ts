import { Pool } from "pg";

import { env } from "./env";

// One shared connection pool for the whole backend (docs/decisions/0003-database-tooling.md §5).
// Only the Repository Layer may run SQL through it (CLAUDE.md §12).
export const pool = new Pool({
  connectionString: env.databaseUrl,
  // Give up quickly when PostgreSQL is unreachable instead of hanging.
  connectionTimeoutMillis: 3000,
});

// An idle client can lose its connection (e.g. PostgreSQL restarts).
// Without this listener, that error would crash the whole process.
pool.on("error", (err) => {
  console.error("[database] idle client error:", err.message);
});
