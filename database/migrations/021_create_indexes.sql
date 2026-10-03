-- =============================================================
-- 021_create_indexes.sql
-- Indexes: DATABASE.md §11, §18, §39 + MIG §38
-- =============================================================

-- Index names follow DATABASE.md. Four indexes that appear only in
-- DATABASE_MIGRATION_PLAN.md §38 use the same naming pattern:
-- idx_occupation_alias_occupation, idx_job_posting_dataset_version,
-- idx_career_result_occupation (and idx_skill_evidence_project from DATABASE.md §18).

-- user_session (DATABASE.md §11)
CREATE INDEX idx_user_session_major ON user_session(major_id);
CREATE INDEX idx_user_session_expires ON user_session(expires_at);
CREATE INDEX idx_user_session_status ON user_session(status);

-- user input (DATABASE.md §39)
CREATE INDEX idx_resume_session ON resume(session_id);
CREATE INDEX idx_portfolio_session ON portfolio(session_id);
CREATE INDEX idx_portfolio_project_portfolio ON portfolio_project(portfolio_id);

-- user skills and evidence (DATABASE.md §18, §39)
CREATE INDEX idx_user_skill_session ON user_skill(session_id);
CREATE INDEX idx_user_skill_skill ON user_skill(skill_id);
CREATE INDEX idx_skill_evidence_user_skill ON skill_evidence(user_skill_id);
CREATE INDEX idx_skill_evidence_project ON skill_evidence(project_id);

-- knowledge (DATABASE.md §39, MIG §38)
CREATE INDEX idx_occupation_family ON occupation(career_family_id);
CREATE INDEX idx_occupation_alias_occupation ON occupation_alias(occupation_id);
CREATE INDEX idx_occupation_skill_occupation ON occupation_skill(occupation_id);
CREATE INDEX idx_occupation_skill_skill ON occupation_skill(skill_id);

-- labour market (DATABASE.md §39, MIG §38)
CREATE INDEX idx_job_posting_occupation ON job_posting(occupation_id);
CREATE INDEX idx_job_posting_dataset_version ON job_posting(dataset_version_id);
CREATE INDEX idx_job_posting_date ON job_posting(date_collected);
CREATE INDEX idx_job_posting_skill_job ON job_posting_skill(job_id);
CREATE INDEX idx_job_posting_skill_skill ON job_posting_skill(skill_id);

-- results (DATABASE.md §39, MIG §38)
CREATE INDEX idx_career_result_session ON career_result(session_id);
CREATE INDEX idx_career_result_rank ON career_result(session_id, rank_position);
CREATE INDEX idx_career_result_occupation ON career_result(occupation_id);
CREATE INDEX idx_skill_gap_result ON skill_gap(result_id);
CREATE INDEX idx_feedback_session ON user_feedback(session_id);
