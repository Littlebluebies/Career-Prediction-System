-- =============================================================
-- 003_create_user_session.sql
-- Temporary session, no login (DATABASE.md §11; MIG §13)
-- =============================================================

CREATE TABLE user_session (
    session_id UUID PRIMARY KEY,
    major_id BIGINT REFERENCES major(major_id)
        ON DELETE SET NULL,

    consent_given BOOLEAN NOT NULL DEFAULT FALSE,
    consent_given_at TIMESTAMPTZ,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    expires_at TIMESTAMPTZ NOT NULL,

    status TEXT NOT NULL DEFAULT 'ACTIVE',

    CONSTRAINT chk_session_status
        CHECK (
            status IN (
                'ACTIVE',
                'PROCESSING',
                'COMPLETED',
                'EXPIRED',
                'DELETED',
                'ERROR'
            )
        )
);
