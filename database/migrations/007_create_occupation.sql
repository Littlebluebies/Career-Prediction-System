-- =============================================================
-- 007_create_occupation.sql
-- Occupation with source traceability (DATABASE.md §20; MIG §17-18)
-- =============================================================

CREATE TABLE occupation (
    occupation_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    career_family_id BIGINT NOT NULL
        REFERENCES career_family(career_family_id)
        ON DELETE RESTRICT,

    occupation_name TEXT NOT NULL,

    description TEXT,

    source TEXT,

    source_identifier TEXT,

    is_active BOOLEAN NOT NULL DEFAULT TRUE,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT uq_occupation
        UNIQUE (career_family_id, occupation_name)
);
