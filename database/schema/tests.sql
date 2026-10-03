-- =============================================================
-- tests.sql — database tests (run by scripts/database/test.sh)
-- Sources: DATABASE_MIGRATION_PLAN §49 (Test 1-5), §73;
--          DATABASE.md §38, §59, §62; CLAUDE.md §6
--
-- Runs inside ONE transaction that is rolled back at the end,
-- on the throw-away database career_system_test.
-- Every check prints "INFO: PASS ..." or raises "FAIL ..." and stops.
-- =============================================================

BEGIN;
SET search_path TO career_system, public;

-- ---------- helpers (temporary, disappear with the session) ----------

CREATE FUNCTION pg_temp.check(ok boolean, label text) RETURNS void
LANGUAGE plpgsql AS $$
BEGIN
    IF ok IS TRUE THEN
        RAISE INFO 'PASS  %', label;
    ELSE
        RAISE EXCEPTION 'FAIL  %', label;
    END IF;
END $$;

-- Runs a statement that MUST fail with the given SQLSTATE:
--   23502 not_null_violation   23503 foreign_key_violation
--   23505 unique_violation     23514 check_violation
CREATE FUNCTION pg_temp.expect_error(stmt text, expected_state text, label text) RETURNS void
LANGUAGE plpgsql AS $$
BEGIN
    BEGIN
        EXECUTE stmt;
    EXCEPTION WHEN OTHERS THEN
        IF SQLSTATE = expected_state THEN
            RAISE INFO 'PASS  % (rejected: %)', label, SQLSTATE;
            RETURN;
        END IF;
        RAISE EXCEPTION 'FAIL  % (expected %, got %: %)', label, expected_state, SQLSTATE, SQLERRM;
    END;
    RAISE EXCEPTION 'FAIL  % (expected error %, but statement succeeded)', label, expected_state;
END $$;

-- =============================================================
-- Test 1 / 2 — Fresh database and migration order (MIG §49)
-- =============================================================

SELECT pg_temp.check(
    (SELECT count(*) FROM public.schema_migrations) = :expected_migrations,
    'T1 all migration files applied on a fresh database');

SELECT pg_temp.check(
    (SELECT array_agg(version ORDER BY applied_at, version) FROM public.schema_migrations)
  = (SELECT array_agg(version ORDER BY version) FROM public.schema_migrations),
    'T2 migrations applied in numeric order');

SELECT pg_temp.check(
    (SELECT count(*) FROM information_schema.schemata WHERE schema_name = 'career_system') = 1,
    'T2 schema career_system exists');

SELECT pg_temp.check(
    (SELECT array_agg(table_name::text ORDER BY table_name)
       FROM information_schema.tables
      WHERE table_schema = 'career_system' AND table_type = 'BASE TABLE')
  = ARRAY['career_family','career_result','dataset_version','job_posting','job_posting_skill',
          'major','occupation','occupation_alias','occupation_skill','portfolio',
          'portfolio_project','resume','skill','skill_alias','skill_evidence',
          'skill_gap','user_feedback','user_session','user_skill'],
    'T2 exactly the 19 core tables of IMPLEMENTATION_PLAN §5.2');

-- =============================================================
-- Test 3 — Foreign keys (MIG §49)
-- =============================================================

SELECT pg_temp.check(
    (SELECT count(*) FROM information_schema.table_constraints
      WHERE constraint_schema = 'career_system' AND constraint_type = 'FOREIGN KEY') = 23,
    'T3 23 foreign keys exist');

SELECT pg_temp.expect_error(
    $$INSERT INTO occupation_skill (occupation_id, skill_id) VALUES (-1, (SELECT min(skill_id) FROM skill))$$,
    '23503', 'T3 occupation_skill cannot reference a missing occupation');

SELECT pg_temp.expect_error(
    $$INSERT INTO resume (session_id, file_name, file_type, storage_reference)
      VALUES ('00000000-0000-0000-0000-00000000dead', 'x.pdf', 'pdf', 'tmp/x')$$,
    '23503', 'T3 resume cannot reference a missing session');

SELECT pg_temp.expect_error(
    $$INSERT INTO skill_gap (result_id, skill_id, status) VALUES (-1, (SELECT min(skill_id) FROM skill), 'MATCHED')$$,
    '23503', 'T3 skill_gap cannot reference a missing career_result');

