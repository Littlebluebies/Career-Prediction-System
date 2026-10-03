-- =============================================================
-- 016_create_job_posting.sql
-- Job postings with source and dataset version (DATABASE.md §23, §25; MIG §29)
-- =============================================================

-- DATABASE.md §25 adds fk_job_posting_dataset_version with a separate ALTER TABLE
-- because there job_posting is defined before dataset_version. In the migration
-- order (MIG §5) dataset_version already exists (010), so the same named
-- constraint is declared inline here. The resulting schema is identical.
CREATE TABLE job_posting (
    job_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    job_title TEXT NOT NULL,

    company TEXT,

    description TEXT,

    requirements TEXT,

    experience TEXT,

    location TEXT,

    source TEXT NOT NULL,

    source_url TEXT,

    date_collected TIMESTAMPTZ NOT NULL,

    occupation_id BIGINT
        REFERENCES occupation(occupation_id)
        ON DELETE SET NULL,

    dataset_version_id BIGINT,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_job_posting_dataset_version
        FOREIGN KEY (dataset_version_id)
        REFERENCES dataset_version(dataset_version_id)
        ON DELETE SET NULL
);
