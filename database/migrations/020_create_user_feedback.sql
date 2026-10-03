-- =============================================================
-- 020_create_user_feedback.sql
-- User feedback and SUS (DATABASE.md §28)
-- =============================================================

CREATE TABLE user_feedback (
    feedback_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    session_id UUID NOT NULL
        REFERENCES user_session(session_id)
        ON DELETE CASCADE,

    sus_score NUMERIC(5,2),

    satisfaction NUMERIC(5,2),

    comment TEXT,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_sus_score
        CHECK (
            sus_score IS NULL
            OR sus_score BETWEEN 0 AND 100
        ),

    CONSTRAINT chk_satisfaction
        CHECK (
            satisfaction IS NULL
            OR satisfaction BETWEEN 0 AND 100
        )
);
