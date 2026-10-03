-- =============================================================
-- career_family.seed.sql — DEMO / TEST DATA
-- Initial Framework, not the final occupation dataset
-- (DATABASE.md §19, DATABASE_MIGRATION_PLAN §45)
-- =============================================================

INSERT INTO career_family (family_code, family_name, description) VALUES
    ('CF01', 'Film & Video Production',        'DEMO / TEST DATA: initial framework'),
    ('CF02', 'Post-Production & Motion/VFX',   'DEMO / TEST DATA: initial framework'),
    ('CF03', 'Broadcast & Audio',              'DEMO / TEST DATA: initial framework'),
    ('CF04', 'Advertising & Creative',         'DEMO / TEST DATA: initial framework'),
    ('CF05', 'Digital Marketing & Content',    'DEMO / TEST DATA: initial framework'),
    ('CF06', 'PR & Corporate Communication',   'DEMO / TEST DATA: initial framework'),
    ('CF07', 'Graphic & Visual Communication', 'DEMO / TEST DATA: initial framework'),
    ('CF08', 'Packaging & Print Design',       'DEMO / TEST DATA: initial framework'),
    ('CF09', 'Prepress & Print Production',    'DEMO / TEST DATA: initial framework'),
    ('CF10', 'Web Development',                'DEMO / TEST DATA: initial framework'),
    ('CF11', 'UI/UX & Digital Product',        'DEMO / TEST DATA: initial framework'),
    ('CF12', 'Web Content & Growth',           'DEMO / TEST DATA: initial framework'),
    ('CF13', 'Game Design & Production',       'DEMO / TEST DATA: initial framework'),
    ('CF14', 'Game Development & Technical',   'DEMO / TEST DATA: initial framework'),
    ('CF15', 'Game Art & Animation',           'DEMO / TEST DATA: initial framework')
ON CONFLICT (family_code) DO NOTHING;
