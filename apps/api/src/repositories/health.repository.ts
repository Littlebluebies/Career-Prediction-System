import { pool } from "../config/database";

// Repository Layer: the only layer that runs SQL (CLAUDE.md §12).

/** Resolves when PostgreSQL answers a trivial query; throws otherwise. */
export async function ping(): Promise<void> {
  await pool.query("SELECT 1");
}
