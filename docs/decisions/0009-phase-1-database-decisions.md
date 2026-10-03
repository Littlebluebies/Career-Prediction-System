# 0009: การตัดสินใจของ Phase 1 (Database)

- สถานะ: Accepted
- วันที่: 2026-10-02
- ผู้ตัดสิน: เจ้าของโครงการ (เลือกตามข้อเสนอก่อนเริ่ม Phase 1)

## บริบท

ก่อนเริ่ม Phase 1 มี 4 เรื่องที่เอกสารไม่ได้กำหนด หรือกำหนดไว้ไม่ตรงกัน:

1. เครื่องมือทดสอบ (ค้างจาก Phase 0) โดย `ENVIRONMENT_SETUP.md` §46 กำหนดให้มี Unit Tests แต่ ADR 0008 ไม่มีเครื่องมือทดสอบ
2. C-06: `major_name` ของสาขาที่ไม่มี Sub-major (`DATABASE.md` §10 กำหนด `branch_name`, `major_name` เป็น `NOT NULL` และ UNIQUE เป็นคู่)
3. ชื่อสาขาใน Seed: `DATABASE.md` §10 ใช้ "สาขาวิชา..." ส่วน `DATABASE_MIGRATION_PLAN.md` §12, §44 ไม่มีคำนำหน้า
4. Database สำหรับทดสอบ: `DATABASE_MIGRATION_PLAN.md` §53 ยกตัวอย่าง `career_system_dev/test/prod` แต่ `ENVIRONMENT_SETUP.md` §13 และ `.env.example` ใช้ `career_system`

## การตัดสินใจ

1. **Database tests เขียนเป็น SQL** (`database/schema/tests.sql`) รันผ่าน `psql` ใน Container ด้วย `scripts/database/test.sh` ไม่เพิ่ม Dependency และตรงกับเหตุผล SQL Transparency ของ ADR 0003 ส่วน Unit Test ของ `apps/api` ใช้ `node:test` ที่มากับ Node 24 (ตั้งค่าเมื่อมีโค้ด Backend ให้ทดสอบ) และเครื่องมือของ Python ตัดสินใน Phase 4
2. **Convention ของ `major`:** สาขาที่ไม่มี Track ใช้ชื่อสาขาเป็น `major_name` ด้วย ส่วนครีเอทีฟมีเดียเทคโนโลยีมี 1 แถวต่อ 1 Track (Web Full Stack, Game Development) รวม 5 แถว ส่วนที่เหลือของ C-06 (`GET /majors`) ตัดสินใน Phase 9
3. **ชื่อสาขาใน Seed ไม่มีคำนำหน้า "สาขาวิชา"** ตาม `DATABASE_MIGRATION_PLAN.md` §44 และยังต้องตรวจกับชื่อทางการของคณะก่อน Production
4. **Development ใช้ `career_system` ตามเดิม** ส่วน `test.sh` สร้าง `career_system_test` ใหม่ทุกครั้งแล้วลบทิ้งเมื่อเสร็จ Production ตัดสินใน Phase 13

## รายละเอียด Implementation ที่เลือกระหว่าง Phase 1

- ตาราง `schema_migrations` อยู่ใน schema `public` เพราะต้องมีก่อน Migration 001
- Migration 001 ตั้ง `search_path` และ `timezone = UTC` ที่ระดับ Database (`ALTER DATABASE`) เพื่อให้ทุก Connection ใช้ค่าเดียวกัน (`DATABASE.md` §4, §9)
- Migration 016 ประกาศ `fk_job_posting_dataset_version` ไว้ใน `CREATE TABLE` แทน `ALTER TABLE` ใน `DATABASE.md` §25 เพราะ `dataset_version` ถูกสร้างก่อนแล้วที่ 010 Schema ที่ได้เหมือนกัน
- Migration 021 รวม Index จาก `DATABASE.md` §11, §18, §39 และ `DATABASE_MIGRATION_PLAN.md` §38 ได้ 24 ตัว
- Development Seed: หมวดของ Skill และ Career Family ของ Occupation ตัวอย่างเป็นการเลือกเพื่อการพัฒนา ติดป้าย DEMO และไม่ Seed `occupation_skill` (MIG §20)

## ผลที่ตามมา

- C-06 ใน `docs/decisions/README.md` ปิดส่วน Convention แล้ว เหลือ `GET /majors`
- ไม่มีการแก้เอกสาร Source of Truth
