# database/schema/

Schema Documentation ของ Database (DATABASE_MIGRATION_PLAN §5)

- Source of Truth ของ Schema คือ `docs/02-database/DATABASE.md`
- โครงสร้างจริงใน Database ถูกสร้างจาก `database/migrations/` เท่านั้น
- ไฟล์ในโฟลเดอร์นี้ใช้อธิบายหรือตรวจสอบ Schema ไม่ใช่ Migration และไม่ถูกรันเพื่อสร้างหรือแก้ตาราง

หลักการแยก Migration, Seed และ Schema Documentation ต้องคงไว้ (DATABASE_MIGRATION_PLAN §5)

## ไฟล์ทดสอบ (รันด้วย `bash scripts/database/test.sh`)

| ไฟล์ | ทดสอบ |
| --- | --- |
| `tests.sql` | Migration, Constraint, Foreign Key, Cascade และกติกาของ Development Seed (รอบที่ 1) |
| `tests_reference.sql` | Reference Seed: จำนวนตรงกับ `dataset_version`, ESCO URI, importance / demand เป็น NULL, Alias, ไม่ปน DEMO, ชื่อสาขาทางการ (รอบที่ 2, ADR 0010) |
