-- =============================================================
-- 011_create_resume.sql
-- Uploaded resume metadata; file itself stays in storage (DATABASE.md §12; MIG §22)
-- =============================================================

CREATE TABLE resume (
    resume_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    session_id UUID NOT NULL
        REFERENCES user_session(session_id)
        ON DELETE CASCADE,

    file_name TEXT NOT NULL,
    file_type TEXT NOT NULL,
    file_size_bytes BIGINT,

    storage_reference TEXT NOT NULL,

    extracted_text TEXT,

    processing_status TEXT NOT NULL DEFAULT 'PENDING',

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_resume_status
        CHECK (
            processing_status IN (
                'PENDING',
                'PROCESSING',
                'COMPLETED',
                'FAILED'
            )
        )
);
