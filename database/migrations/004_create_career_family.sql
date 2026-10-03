-- =============================================================
-- 004_create_career_family.sql
-- Career family level between faculty and occupation (DATABASE.md §19; MIG §14)
-- =============================================================

CREATE TABLE career_family (
    career_family_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    family_code TEXT NOT NULL UNIQUE,

    family_name TEXT NOT NULL,

    description TEXT,

    is_active BOOLEAN NOT NULL DEFAULT TRUE,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
