-- =============================================================
-- 009_create_occupation_skill.sql
-- Occupation <-> skill with importance and demand (DATABASE.md §22; MIG §20)
-- =============================================================

CREATE TABLE occupation_skill (
    occupation_skill_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    occupation_id BIGINT NOT NULL
        REFERENCES occupation(occupation_id)
        ON DELETE CASCADE,

    skill_id BIGINT NOT NULL
        REFERENCES skill(skill_id)
        ON DELETE RESTRICT,

    importance NUMERIC(5,4),

    demand NUMERIC(5,4),

    source TEXT,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT uq_occupation_skill
        UNIQUE (occupation_id, skill_id),

    CONSTRAINT chk_importance
        CHECK (
            importance IS NULL
            OR importance BETWEEN 0 AND 1
        ),

    CONSTRAINT chk_demand
        CHECK (
            demand IS NULL
            OR demand BETWEEN 0 AND 1
        )
);
