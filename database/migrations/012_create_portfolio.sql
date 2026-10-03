-- =============================================================
-- 012_create_portfolio.sql
-- Portfolio URL and access status (DATABASE.md §13)
-- =============================================================

CREATE TABLE portfolio (
    portfolio_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    session_id UUID NOT NULL
        REFERENCES user_session(session_id)
        ON DELETE CASCADE,

    url TEXT NOT NULL,
    platform TEXT,

    status TEXT NOT NULL DEFAULT 'PENDING',

    accessible BOOLEAN,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_portfolio_status
        CHECK (
            status IN (
                'PENDING',
                'ACCESSIBLE',
                'INACCESSIBLE',
                'INVALID',
                'BLOCKED',
                'LOGIN_REQUIRED',
                'UNSUPPORTED',
                'ERROR'
            )
        )
);
