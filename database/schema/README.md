# database/schema/

Schema Documentation ของ Database (DATABASE_MIGRATION_PLAN §5)

- Source of Truth ของ Schema คือ `docs/02-database/DATABASE.md`
- โครงสร้างจริงใน Database ถูกสร้างจาก `database/migrations/` เท่านั้น
- ไฟล์ในโฟลเดอร์นี้ใช้อธิบายหรือตรวจสอบ Schema ไม่ใช่ Migration และไม่ถูกรันเพื่อสร้างหรือแก้ตาราง

หลักการแยก Migration, Seed และ Schema Documentation ต้องคงไว้ (DATABASE_MIGRATION_PLAN §5)
