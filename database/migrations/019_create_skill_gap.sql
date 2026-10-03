-- =============================================================
-- 019_create_skill_gap.sql
-- Skill gap per career result; EVIDENCE_NOT_FOUND, never 'missing skill' (DATABASE.md §27, §34)
-- =============================================================

CREATE TABLE skill_gap (
    gap_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    result_id BIGINT NOT NULL
        REFERENCES career_result(result_id)
        ON DELETE CASCADE,

    skill_id BIGINT NOT NULL
        REFERENCES skill(skill_id)
        ON DELETE RESTRICT,

    status TEXT NOT NULL,

    priority TEXT,

    reason TEXT,

    guidance TEXT,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT uq_result_skill_gap
        UNIQUE (result_id, skill_id),

    CONSTRAINT chk_skill_gap_status
        CHECK (
            status IN (
                'MATCHED',
                'PARTIAL',
                'EVIDENCE_NOT_FOUND'
            )
        ),

    CONSTRAINT chk_skill_gap_priority
        CHECK (
            priority IS NULL
            OR priority IN (
                'HIGH',
                'MEDIUM',
                'LOW'
            )
        )
);