SELECT pg_temp.expect_error(
    $$INSERT INTO job_posting (job_title, source, date_collected, dataset_version_id)
      VALUES ('x', 'test', NOW(), -1)$$,
    '23503', 'T3 job_posting cannot reference a missing dataset_version');

-- =============================================================
-- Test 4 — Constraints: PK, UNIQUE, NOT NULL, CHECK (MIG §49, §73)
-- =============================================================

-- one valid session used by the following checks
INSERT INTO user_session (session_id, major_id, expires_at)
VALUES ('00000000-0000-0000-0000-000000000001',
        (SELECT major_id FROM major WHERE major_name = 'Web Full Stack'),
        NOW() + INTERVAL '1 hour');

SELECT pg_temp.expect_error(
    $$INSERT INTO user_session (session_id, expires_at)
      VALUES ('00000000-0000-0000-0000-000000000001', NOW())$$,
    '23505', 'T4 PRIMARY KEY: duplicate session_id rejected');

SELECT pg_temp.expect_error(
    $$INSERT INTO major (branch_name, major_name) VALUES ('ครีเอทีฟมีเดียเทคโนโลยี', 'Web Full Stack')$$,
    '23505', 'T4 UNIQUE: duplicate (branch_name, major_name) rejected');

SELECT pg_temp.expect_error(
    $$INSERT INTO skill (skill_name, category) VALUES ('React', 'TECHNICAL')$$,
    '23505', 'T4 UNIQUE: duplicate skill_name rejected');

SELECT pg_temp.expect_error(
    $$INSERT INTO skill_alias (skill_id, alias) VALUES ((SELECT min(skill_id) FROM skill), 'ReactJS')$$,
    '23505', 'T4 UNIQUE: duplicate skill alias rejected');

INSERT INTO user_skill (session_id, skill_id, source)
VALUES ('00000000-0000-0000-0000-000000000001', (SELECT skill_id FROM skill WHERE skill_name = 'React'), 'RESUME');

SELECT pg_temp.expect_error(
    $$INSERT INTO user_skill (session_id, skill_id, source)
      VALUES ('00000000-0000-0000-0000-000000000001', (SELECT skill_id FROM skill WHERE skill_name = 'React'), 'PORTFOLIO')$$,
    '23505', 'T4 UNIQUE: same skill twice in one session rejected');

SELECT pg_temp.expect_error(
    $$INSERT INTO skill (skill_name) VALUES ('No Category')$$,
    '23502', 'T4 NOT NULL: skill.category required');

SELECT pg_temp.expect_error(
    $$INSERT INTO user_session (session_id) VALUES ('00000000-0000-0000-0000-000000000002')$$,
    '23502', 'T4 NOT NULL: user_session.expires_at required');

SELECT pg_temp.expect_error(
    $$INSERT INTO user_session (session_id, expires_at, status)
      VALUES ('00000000-0000-0000-0000-000000000003', NOW(), 'UNKNOWN')$$,
    '23514', 'T4 CHECK: invalid session status rejected');

SELECT pg_temp.expect_error(
    $$INSERT INTO skill (skill_name, category) VALUES ('Bad Category', 'MAGIC')$$,
    '23514', 'T4 CHECK: invalid skill category rejected');

SELECT pg_temp.expect_error(
    $$UPDATE user_skill SET confidence = 1.5 WHERE session_id = '00000000-0000-0000-0000-000000000001'$$,
    '23514', 'T4 CHECK: confidence outside 0-1 rejected');

SELECT pg_temp.expect_error(
    $$INSERT INTO career_result (session_id, occupation_id, rank_position)
      VALUES ('00000000-0000-0000-0000-000000000001', (SELECT min(occupation_id) FROM occupation), 0)$$,
    '23514', 'T4 CHECK: rank_position must be > 0');

SELECT pg_temp.expect_error(
    $$INSERT INTO career_result (session_id, occupation_id, rank_position, score)
      VALUES ('00000000-0000-0000-0000-000000000001', (SELECT min(occupation_id) FROM occupation), 1, -1)$$,
    '23514', 'T4 CHECK: negative match score rejected');

SELECT pg_temp.expect_error(
    $$INSERT INTO user_feedback (session_id, sus_score)
      VALUES ('00000000-0000-0000-0000-000000000001', 101)$$,
    '23514', 'T4 CHECK: SUS score above 100 rejected');

