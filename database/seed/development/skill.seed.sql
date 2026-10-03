-- =============================================================
-- skill.seed.sql — DEMO / TEST DATA
-- Skill names: union of DATABASE_MIGRATION_PLAN §15 and §46.
-- Category assignment is a development choice, not a validated taxonomy.
-- The real taxonomy comes from the dataset methodology (Phase 2, DATASET_SPEC.md).
-- =============================================================

INSERT INTO skill (skill_name, category, description) VALUES
    ('HTML',               'TECHNICAL',     'DEMO / TEST DATA'),
    ('CSS',                'TECHNICAL',     'DEMO / TEST DATA'),
    ('JavaScript',         'TECHNICAL',     'DEMO / TEST DATA'),
    ('TypeScript',         'TECHNICAL',     'DEMO / TEST DATA'),
    ('React',              'TECHNICAL',     'DEMO / TEST DATA'),
    ('Next.js',            'TECHNICAL',     'DEMO / TEST DATA'),
    ('Node.js',            'TECHNICAL',     'DEMO / TEST DATA'),
    ('Express.js',         'TECHNICAL',     'DEMO / TEST DATA'),
    ('Python',             'TECHNICAL',     'DEMO / TEST DATA'),
    ('SQL',                'TECHNICAL',     'DEMO / TEST DATA'),
    ('PostgreSQL',         'TECHNICAL',     'DEMO / TEST DATA'),
    ('Git',                'SOFTWARE_TOOL', 'DEMO / TEST DATA'),
    ('Figma',              'SOFTWARE_TOOL', 'DEMO / TEST DATA'),
    ('Adobe Photoshop',    'SOFTWARE_TOOL', 'DEMO / TEST DATA'),
    ('Adobe Illustrator',  'SOFTWARE_TOOL', 'DEMO / TEST DATA'),
    ('Adobe Premiere Pro', 'SOFTWARE_TOOL', 'DEMO / TEST DATA'),
    ('After Effects',      'SOFTWARE_TOOL', 'DEMO / TEST DATA'),
    ('Unity',              'SOFTWARE_TOOL', 'DEMO / TEST DATA'),
    ('Unreal Engine',      'SOFTWARE_TOOL', 'DEMO / TEST DATA'),
    ('UI Design',          'DESIGN',        'DEMO / TEST DATA'),
    ('UX Design',          'DESIGN',        'DEMO / TEST DATA'),
    ('Communication',      'COMMUNICATION', 'DEMO / TEST DATA'),
    ('Presentation',       'COMMUNICATION', 'DEMO / TEST DATA'),
    ('Project Management', 'BUSINESS',      'DEMO / TEST DATA')
ON CONFLICT (skill_name) DO NOTHING;

-- Aliases: examples from DATABASE_MIGRATION_PLAN §16 (raw name -> canonical skill)
INSERT INTO skill_alias (skill_id, alias)
SELECT s.skill_id, a.alias
FROM (VALUES
    ('React',           'React.js'),
    ('React',           'ReactJS'),
    ('Adobe Photoshop', 'Photoshop'),
    ('Adobe Photoshop', 'PS')
) AS a(skill_name, alias)
JOIN skill s ON s.skill_name = a.skill_name
ON CONFLICT (alias) DO NOTHING;
