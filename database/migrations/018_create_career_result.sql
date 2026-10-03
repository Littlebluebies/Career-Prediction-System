-- =============================================================
-- 018_create_career_result.sql
-- Career recommendation per session; score = match score, not employment probability (DATABASE.md §26, §53)
-- =============================================================

CREATE TABLE career_result (
    result_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    session_id UUID NOT NULL
        REFERENCES user_session(session_id)
        ON DELETE CASCADE,

    occupation_id BIGINT NOT NULL
        REFERENCES occupation(occupation_id)
        ON DELETE RESTRICT,

    score NUMERIC(7,4),

    rank_position INTEGER NOT NULL,

    explanation TEXT,

    algorithm_version TEXT,

    dataset_version_id BIGINT
        REFERENCES dataset_version(dataset_version_id)
        ON DELETE SET NULL,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_career_rank
        CHECK (rank_position > 0),

    CONSTRAINT chk_career_score
        CHECK (
            score IS NULL
            OR score >= 0
        ),

    CONSTRAINT uq_session_occupation_result
        UNIQUE (session_id, occupation_id)
);