-- =============================================================
-- Test 5 — Indexes (MIG §49, §38; DATABASE.md §39)
-- =============================================================

SELECT pg_temp.check(
    (SELECT array_agg(indexname::text ORDER BY indexname) FROM pg_indexes
      WHERE schemaname = 'career_system' AND indexname LIKE 'idx\_%')
  = ARRAY['idx_career_result_occupation','idx_career_result_rank','idx_career_result_session',
          'idx_feedback_session','idx_job_posting_dataset_version','idx_job_posting_date',
          'idx_job_posting_occupation','idx_job_posting_skill_job','idx_job_posting_skill_skill',
          'idx_occupation_alias_occupation','idx_occupation_family','idx_occupation_skill_occupation',
          'idx_occupation_skill_skill','idx_portfolio_project_portfolio','idx_portfolio_session',
          'idx_resume_session','idx_skill_evidence_project','idx_skill_evidence_user_skill',
          'idx_skill_gap_result','idx_user_session_expires','idx_user_session_major',
          'idx_user_session_status','idx_user_skill_session','idx_user_skill_skill'],
    'T5 all 24 indexes exist with the documented names');

-- The planner can use an index for a typical lookup (seq scan disabled to force the choice)
SET LOCAL enable_seqscan = off;
CREATE FUNCTION pg_temp.plan_uses(query text, index_name text) RETURNS boolean
LANGUAGE plpgsql AS $$
DECLARE
    line text;
BEGIN
    FOR line IN EXECUTE 'EXPLAIN ' || query LOOP
        IF position(index_name IN line) > 0 THEN
            RETURN TRUE;
        END IF;
    END LOOP;
    RETURN FALSE;
END $$;

SELECT pg_temp.check(
    pg_temp.plan_uses($$SELECT * FROM resume WHERE session_id = '00000000-0000-0000-0000-000000000001'$$,
                      'idx_resume_session'),
    'T5 resume lookup by session can use idx_resume_session');

SELECT pg_temp.check(
    pg_temp.plan_uses($$SELECT * FROM job_posting WHERE date_collected >= NOW() - INTERVAL '30 days'$$,
                      'idx_job_posting_date'),
    'T5 job_posting lookup by date can use idx_job_posting_date');
RESET enable_seqscan;

-- =============================================================
-- Relationships + cascade (DATABASE.md §38, §59, §62)
-- =============================================================

-- Build one complete chain of user data for session ...0001
INSERT INTO resume (session_id, file_name, file_type, storage_reference)
VALUES ('00000000-0000-0000-0000-000000000001', 'synthetic.pdf', 'pdf', 'temporary/synthetic.pdf');

INSERT INTO portfolio (session_id, url)
VALUES ('00000000-0000-0000-0000-000000000001', 'https://example.com/portfolio');

INSERT INTO portfolio_project (portfolio_id, title)
SELECT portfolio_id, 'Synthetic project' FROM portfolio
WHERE session_id = '00000000-0000-0000-0000-000000000001';

INSERT INTO skill_evidence (user_skill_id, source_type, project_id, evidence_text)
SELECT us.user_skill_id, 'PORTFOLIO_PROJECT', pp.project_id, 'synthetic evidence'
FROM user_skill us
JOIN portfolio p ON p.session_id = us.session_id
JOIN portfolio_project pp ON pp.portfolio_id = p.portfolio_id
WHERE us.session_id = '00000000-0000-0000-0000-000000000001';

INSERT INTO dataset_version (dataset_name, version_name) VALUES ('test', 'v0');

INSERT INTO career_result (session_id, occupation_id, rank_position, score, algorithm_version, dataset_version_id)
SELECT '00000000-0000-0000-0000-000000000001', occupation_id, 1, 80, 'test', (SELECT dataset_version_id FROM dataset_version WHERE dataset_name = 'test')
FROM occupation WHERE occupation_name = 'Front-end Developer';

INSERT INTO skill_gap (result_id, skill_id, status, priority)
SELECT cr.result_id, s.skill_id, 'EVIDENCE_NOT_FOUND', 'HIGH'
FROM career_result cr, skill s
WHERE cr.session_id = '00000000-0000-0000-0000-000000000001' AND s.skill_name = 'TypeScript';

