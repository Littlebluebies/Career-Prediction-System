-- =============================================================
-- 001_create_schema.sql
-- Application schema (DATABASE.md §4, §9; DATABASE_MIGRATION_PLAN.md §10)
-- =============================================================

CREATE SCHEMA IF NOT EXISTS career_system;

-- Defaults for every NEW connection to this database:
--   * search_path: unqualified names resolve to career_system first,
--     so the backend and later migrations can write `major`, not `career_system.major`
--   * timezone: store and compare TIMESTAMPTZ in UTC (DATABASE.md §4)
-- current_database() keeps this file independent of the database name
-- (career_system for development, career_system_test for tests).
DO $$
BEGIN
    EXECUTE format('ALTER DATABASE %I SET search_path TO career_system, public', current_database());
    EXECUTE format('ALTER DATABASE %I SET timezone TO %L', current_database(), 'UTC');
END
$$;
