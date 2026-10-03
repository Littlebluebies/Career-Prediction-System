-- =============================================================
-- 002_create_major.sql
-- Faculty majors; context only, never a hard filter (DATABASE.md §10, §32; MIG §11-12)
-- =============================================================

CREATE TABLE major (
    major_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    branch_name TEXT NOT NULL,
    major_name TEXT NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT uq_major
        UNIQUE (branch_name, major_name)
);
