# database/

ฐานข้อมูลหลักของระบบ: **PostgreSQL** (`CLAUDE.md` §7)

Source of Truth ของ Schema:

- `docs/02-database/DATABASE.md`
- `docs/02-database/DATABASE_MIGRATION_PLAN.md`
- `docs/decisions/0003-database-tooling.md`

## โครงสร้าง

| โฟลเดอร์ | หน้าที่ |
| --- | --- |
| `migrations/` | SQL Migration Files ที่สร้างโครงสร้าง Database (001-021 ตาม DATABASE_MIGRATION_PLAN §5) |
| `seed/` | ข้อมูลเริ่มต้น แยกจาก Migration (ดู `seed/README.md`) |
| `schema/` | Schema Documentation (ดู `schema/README.md`) |

## Migration Tool

SQL Migration Files + Runner Script ใน `scripts/database/` (ADR 0003 ข้อ 1, 4)
DB Client ของ Backend คือ `pg` (node-postgres) ไม่ใช้ ORM (ADR 0003 ข้อ 5)

## Migration Naming Convention

`NNN_action_target.sql` เช่น `001_create_schema.sql` (DATABASE_MIGRATION_PLAN §6)

## How to Create New Migration

1. Requirement -> Update Documentation -> New Migration -> Test (`CLAUDE.md` §7)
2. ใช้เลขถัดไปจากไฟล์ล่าสุด
3. ห้ามแก้ Migration ที่ Apply แล้ว (Immutable, DATABASE_MIGRATION_PLAN §7)
   ตาราง `schema_migrations` เก็บ `version`, `applied_at`, `checksum` เพื่อตรวจการแก้ไฟล์ (ADR 0003 ข้อ 2)

## Rollback Policy

Reverse Migration: แก้ด้วย Migration ใหม่ ไม่มีไฟล์ down (DATABASE_MIGRATION_PLAN §50, ADR 0003 ข้อ 3)
Development: รีเซ็ตฐานข้อมูลแล้วรัน Migration ใหม่
ห้ามใช้ `DROP DATABASE` แก้ปัญหาใน Production

## How to Run Migration / Seed / Reset / Tests

สร้างใน Phase 1 (`scripts/database/migrate.sh`, `seed.sh`, `reset.sh` ตาม FOLDER_STRUCTURE §24)

## Environment Variables

`DATABASE_URL` (ENVIRONMENT_SETUP §15) ค่าจริงอยู่ใน `.env` ซึ่งห้าม Commit

## ห้าม

- MySQL / MariaDB syntax, MongoDB เป็น Main Database (`CLAUDE.md` §7)
- ข้อมูล User จริงใน Migration หรือ Seed (DATABASE_MIGRATION_PLAN §48)
