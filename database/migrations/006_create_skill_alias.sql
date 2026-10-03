-- =============================================================
-- 006_create_skill_alias.sql
-- Raw skill name -> canonical skill (DATABASE.md §16; MIG §16)
-- =============================================================

CREATE TABLE skill_alias (
    alias_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    skill_id BIGINT NOT NULL
        REFERENCES skill(skill_id)
        ON DELETE CASCADE,

    alias TEXT NOT NULL UNIQUE
);
