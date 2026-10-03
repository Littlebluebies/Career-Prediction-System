-- =============================================================
-- 013_create_portfolio_project.sql
-- Projects found in a portfolio (DATABASE.md §14)
-- =============================================================

CREATE TABLE portfolio_project (
    project_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    portfolio_id BIGINT NOT NULL
        REFERENCES portfolio(portfolio_id)
        ON DELETE CASCADE,

    title TEXT NOT NULL,
    description TEXT,
    url TEXT,
    technologies TEXT,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
