-- =============================================================
-- 015_create_skill_evidence.sql
-- Evidence supporting a user skill (DATABASE.md §18, §33)
-- =============================================================

CREATE TABLE skill_evidence (
    evidence_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    user_skill_id BIGINT NOT NULL
        REFERENCES user_skill(user_skill_id)
        ON DELETE CASCADE,

    source_type TEXT NOT NULL,

    source_reference TEXT,

    project_id BIGINT
        REFERENCES portfolio_project(project_id)
        ON DELETE SET NULL,

    evidence_text TEXT,

    confidence NUMERIC(5,4),

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_evidence_source
        CHECK (
            source_type IN (
                'RESUME_SKILL',
                'RESUME_PROJECT',
                'RESUME_EXPERIENCE',
                'RESUME_CERTIFICATE',
                'PORTFOLIO_PROJECT',
                'PORTFOLIO_DESCRIPTION',
                'PORTFOLIO_TECHNOLOGY',
                'PORTFOLIO_ARTIFACT'
            )
        ),

    CONSTRAINT chk_evidence_confidence
        CHECK (
            confidence IS NULL
            OR confidence BETWEEN 0 AND 1
        )
);
