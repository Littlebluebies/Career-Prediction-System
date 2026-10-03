-- =============================================================
-- major.seed.sql — DEMO / TEST DATA (DATABASE_MIGRATION_PLAN §44)
-- Names are NOT verified against the faculty's official curriculum.
-- Verify before production (MIG §12, §44).
--
-- Convention (Phase 1 decision, C-06):
--   * a branch without tracks uses its own name as major_name
--   * Creative Media Technology has one row per track
-- Major is context only, never a hard filter of careers (CLAUDE.md §6).
-- =============================================================

INSERT INTO major (branch_name, major_name) VALUES
    ('เทคโนโลยีการผลิตภาพยนตร์และวิทยุโทรทัศน์', 'เทคโนโลยีการผลิตภาพยนตร์และวิทยุโทรทัศน์'),
    ('เทคโนโลยีการโฆษณาและประชาสัมพันธ์', 'เทคโนโลยีการโฆษณาและประชาสัมพันธ์'),
    ('เทคโนโลยีการพิมพ์ดิจิทัลและบรรจุภัณฑ์', 'เทคโนโลยีการพิมพ์ดิจิทัลและบรรจุภัณฑ์'),
    ('ครีเอทีฟมีเดียเทคโนโลยี', 'Web Full Stack'),
    ('ครีเอทีฟมีเดียเทคโนโลยี', 'Game Development')
ON CONFLICT (branch_name, major_name) DO NOTHING;
