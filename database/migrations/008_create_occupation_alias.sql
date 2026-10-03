-- =============================================================
-- 008_create_occupation_alias.sql
-- Alternative occupation titles -> canonical occupation (DATABASE.md §21; MIG §19)
-- =============================================================

CREATE TABLE occupation_alias (
    alias_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    occupation_id BIGINT NOT NULL
        REFERENCES occupation(occupation_id)
        ON DELETE CASCADE,

    alias TEXT NOT NULL UNIQUE
);
