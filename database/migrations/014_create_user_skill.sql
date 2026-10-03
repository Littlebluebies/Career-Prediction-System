-- =============================================================
-- 014_create_user_skill.sql
-- Skills detected for a session (DATABASE.md §17)
-- =============================================================

CREATE TABLE user_skill (
    user_skill_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    session_id UUID NOT NULL
        REFERENCES user_session(session_id)
        ON DELETE CASCADE,

    skill_id BIGINT NOT NULL
        REFERENCES skill(skill_id)
        ON DELETE RESTRICT,

    confidence NUMERIC(5,4),

    source TEXT NOT NULL,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT uq_user_skill
        UNIQUE (session_id, skill_id),

    CONSTRAINT chk_user_skill_source
        CHECK (
            source IN (
                'RESUME',
                'PORTFOLIO',
                'BOTH'
            )
        ),

    CONSTRAINT chk_user_skill_confidence
        CHECK (
            confidence IS NULL
            OR confidence BETWEEN 0 AND 1
        )
);
