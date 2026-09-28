# 0003: เครื่องมือฐานข้อมูล

- สถานะ: Accepted (ตัวเลือกที่ Claude เลือกตามคำสั่งให้แก้ความเสี่ยงโดยตรง เจ้าของโครงการเปลี่ยนได้ก่อนเริ่ม Phase 1)
- วันที่: 2026-09-20
- การยืนยัน: เจ้าของโครงการสั่งให้ดำเนินการต่อหลังตรวจว่าไม่ขัดกับชิ้นงาน (2026-09-20)

## บริบท

- `DATABASE_MIGRATION_PLAN.md` §64 กำหนดให้เลือกวิธีจัดการ Migration ระหว่าง SQL Files กับ Tool ของ Node.js และ §50 ให้เลือกวิธี Rollback
- `TECH_STACK.md` §18 ให้เลือก PostgreSQL Client, Query Builder หรือ ORM และบันทึกการตัดสินใจ
- รายการ Migration มี 3 ชุดที่ไม่ตรงกัน: `FOLDER_STRUCTURE.md` §16 (2 ไฟล์), `DATABASE.md` §45 (11 ไฟล์) และ `DATABASE_MIGRATION_PLAN.md` §5 (21 ไฟล์)
- เอกสารไม่ระบุ PostgreSQL major version

## การตัดสินใจ

1. **Migration:** SQL Files ชื่อ `NNN_action_target.sql` รายการฉบับเต็มคือ `DATABASE_MIGRATION_PLAN.md` §5 (001-021) `DATABASE.md` §45 และ `FOLDER_STRUCTURE.md` §16 อ้างถึงรายการนี้แล้ว
2. **การติดตาม:** ตาราง `schema_migrations` ตาม `DATABASE_MIGRATION_PLAN.md` §8 (`version`, `applied_at`) เพิ่มคอลัมน์ `checksum` (SHA-256 ของไฟล์) เพื่อตรวจว่าไม่มีการแก้ Migration ที่ Apply แล้ว (§7) `.gitattributes` บังคับ `*.sql` เป็น LF เพื่อให้ Checksum เท่ากันทุก OS
3. **Rollback:** Approach B (§50) แบบ Reverse Migration ไม่มีไฟล์ down แก้ด้วย Migration ใหม่ ส่วน Development รีเซ็ตฐานข้อมูลแล้วรันใหม่ ห้ามใช้ `DROP DATABASE` แก้ปัญหาใน Production
4. **Runner:** Script ใน `scripts/database/` รัน Migration แต่ละไฟล์ใน Transaction เดียว สร้างใน Phase 1
5. **DB client:** node-postgres (`pg`) เขียน SQL แบบ Parameterized ใน Repository Layer ไม่ใช้ ORM
6. **Seed:** `seed/development/` เป็น DEMO / TEST DATA ส่วน `seed/reference/` เป็นข้อมูลอ้างอิงที่ตรวจสอบแล้ว
7. **PostgreSQL:** `postgres:17` ใน `docker-compose.yml` เวอร์ชัน 17 ได้รับการสนับสนุนถึง พ.ย. 2029 ส่วนเวอร์ชัน 18 ออกแล้ว ถ้าต้องการใช้ ให้ตรวจ Path ของ Volume ในเอกสารของ Image ก่อน

## เหตุผล

- Schema ถูกออกแบบเป็น SQL ใน `DATABASE.md` อยู่แล้ว การใช้ ORM จะสร้าง Schema อีกชุด ซึ่ง `DATABASE_MIGRATION_PLAN.md` §65 เตือนไว้
- `CLAUDE.md` §12 กำหนด Repository Layer อยู่แล้ว จึงไม่ต้องมี Layer เพิ่ม
- SQL Files ตรวจสอบและ Review ได้ตรงๆ ตรงกับเกณฑ์ SQL Transparency ใน §64

## ผลที่ตามมา

- เอกสารที่แก้: `DATABASE.md` §45, `DATABASE_MIGRATION_PLAN.md` §5, §6, §50, §64, §65, `TECH_STACK.md` §17, §18, `FOLDER_STRUCTURE.md` §16-§18
- ตัวอย่าง Migration ในอนาคตใน `DATABASE_MIGRATION_PLAN.md` §6 เปลี่ยนเป็นรูปแบบชื่อ เพราะ `024_add_algorithm_version.sql` ซ้ำกับคอลัมน์ที่ `career_result` มีอยู่แล้ว (`DATABASE.md` §26, `018_create_career_result.sql`)
- ยังไม่เพิ่ม Dependency ใดใน `apps/api` จนกว่าจะถึง Phase 0
