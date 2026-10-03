-- =============================================================
-- 017_create_job_posting_skill.sql
-- Skills extracted from job postings (DATABASE.md §24)
-- =============================================================

CREATE TABLE job_posting_skill (
    job_posting_skill_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    job_id BIGINT NOT NULL
        REFERENCES job_posting(job_id)
        ON DELETE CASCADE,

    skill_id BIGINT NOT NULL
        REFERENCES skill(skill_id)
        ON DELETE RESTRICT,

    confidence NUMERIC(5,4),

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT uq_job_posting_skill
        UNIQUE (job_id, skill_id),

    CONSTRAINT chk_job_skill_confidence
        CHECK (
            confidence IS NULL
            OR confidence BETWEEN 0 AND 1
        )
);
