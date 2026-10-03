-- =============================================================
-- 010_create_dataset_version.sql
-- Dataset version traceability (DATABASE.md §25; MIG §21; ADR 0006)
-- =============================================================

CREATE TABLE dataset_version (
    dataset_version_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    dataset_name TEXT NOT NULL,

    version_name TEXT NOT NULL,

    source_description TEXT,

    collected_at TIMESTAMPTZ,

    processed_at TIMESTAMPTZ,

    record_count INTEGER,

    description TEXT,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT uq_dataset_version
        UNIQUE (dataset_name, version_name)
);
