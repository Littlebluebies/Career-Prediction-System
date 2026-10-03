-- =============================================================
-- 005_create_skill.sql
-- Canonical skill dictionary (DATABASE.md §15; MIG §15)
-- =============================================================

CREATE TABLE skill (
    skill_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    skill_name TEXT NOT NULL UNIQUE,

    category TEXT NOT NULL,

    description TEXT,

    is_active BOOLEAN NOT NULL DEFAULT TRUE,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_skill_category
        CHECK (
            category IN (
                'TECHNICAL',
                'DESIGN',
                'CREATIVE',
                'SOFTWARE_TOOL',
                'COMMUNICATION',
                'BUSINESS',
                'OTHER'
            )
        )
);
