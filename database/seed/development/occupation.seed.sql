-- =============================================================
-- occupation.seed.sql — DEMO / DEVELOPMENT DATA
-- Occupations from DATABASE_MIGRATION_PLAN §47, to be replaced by the
-- occupation framework from ESCO / O*NET + Thai labour market (Phase 2).
-- Career-family assignment is a development choice.
--
-- occupation_skill is intentionally NOT seeded: importance and demand must
-- come from a documented methodology, never invented numbers (MIG §20,
-- CLAUDE.md §6 Labour Market).
-- =============================================================

INSERT INTO occupation (career_family_id, occupation_name, source)
SELECT cf.career_family_id, o.occupation_name, 'DEMO / DEVELOPMENT DATA'
FROM (VALUES
    ('CF10', 'Front-end Developer'),
    ('CF10', 'Back-end Developer'),
    ('CF10', 'Full-stack Developer'),
    ('CF10', 'Web Developer'),
    ('CF11', 'UI/UX Designer'),
    ('CF07', 'Graphic Designer'),
    ('CF02', 'Video Editor'),
    ('CF14', 'Game Programmer'),
    ('CF13', 'Game Designer')
) AS o(family_code, occupation_name)
JOIN career_family cf ON cf.family_code = o.family_code
ON CONFLICT (career_family_id, occupation_name) DO NOTHING;

-- Aliases: examples from DATABASE.md §21
INSERT INTO occupation_alias (occupation_id, alias)
SELECT oc.occupation_id, a.alias
FROM (VALUES
    ('Front-end Developer', 'Frontend Developer'),
    ('Front-end Developer', 'Frontend Engineer'),
    ('Front-end Developer', 'Junior Frontend Developer')
) AS a(occupation_name, alias)
JOIN occupation oc ON oc.occupation_name = a.occupation_name
ON CONFLICT (alias) DO NOTHING;