INSERT INTO user_feedback (session_id, sus_score, satisfaction)
VALUES ('00000000-0000-0000-0000-000000000001', 75, 80);

SELECT pg_temp.check(
    (SELECT count(*) FROM resume WHERE session_id = '00000000-0000-0000-0000-000000000001') = 1
    AND (SELECT count(*) FROM skill_evidence) = 1
    AND (SELECT count(*) FROM skill_gap) = 1
    AND (SELECT count(*) FROM user_feedback) = 1,
    'REL session -> resume / portfolio -> project / skill -> evidence / result -> gap / feedback linked');

-- Evidence Not Found principle (CLAUDE.md §6): there is no "missing skill" status
SELECT pg_temp.expect_error(
    $$UPDATE skill_gap SET status = 'MISSING'$$,
    '23514', 'RULE skill_gap status cannot claim a skill is MISSING (only EVIDENCE_NOT_FOUND)');

-- RESTRICT: knowledge in use cannot be deleted (DATABASE.md §38)
SELECT pg_temp.expect_error(
    $$DELETE FROM skill WHERE skill_name = 'React'$$,
    '23503', 'DELETE RESTRICT: skill used by user_skill cannot be deleted');

SELECT pg_temp.expect_error(
    $$DELETE FROM occupation WHERE occupation_name = 'Front-end Developer'$$,
    '23503', 'DELETE RESTRICT: occupation used by career_result cannot be deleted');

-- SET NULL: deleting a project keeps the evidence, detaches it
DELETE FROM portfolio_project;
SELECT pg_temp.check(
    (SELECT count(*) FROM skill_evidence WHERE project_id IS NULL) = 1,
    'DELETE SET NULL: evidence survives project deletion with project_id = NULL');

-- CASCADE: deleting the session removes all temporary user data
DELETE FROM user_session WHERE session_id = '00000000-0000-0000-0000-000000000001';

SELECT pg_temp.check(
    (SELECT count(*) FROM resume) = 0
    AND (SELECT count(*) FROM portfolio) = 0
    AND (SELECT count(*) FROM user_skill) = 0
    AND (SELECT count(*) FROM skill_evidence) = 0
    AND (SELECT count(*) FROM career_result) = 0
    AND (SELECT count(*) FROM skill_gap) = 0
    AND (SELECT count(*) FROM user_feedback) = 0,
    'DELETE CASCADE: session deletion removes all temporary user data');

SELECT pg_temp.check(
    (SELECT count(*) FROM skill) = 24
    AND (SELECT count(*) FROM occupation) = 9
    AND (SELECT count(*) FROM dataset_version) = 1,
    'DELETE CASCADE: skill / occupation / dataset knowledge is kept');

-- SET NULL: deleting a major keeps sessions (major is context only)
INSERT INTO user_session (session_id, major_id, expires_at)
VALUES ('00000000-0000-0000-0000-000000000004',
        (SELECT major_id FROM major WHERE major_name = 'Game Development'), NOW());
DELETE FROM major WHERE major_name = 'Game Development';
SELECT pg_temp.check(
    (SELECT major_id FROM user_session WHERE session_id = '00000000-0000-0000-0000-000000000004') IS NULL,
    'DELETE SET NULL: session survives major deletion with major_id = NULL');

-- =============================================================
-- Development seed rules (MIG §44-48, IMPLEMENTATION_PLAN §5.4)
-- Re-checked after rollback-safe changes above, so use seeded totals.
-- =============================================================

SELECT pg_temp.check(
    (SELECT count(DISTINCT branch_name) FROM major) = 4,
    'SEED 4 faculty branches');

SELECT pg_temp.check(
    (SELECT count(*) FROM career_family) = 15,
    'SEED 15 career families');

SELECT pg_temp.check(
    (SELECT count(*) FROM skill_alias) >= 1 AND (SELECT count(*) FROM occupation_alias) >= 1,
    'SEED sample skill and occupation aliases');

SELECT pg_temp.check(
    NOT EXISTS (SELECT 1 FROM occupation WHERE source IS DISTINCT FROM 'DEMO / DEVELOPMENT DATA'),
    'SEED every occupation is labelled DEMO / DEVELOPMENT DATA');

SELECT pg_temp.check(
    (SELECT count(*) FROM occupation_skill) = 0,
    'SEED no occupation_skill importance/demand invented without methodology');

ROLLBACK;
