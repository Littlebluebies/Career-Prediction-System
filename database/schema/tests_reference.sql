-- =============================================================
-- tests_reference.sql — reference seed tests (run by scripts/database/test.sh)
-- Sources: DATASET_SPEC.md §32-35, §56-57; ADR 0006; ADR 0010
--
-- Runs on a fresh career_system_test database loaded with
--   migrate.sh + seed.sh reference (twice, to prove it is idempotent)
-- Same style as tests.sql: one transaction, rolled back at the end,
-- every check prints "INFO: PASS ..." or raises "FAIL ..." and stops.
-- Expected counts come from dataset_version.record_count, which import.py
-- copies from datasets/metadata/*.json (validate.py checks them against the CSVs).
-- =============================================================

BEGIN;
SET search_path TO career_system, public;

CREATE FUNCTION pg_temp.check(ok boolean, label text) RETURNS void
LANGUAGE plpgsql AS $$
BEGIN
    IF ok IS TRUE THEN
        RAISE INFO 'PASS  %', label;
    ELSE
        RAISE EXCEPTION 'FAIL  %', label;
    END IF;
END $$;

-- record_count of the only version of a dataset (NULL if missing or ambiguous)
CREATE FUNCTION pg_temp.expected(name text) RETURNS integer
LANGUAGE sql AS $$
    SELECT CASE WHEN count(*) = 1 THEN max(record_count) END
    FROM dataset_version WHERE dataset_name = name
$$;

-- =============================================================
-- Dataset version / traceability (ADR 0006, DATASET_SPEC §32-33)
-- =============================================================

SELECT pg_temp.check(
    (SELECT count(*) FROM dataset_version) = 3
    AND pg_temp.expected('occupation') IS NOT NULL
    AND pg_temp.expected('skill') IS NOT NULL
    AND pg_temp.expected('occupation_skill') IS NOT NULL,
    'REF dataset_version has one row each for occupation, skill, occupation_skill');

SELECT pg_temp.check(
    NOT EXISTS (SELECT 1 FROM dataset_version
                WHERE version_name !~ '^[0-9]{4}\.[0-9]{2}$'
                   OR source_description IS NULL
                   OR collected_at IS NULL
                   OR record_count IS NULL),
    'REF dataset_version: version YYYY.NN, source and collection date recorded');

-- =============================================================
-- Counts match the dataset version (nothing lost on import)
-- =============================================================

SELECT pg_temp.check(
    (SELECT count(*) FROM occupation) = pg_temp.expected('occupation'),
    'REF occupation rows = dataset_version.record_count');

SELECT pg_temp.check(
    (SELECT count(*) FROM skill) = pg_temp.expected('skill'),
    'REF skill rows = dataset_version.record_count');

SELECT pg_temp.check(
    (SELECT count(*) FROM occupation_skill) = pg_temp.expected('occupation_skill'),
    'REF occupation_skill rows = dataset_version.record_count');

SELECT pg_temp.check(
    (SELECT count(*) FROM skill_alias) > 0 AND (SELECT count(*) FROM occupation_alias) > 0,
    'REF skill and occupation aliases loaded');

-- =============================================================
-- Occupation framework (DATASET_SPEC §35, ADR 0010 §2, §8)
-- =============================================================

SELECT pg_temp.check(
    (SELECT count(*) FROM career_family) = 15,
    'REF 15 career families (DATABASE.md §19)');

SELECT pg_temp.check(
    NOT EXISTS (SELECT 1 FROM occupation o JOIN career_family cf USING (career_family_id)
                WHERE cf.family_code NOT IN ('CF10', 'CF11')),
    'REF pilot occupations belong to CF10 or CF11 only (ADR 0010 §2)');

SELECT pg_temp.check(
    NOT EXISTS (SELECT 1 FROM occupation
                WHERE source IS NULL
                   OR source NOT LIKE 'ESCO %'
                   OR source_identifier NOT LIKE 'http://data.europa.eu/esco/occupation/%'),
    'REF every occupation has an ESCO source and URI');

SELECT pg_temp.check(
    (SELECT count(DISTINCT source_identifier) FROM occupation) = (SELECT count(*) FROM occupation),
    'REF occupation URIs are unique');

-- =============================================================
-- Occupation-skill relations (ADR 0010 §3, §11)
-- =============================================================

SELECT pg_temp.check(
    NOT EXISTS (SELECT 1 FROM occupation_skill WHERE importance IS NOT NULL OR demand IS NOT NULL),
    'REF importance and demand are NULL (not invented before Phase 3)');

SELECT pg_temp.check(
    NOT EXISTS (SELECT 1 FROM occupation_skill WHERE source !~ '^ESCO \S+: (essential|optional)$'),
    'REF occupation_skill.source records the ESCO relation type');

SELECT pg_temp.check(
    NOT EXISTS (SELECT 1 FROM occupation o
                WHERE NOT EXISTS (SELECT 1 FROM occupation_skill os
                                  WHERE os.occupation_id = o.occupation_id
                                    AND os.source LIKE '%: essential')),
    'REF every occupation has at least one essential skill');

SELECT pg_temp.check(
    NOT EXISTS (SELECT 1 FROM skill s
                WHERE NOT EXISTS (SELECT 1 FROM occupation_skill os WHERE os.skill_id = s.skill_id)),
    'REF every skill is related to at least one occupation');

-- =============================================================
-- Alias rules (DATASET_SPEC §9.1, §34-35)
-- =============================================================

SELECT pg_temp.check(
    NOT EXISTS (SELECT 1 FROM skill_alias a JOIN skill s ON lower(s.skill_name) = lower(a.alias)),
    'REF no skill alias equals a canonical skill name');

SELECT pg_temp.check(
    NOT EXISTS (SELECT 1 FROM occupation_alias a JOIN occupation o ON lower(o.occupation_name) = lower(a.alias)),
    'REF no occupation alias equals an occupation name');

-- =============================================================
-- Reference data is not mixed with DEMO data (DATASET_SPEC §56)
-- =============================================================

SELECT pg_temp.check(
    NOT EXISTS (SELECT 1 FROM occupation WHERE source = 'DEMO / DEVELOPMENT DATA')
    AND NOT EXISTS (SELECT 1 FROM skill WHERE description LIKE 'DEMO%')
    AND NOT EXISTS (SELECT 1 FROM career_family WHERE description LIKE 'DEMO%'),
    'REF no DEMO / TEST DATA in the reference database');

SELECT pg_temp.check(
    (SELECT count(*) FROM major) = 0,
    'REF no majors yet (official names pending, ADR 0010 §7)');

ROLLBACK;
