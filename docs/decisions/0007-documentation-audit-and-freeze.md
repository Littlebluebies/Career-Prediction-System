# 0007: Documentation Audit และ Freeze

- สถานะ: Accepted
- วันที่: 2026-09-20 (ยืนยันโดยเจ้าของโครงการ 2026-09-21)
- ผลการตรวจ: DOCUMENTATION FREEZE: READY (ดูหัวข้อ 6)

ไฟล์นี้เป็น **บันทึกผลการตรวจ (Audit Record)** ของสถานะเอกสาร ณ วันที่ตรวจเท่านั้น ไม่ใช่ Source of Truth ฉบับใหม่ และไม่แทนที่ลำดับ Source of Truth ใน `CLAUDE.md` §3 การแก้ไขที่บันทึกไว้ (A-01 ถึง A-21) ถูกนำไปใช้กับเอกสารต้นทางแล้ว เอกสารต้นทางแต่ละฉบับ (`PROJECT_SPEC.md`, `TECH_STACK.md`, `DATABASE.md` ฯลฯ) ยังเป็น Source of Truth ตามหน้าที่เดิม

หลังจากนี้ การแก้เอกสารที่ Freeze แล้วต้องเขียนบันทึกใน `docs/decisions/` และได้รับอนุมัติจากเจ้าของโครงการก่อน เรื่องที่ยังเปิดอยู่อยู่ใน `docs/decisions/README.md` (C-01 ถึง C-15)

## รายงาน Documentation Audit

โครงการ: Career Prediction System (`Career-Prediction-System/`)  
วันที่ตรวจ: 2026-09-20  
ขอบเขต: ตรวจก่อน Phase 0 ไม่มีการเขียนโค้ดและไม่ติดตั้ง Dependency

## 0. วิธีตรวจ

- อ่านเนื้อหาทั้ง 14 ไฟล์ตามที่แนบมา ทีละส่วนจนจบ (`PROJECT_SPEC`, `TECH_STACK`, `IMPLEMENTATION_PLAN`, `FOLDER_STRUCTURE`, `API`, `ENVIRONMENT_SETUP`, `DATABASE`, `DATABASE_MIGRATION_PLAN`, `DATASET_SPEC`, `AI_MATCHING_SPEC`, `UI_UX_SPEC`, `CLAUDE.md`, `README.md`, `CLAUDE_INITIAL_IMPLEMENTATION_PROMPT.md`) รวมถึงเอกสารที่เพิ่มในรอบก่อน (ADR 0001-0006, `docs/decisions/README.md`, README ของ `database/`, `database/seed/`, `database/schema/`, `datasets/`, `tests/fixtures/`)
- ไม่ใช้ grep หรือ keyword scan แทนการอ่านในรอบแรก การตรวจความสอดคล้องเทียบเชิงความหมายระหว่างเอกสาร
- `CLAUDE_INITIAL_IMPLEMENTATION_PROMPT.md` ไม่อยู่ใน repo (ไม่มีในแผนผังที่กำหนด) อ่านจากไฟล์ที่แนบ ส่วน `README.md` ต้นฉบับว่างเปล่า ฉบับใน repo คือฉบับที่เขียนขึ้นภายหลัง
- ไม่มีการแก้เอกสารระหว่างรอบแรก

### Source of Truth ที่ใช้ (ตามหน้าที่)

| หน้าที่ | Source of Truth |
| --- | --- |
| กติกา กระบวนการ หลักการที่ล็อก | `CLAUDE.md` |
| เทคโนโลยี สถาปัตยกรรม | `TECH_STACK.md` |
| Schema ฐานข้อมูล | `DATABASE.md` (ลำดับ Migration: `DATABASE_MIGRATION_PLAN.md`) |
| หัวข้ออื่น | ตามตารางใน `ENVIRONMENT_SETUP.md` §62: API, AI/NLP, Dataset, UI/UX, Development Process, Folder Structure |
| Workflow หลัก | `PROJECT_SPEC.md` §8 (Core Workflow: LOCKED) |

## 1. สรุปผลรอบแรก

| ประเภท | จำนวน | ความหมาย |
| --- | ---: | --- |
| A True Conflict | 21 | เอกสารขัดกันเองและต้องแก้เพื่อความสอดคล้อง |
| B Implementation Decision | 12 | ต่างกันแต่เลือกตอน Implement ได้ ไม่ต้องแก้เอกสาร |
| C Missing Decision | 15 | เอกสารไม่กำหนด ต้องให้เจ้าของโครงการตัดสิน |
| D No Conflict | 17 | ดูเหมือนขัดแต่ตรวจแล้วไม่ขัด |

รอบก่อนพลาด 4 เรื่องที่พบรอบนี้: `PHASE 1` (ตัวพิมพ์ใหญ่) ใน PROJECT_SPEC §73, `src/lib/api/` ใน API §63, ชื่อ Migration ตัวอย่างใน FOLDER §39 และ ENV §29, และโครง `python-service/` ใน TECH_STACK §14 (ตรวจรอบก่อนด้วยการค้นหา pattern จึงหลุด)


## 2. ผลตามหัวข้อที่ตรวจ

| หัวข้อ | ผล | รายการ |
| --- | --- | --- |
| Project scope | ไม่พบความขัดแย้ง | D-02, D-15 |
| Locked principles | ไม่พบความขัดแย้ง ไม่มีรอบใดแก้หลักการ | D-15 |
| Technology stack | สถานะ TO BE FINALIZED ตกค้าง 2 จุด และค่า Port/ชื่อ env ใน TECH_STACK | A-01, A-02, A-16 |
| Architecture | ไม่ขัด แต่ขาด Contract ของ Matching | D-01, D-04, C-01 |
| Folder structure | path/ตัวอย่างเก่าตกค้าง | A-07, A-09, A-10, A-11, A-18 |
| Phase numbering | เหลือ PHASE 1 ใน PROJECT_SPEC §73 และ Prompt | A-03, A-21, D-03 |
| Semester 1 / 2 scope | ตรงกัน | D-02, D-17 |
| Database schema | ชื่อ/enum ไม่ตรงระหว่าง DB กับ API/MIG | A-05, A-12, A-13, A-14, C-02, C-05, C-06, C-09 |
| Migration plan | ชื่อไฟล์ตัวอย่างและ Field list | A-08, A-13, B-04, B-11, B-12 |
| API contract | enum, evidence, path, satisfaction | A-05, A-06, A-07, A-17, B-01..B-03 |
| Python AI service structure | โครงเก่าใน TECH §14 และถ้อยคำ ADR 0004 | A-11, A-19, C-01 |
| Dataset structure | ชื่อโฟลเดอร์และ path Script | A-09, A-10, C-11, C-08 |
| Resume / Portfolio processing | status และ evidence ของ Python | A-05, A-06, C-03, C-13 |
| Privacy | ลำดับ Consent ใน 3 จุด และค่า Retention ยังไม่กำหนด | A-04, C-03, C-04, C-05 |
| Evaluation | Metric ตรงกัน แต่ที่เก็บ SUS/Ground Truth ยังไม่กำหนด | C-05, C-11, C-15 |
| UI/UX | สถานะ Framework และสเกล Satisfaction | A-02, A-17, C-06, C-07, C-10 |
| Git / Docker / Environment | ชื่อ env, port, ชื่อไฟล์ Migration ตัวอย่าง | A-08, A-15, A-16, B-05..B-10 |

## 3. รายการ

### A. True Conflict (แก้ในขั้นตอนที่ 8)

| ID | File | Section | Issue | Type | Source of Truth | Proposed Resolution | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A-01 | PROJECT_SPEC | §74 | สถานะ `Technology Stack: TO BE FINALIZED` ขัดกับ LOCKED ใน CLAUDE §4, TECH_STACK §85, DATABASE §66, API §79, FOLDER §56, ENV §69, MIG §78 | A | TECH_STACK §85, CLAUDE §4 | แก้บรรทัดสถานะเป็น LOCKED (อ้าง TECH_STACK §85) | ข้อความสถานะล้าหลัง ไม่ได้เปลี่ยน Stack |
| A-02 | UI_UX_SPEC | §98 | `Exact Frontend Framework: TO BE FINALIZED` ขัดกับ Next.js + React + TypeScript + Tailwind ที่ LOCKED | A | TECH_STACK §85 | แก้เป็น Next.js (LOCKED) คง Component Library / Visual Theme เป็น TBD | เหตุผลเดียวกับ A-01 |
| A-03 | PROJECT_SPEC | §73 | `PHASE 1` รวม Project Foundation + Database ขัดกับเลข Phase 0 (Setup) และ 1 (Database) | A | CLAUDE §8, IMPLEMENTATION_PLAN §3 | เปลี่ยนเป็น Phase 0-1 | Phase numbering ต้องมีระบบเดียว (ADR 0002) ตกหล่นจากรอบก่อน |
| A-04 | TECH_STACK / IMPLEMENTATION_PLAN | TECH §24, §46; IMPL §64 | Consent มาก่อน Upload (TECH §24 ข้อ 3, §46) และ E2E ใน IMPL §64 เรียง Consent > Upload และ Create Session > Select Major ขัดกับ Workflow ที่ล็อก (Major > Resume > Portfolio > Consent > Analyze) | A | PROJECT_SPEC §8 (Core Workflow LOCKED), UI_UX §1, API §5/§61 | เรียง TECH §24, §46 และ IMPL §64 ตาม Workflow ที่ล็อก | PROJECT_SPEC, UI, API, FOLDER §6/§30, TECH §43.3, DATASET §51 ใช้ลำดับนี้ ไม่แก้ Workflow |
| A-05 | API / DATABASE_MIGRATION_PLAN | API §12; MIG §23 | Resume status เป็น ERROR (และ DELETED ใน API) แต่ DATABASE §12 CHECK เป็น PENDING/PROCESSING/COMPLETED/FAILED | A | DATABASE §12 | ใช้ FAILED และตัด DELETED ออกจาก resume status | CHECK constraint ของ DB เป็นตัวกำหนด |
| A-06 | API / TECH_STACK | API §36-37; TECH §13 | Python ส่ง evidence เป็น `source` (RESUME/PORTFOLIO) แต่ DB `skill_evidence.source_type` ต้องเป็น 8 ค่า (AI §13) และมี `project_id` Express แปลงเองไม่ได้ | A | DATABASE §18, AI_MATCHING §13 | ตัวอย่าง Response ใช้ `source_type` 8 ค่า + `evidence_text` และ Request เพิ่ม `project_id` ใน `portfolio_projects` | ทำให้ Contract ระหว่าง Python, API, DB ตรงกัน |
| A-07 | API | §63 | โครงสร้าง Frontend ใช้ `src/lib/api/` (path เก่า) | A | FOLDER §4, §9 | เปลี่ยนเป็น `apps/web/lib/api/` | ตกหล่นจากรอบก่อน (ค้นหา `src/app` อย่างเดียว) |
| A-08 | FOLDER_STRUCTURE / ENVIRONMENT_SETUP | FOLDER §39; ENV §29 | ตัวอย่างชื่อ Migration `001_initial_schema.sql`, `002_add_skill_evidence.sql`, `002_indexes.sql` ขัดกับ 001_create_schema, 002_create_major | A | DATABASE_MIGRATION_PLAN §5 | เปลี่ยนตัวอย่างเป็นชื่อใน MIG §5 | ชื่อเก่าชน 002 ของแผนจริง |
| A-09 | DATABASE / DATASET_SPEC | DATABASE §47; DATASET §55 | ที่วาง Script `scripts/import/...` และ `scripts/*` แบบแบน ขัดกับ `scripts/{database,dataset,development}` | A | FOLDER_STRUCTURE §24 | เปลี่ยนเป็น `scripts/dataset/` | FOLDER เป็น SoT ของ Folder Structure (ENV §62) |
| A-10 | FOLDER_STRUCTURE | §19, §20 | ชื่อโฟลเดอร์ย่อยของ Dataset (`skills/`, `labour-market/`) ต่างจาก `skill/`, `job_posting/`, `occupation_skill/` ใน DATASET §54 | A | DATASET_SPEC §54 | ใช้ชื่อตาม DATASET §54 | DATASET เป็น SoT ของ Dataset (ENV §62) |
| A-11 | TECH_STACK | §14 | ตัวอย่างโครง Python ใช้ `python-service/` และโมดูลเดิม (parsers, extraction, ranking, gap_analysis, models/ ที่ Root) | A | TECH_STACK §42, FOLDER §14 | ให้ §14 อ้างโครง `services/ai/` เดียวกับ §42 | ตกหล่นจากรอบก่อน เป็น path/ชื่อเก่า |
| A-12 | DATABASE_MIGRATION_PLAN | §29, §31, §38 | ใช้คอลัมน์ `job_posting_id` แต่ DB ใช้ `job_id` (PROJECT_SPEC, DATASET ก็ใช้ `job_id`) | A | DATABASE §23-24 | เปลี่ยนเป็น `job_id` | ชื่อคอลัมน์ใน Migration ต้องตรง DB |
| A-13 | DATABASE_MIGRATION_PLAN | §21, §22, §24, §26 | รายการ Field ไม่ตรง DB: dataset_version (`version`, `source`), resume (`filename`), portfolio (`portfolio_url`, `title`, `description`, ไม่มี `accessible`), portfolio_project (`project_title`, `project_url`) | A | DATABASE §25, §12, §13, §14 | ปรับรายการ Field ให้ตรงชื่อและคอลัมน์ใน DB | MIG เป็นเอกสาร Implementation ไม่ใช่ตัวกำหนด Schema (MIG §1) |
| A-14 | DATABASE | §61 | ลำดับสร้างตารางต่างจาก MIG §5 (MIG §2 ให้ MIG เป็น SoT ของลำดับ) | A | DATABASE_MIGRATION_PLAN §2, §5 | เพิ่มหมายเหตุให้ใช้ลำดับ MIG §5 | ลดความขัดแย้งโดยไม่แก้ Schema |
| A-15 | ENVIRONMENT_SETUP | §16 | Private env ชื่อ `AI_INTERNAL_URL` ขณะที่ทั้งชุดใช้ `AI_SERVICE_URL` | A | ENV §15 | เปลี่ยนเป็น `AI_SERVICE_URL` | ชื่อ env ต้องตรงกัน (ก่อนสร้าง .env.example จริง) |
| A-16 | TECH_STACK | §33, §34, §56 | Backend port 3001, `NEXT_PUBLIC_API_URL`, `PORT`, และ host `python-ai` ขัดกับ 4000, `NEXT_PUBLIC_API_BASE_URL`, `BACKEND_PORT`, `ai-service` ใน ENV/FOLDER/API และ §35 ของ TECH เอง | A | ENV §15, §24-25; API §3 | ปรับตัวอย่างใน TECH §33, §34, §56 ให้ตรง ENV | ค่า Environment ต้องไม่กำกวมก่อน Phase 0 |
| A-17 | UI_UX_SPEC / API | UI §43-44; API §32 | UI เก็บ Satisfaction สเกล 1-5 แต่ API ตัวอย่างและ DB (`user_feedback.satisfaction` 0-100) ใช้ 0-100 ไม่มีการแปลง | A | DATABASE §28 | ระบุว่า Frontend แปลง 1-5 เป็น 0-100 (คูณ 20) ก่อนส่ง | สเกลข้อมูลต้องตรงกัน โดยไม่แก้ DB |
| A-18 | TECH_STACK | §39 | ผังราก Repository ไม่มี `.gitattributes` | A | FOLDER §3 | เพิ่ม `.gitattributes` | ผัง Root ต้องตรงกัน |
| A-19 | docs/decisions | 0004 การตัดสินใจข้อ 3 | เขียนว่า Python มี `POST /internal/analyze` และ `GET /health` "เท่านั้น" ทั้งที่ FOLDER §14-15 และ §42 วางโมดูล matching ใน Python | A | FOLDER §42, TECH §12 | แก้ถ้อยคำเป็นชุดเริ่มต้น และอ้าง C-01 | ADR ของผมเองขัดกับเอกสารต้นทาง |
| A-20 | docs/decisions, datasets | 0006 ข้อ 6; datasets/README | กฎ `DATASET_VERSION` ต้องตรงไฟล์ Metadata ขัดกับ `.env.example` (`development`) ตาม ENV §15 | A | ENV §15 | เพิ่มข้อยกเว้นค่า placeholder `development` | ADR/README ของผมเองขัดกับ ENV |
| A-21 | CLAUDE_INITIAL_IMPLEMENTATION_PROMPT (นอก repo) | Phase 0-3; รายชื่อเอกสาร | Phase 3 = Vertical Slice (ระบบรวม Phase 3 = Labour Market Dataset) และรายชื่อเอกสารไม่มี path `docs/` | A | CLAUDE §8, FOLDER §25 | ออกฉบับแก้ (Vertical Slice เป็น Milestone และระบุ path) | ไฟล์ไม่อยู่ในแผนผัง repo จึงแก้เป็นสำเนาแยก |

### B. Implementation Decision

| ID | File | Section | Issue | Type | Source of Truth | Proposed Resolution | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- |
| B-01 | FOLDER §10, TECH §58, API | JSON naming | TypeScript camelCase (`resultId`) ต่างจาก JSON snake_case (`result_id`) ของ API | B | API (wire), FOLDER §40 (TS) | แปลงที่ชั้น `apps/web/lib/api/` | กติกาทั้งสองมีอยู่ ต้องมี Mapping ตอน Implement |
| B-02 | API §21, §23; AI §64; IMPL §22 | Evidence DTO | รูป Evidence ที่ส่งให้ Frontend มีหลายแบบ | B | API §23 + DATABASE `skill_evidence` | ใช้ `source_type/source_reference/description` ตาม API §23 ตอน Phase 9 | เป็นตัวอย่างแนวคิด |
| B-03 | API §21, §24, §28, §31, §54 | explanation / guidance | explanation เป็น string และ object, guidance เป็น object แต่ DB เป็น TEXT | B | DATABASE §26, §27 | เก็บ summary เป็น TEXT และ guidance เป็น JSON ใน TEXT ตอน Phase 8-9 | ไม่ต้องเปลี่ยน Schema |
| B-04 | MIG §10 | search_path | `SET search_path` มีผลเฉพาะ Session | B | DATABASE §9 | ตั้งที่ Connection/Role ตอน Phase 1 | รายละเอียด Implementation |
| B-05 | MIG §53; ENV §13 | ชื่อ DB | `career_system_dev/test/prod` (ตัวอย่าง) กับ `career_system` | B | ENV §13 | ใช้ `career_system` ใน dev ตามที่ compose ตั้ง แยก test ภายหลัง | ทั้งคู่เป็นตัวอย่าง |
| B-06 | TECH §32; ADR 0003 | เวอร์ชัน | TECH ให้ใช้ stable ล่าสุด ADR 0003 ตรึง `postgres:17` | B | TECH §32, ADR 0003 | คงตามเหตุผลใน ADR และตรึง Node/Python ด้วย lockfile ตอน Phase 0 | บันทึกเหตุผลแล้ว |
| B-07 | CLAUDE §11 vs PROMPT | รูปแบบรายงาน | หัวข้อรายงานต่างกัน | B | CLAUDE §11 | ใช้ CLAUDE §11 และเพิ่ม `Commands to Run` | CLAUDE เป็นกติกาหลัก |
| B-08 | ENV §63, §66 vs IMPL §4 | ขอบเขต Phase 0 | Setup checklist รวม Migration/Seed ซึ่งเป็น Phase 1-2 | B | IMPLEMENTATION_PLAN §4, CLAUDE §8 | Phase 0 = ENV §63 ข้อ 1-6, 8-12 | ตรงกับ Acceptance ของ Phase 0 |
| B-09 | FOLDER §35; ENV | Temporary storage | ไม่ระบุที่เก็บและชื่อ env | B | ENV | กำหนดตอน Phase 4 | Implementation |
| B-10 | ENV §32; API §8 | /health | `GET /health` ไม่อยู่ใน Endpoint Overview ของ API | B | ENV §32, §39 | คง `/health` ที่ Root ของ Express และ Python | เป็น Ops endpoint |
| B-11 | MIG §38 vs DATABASE §39 | Index | รายการ Index ต่างกันเล็กน้อย | B | MIG §38 (ตัดสินตอน 021) | สร้างจาก Query Pattern จริง | ทั้งสองระบุเป็นตัวอย่าง |
| B-12 | ADR 0003 vs MIG §8 | schema_migrations | ADR เพิ่ม `checksum` จากแนวคิด (version, applied_at) | B | MIG §8 (แนวคิด) | คง ADR และปรับ MIG §8 ตอน Phase 1 | ไม่ใช่ตารางใหม่ของ DATABASE.md |

### C. Missing Decision (ไม่แก้ รอเจ้าของโครงการ)

| ID | File | Section | Issue | Type | Source of Truth | Proposed Resolution | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C-01 | API §35-38; FOLDER §14-15, §42; TECH §12; AI §46-47 | Matching contract | เอกสารกำหนดว่า Python คำนวณ Matching/Gap/Guidance และ Express Orchestrate (FOLDER §42) แต่ Internal API มีเฉพาะ `/internal/analyze` (สกัด Skill) และ Python อ่าน DB ไม่ได้ ไม่มี Contract ส่ง Occupation Profile/Demand ไป Python | C | TECH_STACK §12 + FOLDER §42 | กำหนด Contract (เช่น `POST /internal/match`: Express โหลด Profile+Demand ส่งให้ Python แล้วบันทึกผล) ก่อน Phase 7 | ต้องให้เจ้าของโครงการเลือก เพราะกระทบ API และไม่เปลี่ยน Architecture ที่ล็อก |
| C-02 | API §18; UI §15; DATABASE §11; TECH §50 | Analysis stage | สถานะ 12 ค่าแต่ `user_session.status` มี 6 ค่า ไม่มีตาราง Job | C | DATABASE §11 | เก็บ `PROCESSING` ใน DB และ Stage ในหน่วยความจำ หรือเพิ่มคอลัมน์ผ่าน Migration ใหม่ | เป็นการเปลี่ยน Database design จึงต้องรอคำสั่ง |
| C-03 | API §12, §16; ENV §53; PROJECT_SPEC §42; UI §97 ข้อ 20 | Consent กับเวลาสกัด Resume | การสกัด/วิเคราะห์ตอน Upload จะเกิดก่อน Consent | C | PROJECT_SPEC §42 | Upload = ตรวจสอบและเก็บชั่วคราว ประมวลผลหลัง `/analyze` และ Vertical Slice ใช้ข้อมูลสังเคราะห์ | ต้องตัดสินก่อน Phase 4 |
| C-04 | UI §65-66; API §49-50; DATABASE §35; ENV §15 | Retention | ไม่มีค่าระยะเวลาเก็บข้อมูล (มี `SESSION_TTL_MINUTES=60` เป็นตัวอย่าง) และไม่มี Endpoint ลบตามคำขอ | C | PROJECT_SPEC §33 | กำหนดระยะเวลาและ (ถ้าต้องการ) `DELETE /session/:id` | UI ต้องแสดงระยะเวลาก่อน Consent |
| C-05 | API §32-33; UI §42-44; DATABASE §28, §38 | SUS/Feedback | ไม่ระบุว่าใครคำนวณ SUS, ไม่เก็บรายข้อ, และ Feedback ถูกลบพร้อม Session (CASCADE) | C | DATABASE §28 | กำหนดวิธีคำนวณและที่เก็บ Feedback สำหรับ Evaluation | เกี่ยวกับ Database design และผลวิจัย |
| C-06 | DATABASE §10; MIG §12, §44; UI §8; API §8 | Major rows | ไม่มีข้อกำหนดแถวของสาขาที่ไม่มี Sub-major และไม่มี Endpoint ดึงรายการ Major | C | DATABASE §10 | กำหนด Convention ของ `major` และ `GET /majors` หรือ Config | ต้องรู้ก่อน Seed (Phase 1-2) |
| C-07 | PROJECT_SPEC §27; AI §37; API §21, §25; UI §20, §72 | Score scale | 0.82, 92.4, 86%, XX.X ไม่บอกสเกลมาตรฐาน | C | AI_MATCHING (Phase 7) | กำหนดสเกลเก็บ (เช่น 0-100) และรูปแบบแสดง | ก่อน Phase 7 |
| C-08 | TECH §52; DATABASE §53; DATASET §31; MIG §21, §67; IMPL §17; ENV §15, §61; API §53 | Version format | รูปแบบ Version หลายแบบ และ `career_result` มี `dataset_version_id` เดียวแต่ใช้หลาย Dataset | C | DATASET_SPEC §31 | กำหนดรูปแบบเดียวและนิยาม Release | ก่อน Phase 3 และ 7 |
| C-09 | AI §48, §50, §82 | Intermediate/versions | คะแนนกลางทางและ Version ย่อยไม่มีที่เก็บใน `career_result` | C | DATABASE §26 | เก็บใน Log/ไฟล์หรือรวมใน `algorithm_version` | ห้ามเพิ่มตารางโดยไม่มี Requirement |
| C-10 | UI §39; AI §61-62; DATABASE §10, §32 | Cross-Major label | ต้องรู้ว่า Career นอกสาย Major แต่ไม่มีแหล่งข้อมูลและ DB ห้าม Mapping ที่บังคับ | C | PROJECT_SPEC §7 | กำหนดวิธีตัดสินแบบไม่บังคับ (Config) ตอน Phase 7-10 | ต้องตัดสินโดยเจ้าของโครงการ |
| C-11 | DATASET §30 vs DATABASE | Evaluation storage | DATASET_SPEC แนะนำตาราง EVALUATION_* แต่ DB ไม่มี | C | DATABASE, FOLDER §22 | เก็บเป็นไฟล์ใน `datasets/evaluation/` | ตรงกับ CLAUDE §7 |
| C-12 | CLAUDE §3; TECH §86; DATABASE §67; MIG §2; ENV §62; IMPL §89; DATASET/AI header | ลำดับ SoT และป้ายสถานะ | มีลำดับความสำคัญ 4 แบบ และป้าย Draft กับ LOCKED ปนกัน | C | คำสั่งเจ้าของโครงการ: CLAUDE, TECH_STACK, DATABASE ตามหน้าที่ | บันทึกกติกาลำดับใน `docs/decisions/` และเปลี่ยนป้ายเมื่อประกาศ Freeze | ต้องให้เจ้าของโครงการยืนยัน |
| C-13 | API §44; TECH §44; AI §52-53 | Insufficient evidence | ไม่มี Response/Error สำหรับไม่พบหลักฐานเพียงพอ | C | AI_MATCHING §53 | กำหนดผลลัพธ์ที่ Complete พร้อมข้อความข้อจำกัด | ก่อน Phase 6 และ 9 |
| C-14 | IMPL §81; TECH §81; decisions | งานจิปาถะ | `Dataset Dashboard` ไม่ระบุขอบเขต, TECH §81 อ้าง ARCHITECTURE.md ที่ไม่มี, LICENSE, `datasets/raw/` เข้า Git หรือไม่ | C | CLAUDE §16 | ตัดสินตามเวลาที่เกี่ยวข้อง | ไม่กระทบ Phase 0 |
| C-15 | DATASET §62; AI §93 | พารามิเตอร์วิจัย | แหล่งข้อมูล ช่วงเก็บ น้ำหนัก Threshold Top-K Evaluation Protocol ยังเป็น TBD | C | DATASET_SPEC, AI_MATCHING | กำหนดใน Phase 3, 7, 12 | เป็น TBD ที่ตั้งใจ ไม่ใช่ความขัดแย้ง |

### D. No Conflict

| ID | File | Section | Issue | Type | Source of Truth | Proposed Resolution | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- |
| D-01 | FOLDER §42; API §17, §39 | ผู้เป็นเจ้าของ Matching | Express Orchestrate และ Python คำนวณ ตรงกันทุกเอกสาร (เหลือเพียง Contract = C-01) | D | FOLDER §42 | ไม่แก้ | - |
| D-02 | CLAUDE §15; IMPL §75, §90; FOLDER §52; MIG §72; ENV §53; API §68; PROJECT_SPEC §6 | Semester 1 | Vertical Slice เป็นก้าวแรก แล้วต่อเป็น MVP บน Web Full Stack Pilot ตรงกันทุกเอกสาร และ Semester 2 ทั้งคณะ | D | PROJECT_SPEC §6 | ไม่แก้ | ADR 0002 ตรงกับข้อความเดิมของ IMPL §90 |
| D-03 | PROJECT_SPEC §57; TECH §77-78; API §72; MIG §71 | ลิสต์ลำดับงานอื่น | เรียกว่า Step/Stage/Priority ไม่ใช่ Phase และมีตารางเทียบ | D | IMPLEMENTATION_PLAN §3 | ไม่แก้ | - |
| D-04 | DATABASE §2, §44; TECH §16; MIG §75 | Python กับ DB | Express เป็นเจ้าของ DB ตรงกัน (DATABASE §2 ผ่อนปรนเล็กน้อยแต่ §44 ชัดเจน) | D | DATABASE §44 | ไม่แก้ | - |
| D-05 | PROJECT_SPEC §34-35; DATABASE §7 | จำนวนตาราง | 17 กับ 19 ตาราง มีหมายเหตุใน PROJECT_SPEC §35 แล้ว | D | DATABASE §7 | ไม่แก้ | - |
| D-06 | PROJECT_SPEC §13; DATASET §8; DATABASE §15 | Skill category | 5/6/7 กลุ่ม DB ใช้ 7 ค่า | D | DATABASE §15 | ไม่แก้ | DB เป็น SoT |
| D-07 | PROJECT_SPEC §9.3; UI §12; DATABASE §13; API §14 | Portfolio status | DB/API/AI 8 ค่า UI แสดง 3 สถานะ `Private` ตรงกับ LOGIN_REQUIRED/INACCESSIBLE | D | DATABASE §13 | ไม่แก้ | - |
| D-08 | PROJECT_SPEC §15; AI §14; DATABASE | Confidence | High/Medium/Low กับตัวเลข 0-1 อนุญาตทั้งคู่ | D | AI_MATCHING §14 | ไม่แก้ | - |
| D-09 | TECH §19 vs API §6 | Response envelope | TECH เป็นตัวอย่างขั้นต่ำ API เป็นสัญญาจริง | D | API §6 | ไม่แก้ | - |
| D-10 | ทุกเอกสาร | ประเภทไฟล์ Resume | PDF/DOC/DOCX ตรงกัน (แก้คำพูดผิดของรอบก่อน) | D | API §11 | ไม่แก้ | - |
| D-11 | API §13; AI §55; DATABASE §13; UI §11 | Portfolio หลาย URL | รองรับตรงกัน | D | API §13 | ไม่แก้ | - |
| D-12 | API §19; AI §84; TECH §50 | Sync/Async | 202 + Polling ใช้ได้ AI ยอมให้ Sync ใน Prototype | D | API §19 | ไม่แก้ | - |
| D-13 | API §18; UI §15; TECH §50; PROJECT_SPEC §43 | Progress | 12 สถานะของ API = UI รายการอื่นเป็นชุดย่อย | D | API §18 | ไม่แก้ | - |
| D-14 | PROJECT_SPEC §37; UI §5; FOLDER §4 | จำนวนหน้า | 14 vs 13 หน้า UI เป็น SoT และรวมหน้าได้ | D | UI_UX §5 | ไม่แก้ | - |
| D-15 | CLAUDE §6; PROJECT_SPEC §7; ทุกเอกสาร | Locked principles | No Login, Major เป็น Context, Evidence-Based, Evidence Not Found, Match Score, Demand จาก Job Posting ตรงกันทุกไฟล์ และไม่ถูกแก้โดยรอบก่อน | D | CLAUDE §6 | ไม่แก้ | - |
| D-16 | IMPL §5.3 vs ADR 0003 | Rollback | IMPL ต้องการ Rollback; ADR ใช้ Reverse Migration ซึ่งเป็น Approach B ของ MIG §50 | D | MIG §50 | ไม่แก้ | - |
| D-17 | PROJECT_SPEC §5-6; TECH §66; IMPL §77; FOLDER §47; API §69 | ชื่อสาขา | `Film & Television` กับ `Film & Radio Television` และคำนำหน้า `สาขาวิชา` เป็นความต่างของป้าย ชื่อทางการให้ตรวจกับคณะก่อน Production (MIG §12) | D | MIG §12 | ไม่แก้ | - |

## 4. การแก้ไขที่ทำ (เฉพาะ True Conflict)

| ID | ที่แก้ | ผล |
| --- | --- | --- |
| A-01 | PROJECT_SPEC §74 | `Technology Stack: LOCKED (see TECH_STACK.md §85)` |
| A-02 | UI_UX_SPEC §98 | `Frontend Framework: Next.js + React + TypeScript + Tailwind CSS (LOCKED ...)` คง Component Library/Visual Theme เป็น TBD |
| A-03 | PROJECT_SPEC §73 | `PHASE 0-1` พร้อมหมายเหตุอ้าง IMPLEMENTATION_PLAN §3 |
| A-04 | TECH_STACK §24, §46; IMPLEMENTATION_PLAN §64 | เรียงเป็น Major > Session > Resume > Portfolio > Consent > Analyze |
| A-05 | API §12; DATABASE_MIGRATION_PLAN §23 | Resume status เป็น PENDING/PROCESSING/COMPLETED/FAILED (ตัด ERROR, DELETED) |
| A-06 | API §36-37; TECH_STACK §13 | Response evidence ใช้ `source_type` (8 ค่า) + `evidence_text`; Request `portfolio_projects[]` เพิ่ม `project_id`; เพิ่มหมายเหตุ |
| A-07 | API §63 | `src/lib/api/` เป็น `apps/web/lib/api/` |
| A-08 | FOLDER_STRUCTURE §39; ENVIRONMENT_SETUP §29 | ตัวอย่างชื่อ Migration ตาม MIG §5 |
| A-09 | DATABASE §47; DATASET_SPEC §55 | `scripts/import/` และ `scripts/` เป็น `scripts/dataset/` |
| A-10 | FOLDER_STRUCTURE §19, §20 | โฟลเดอร์ย่อยเป็น `skill/`, `job_posting/`, `occupation_skill/` ตาม DATASET §54 |
| A-11 | TECH_STACK §14 | แทนโครง `python-service/` ด้วยโครง `services/ai/` เดียวกับ §42 |
| A-12 | DATABASE_MIGRATION_PLAN §29, §31, §38 | `job_posting_id` เป็น `job_id` |
| A-13 | DATABASE_MIGRATION_PLAN §21, §22, §24, §26 | รายการ Field ตรงคอลัมน์ใน DATABASE.md |
| A-14 | DATABASE §61 | ระบุว่าเป็นลำดับเชิงแนวคิด ลำดับจริงใช้ MIG §5 |
| A-15 | ENVIRONMENT_SETUP §16 | `AI_INTERNAL_URL` เป็น `AI_SERVICE_URL` |
| A-16 | TECH_STACK §33, §34, §56 | Port 4000, `NEXT_PUBLIC_API_BASE_URL`, `BACKEND_PORT`, `ai-service`, `career_user@postgres` |
| A-17 | UI_UX_SPEC §43; API §32 | เพิ่มข้อความ: Frontend แปลง Satisfaction 1-5 เป็น 0-100 (คูณ 20) |
| A-18 | TECH_STACK §39 | เพิ่ม `.gitattributes` ในผัง Root |
| A-19 | docs/decisions/0004; FOLDER_STRUCTURE §15 | ถ้อยคำเป็นชุดเริ่มต้น/ชั่วคราว อ้าง C-01 |
| A-20 | docs/decisions/0006; datasets/README | เพิ่มข้อยกเว้นค่า placeholder `development` |
| A-21 | CLAUDE_INITIAL_IMPLEMENTATION_PROMPT (นอก repo) | สำเนาแก้: รายชื่อเอกสารมี path, Vertical Slice เป็น Milestone ไม่ใช่ Phase 3, อ้าง decisions |

นอกจากนี้ตารางเรื่องที่ยังเปิดใน `docs/decisions/README.md` ถูกแทนด้วยรายการ C-01 ถึง C-15 จากรายงานนี้

ไม่ได้แก้: Core architecture, Project scope, Locked technology stack, Matching concept, Evidence-Based principle, Major-as-context principle, Semester scope, Database design หลัก (การแก้ใน DATABASE_MIGRATION_PLAN เปลี่ยนเฉพาะชื่อ Field ให้ตรง DATABASE.md ไม่แตะ Schema) ไฟล์ต้นฉบับใน uploads ไม่ถูกแตะ

รายการที่เจ้าของโครงการควรดูเป็นพิเศษ เพราะแตะรายละเอียดของ Contract หรือ Workflow ในเอกสารหลัก:

- A-04 ลำดับ Consent ใน TECH_STACK และ IMPLEMENTATION_PLAN (ทำตาม Workflow ที่ล็อกใน PROJECT_SPEC §8 ไม่ได้เปลี่ยน Workflow)
- A-06 เพิ่ม `project_id` ใน Request และเปลี่ยนรูป evidence ของ Python ให้ตรง `skill_evidence`
- A-17 การแปลงสเกล Satisfaction (คูณ 20)

## 5. Audit รอบที่ 2

วิธี: รอบนี้ไม่ใช่การอ่านซ้ำทั้ง 14 ไฟล์ แต่เป็นการตรวจซ้ำเฉพาะจุดที่แก้ (เทียบ diff กับ zip ก่อนแก้: 14 ไฟล์เปลี่ยน ทุกบรรทัดตรงกับที่ตั้งใจ) ร่วมกับสคริปต์ตรวจข้ามเอกสารสำหรับแต่ละเงื่อนไข สคริปต์เป็นส่วนเสริมของการอ่านในรอบแรก ไม่ได้แทนการอ่าน

| เงื่อนไข | วิธีตรวจ | ผล |
| --- | --- | --- |
| ไม่มี True Conflict ค้าง | A-01 ถึง A-21 แก้แล้วและตรวจ diff; ค้นหา `TO BE FINALIZED` ทุกไฟล์ | ผ่าน เหลือเฉพาะพารามิเตอร์วิจัย/ภาพลักษณ์ที่ตั้งใจให้เปิด (Visual Theme, Component Library, แหล่งข้อมูล, น้ำหนัก, Top-K) |
| ไม่มี path เก่า | ค้นหา `frontend/`, `backend/`, `ai-service/`, `src/`, `python-service`, `python-ai`, `scripts/import`, ชื่อ Migration เก่า, `career-prediction-system` ใน repo ทั้งหมดและ Prompt ฉบับแก้ | ผ่าน เหลือ 3 จุดที่เป็นการเล่าประวัติ (ADR 0001, ADR 0004) และ `apps/api/src/` ซึ่งถูกต้อง |
| Phase numbering ระบบเดียว | เทียบชื่อและเลข Phase 0-13 ของ CLAUDE §8, IMPLEMENTATION_PLAN §3, FOLDER_STRUCTURE §51 แบบโปรแกรม; ค้นหาการผสมที่ขัด (Phase 3 + Vertical Slice, Phase 12 + Deployment, PHASE 1) | ผ่าน ชื่อและเลขตรงกันทั้งสามที่ ลิสต์อื่นใช้คำว่า Step/Stage/Priority พร้อมตารางเทียบ |
| API และ Python internal endpoint ตรงกัน | ตรวจการอ้าง `/internal/` ทุกไฟล์ และรูป Request/Response | ผ่าน `POST /internal/analyze` ตรงกันใน API §35-37, TECH §13, FOLDER §15, ADR 0004; ไม่มี `/process/*` นอกคำบรรยายประวัติ Contract ของ Matching ยังไม่กำหนด (C-01) |
| Database และ migration plan ตรงกัน | แยกคอลัมน์จาก `CREATE TABLE` ใน DATABASE.md เทียบกับรายการ Field ใน MIG §11-37 (15 ตาราง) | ผ่าน ไม่มีคอลัมน์ที่ MIG อ้างแต่ DB ไม่มี (สิ่งที่โปรแกรมรายงานใน §29 คือชื่อเชิงแนวคิด `dataset_version` ของ `dataset_version_id`) ชื่อไฟล์ Migration และสถานะ Resume ตรงกัน |
| Dataset structure ตรง DATASET_SPEC | เทียบ DATASET §54, FOLDER §19-20, datasets/README, ADR 0006, path Script | ผ่าน `raw/ processed/ evaluation/ metadata/` และโฟลเดอร์ย่อยตรงกัน Script อยู่ที่ `scripts/dataset/` |
| Tech stack ตรงกัน | ตรวจบรรทัดสถานะ `Technology Stack`/`Frontend Framework` ทุกไฟล์; นับคำต้องห้าม (MySQL, MariaDB, MongoDB, Yii, Vue, PHP) เทียบต้นฉบับ; Port/ชื่อ env | ผ่าน ทุกไฟล์ LOCKED จำนวนคำต้องห้ามเท่าเดิม Port 4000 และ `AI_SERVICE_URL` ตรงกันทุกที่ |
| Semester 1/2 scope ตรงกัน | อ่านข้อความ Semester ทุกไฟล์ | ผ่าน Semester 1 = Pilot บน Web Full Stack ให้ Core Engine ทำงาน (เริ่มที่ Vertical Slice แล้วต่อเป็น MVP) Semester 2 = 4 สาขา และไม่มีการแก้ขอบเขต |
| Privacy rules ตรงกัน | ตรวจลำดับ Consent ในทุก Flow (fenced) ของ 14 ไฟล์และ Prompt (23 flow) | ผ่าน ทุก Flow เรียง Resume/Portfolio ก่อน Consent (7 รายการที่ตัวตรวจแจ้งเป็นผลบวกลวง ไม่มี Upload ในบล็อก; อีก 1 เป็น Checklist) ค่า Retention และเวลา Parse Resume ยังไม่กำหนด (C-03, C-04) ซึ่งเป็น Missing Decision ไม่ใช่ความขัดแย้ง |

### ข้อจำกัดของ Audit นี้

- การอ่านรอบแรกทำเป็นชุดต่อเนื่อง โดยจดบันทึกสรุปหลังอ่านแต่ละส่วน การเทียบข้ามเอกสารทำจากบันทึกเหล่านั้นและการเปิดอ่านซ้ำในจุดที่สงสัย ความขัดแย้งเล็กที่ไม่ได้จดอาจหลุด
- รอบที่ 2 ตรวจเฉพาะจุดที่แก้และ 9 เงื่อนไข ไม่ใช่การอ่านครบทั้งชุดอีกครั้ง
- ตัวอย่างในเอกสารที่ระบุว่าเป็น "ตัวอย่าง" ถูกตรวจเฉพาะกรณีที่ขัดกับค่าที่ใช้จริง (ชื่อ path, env, enum, ชื่อคอลัมน์)
- รอบก่อนหน้าเคยยืนยันว่าไม่เหลือ path เก่า ซึ่งไม่จริง (พบ 4 จุดรอบนี้) จึงเพิ่มการค้นหา pattern กว้างขึ้นในรอบที่ 2

## 6. สถานะ

**DOCUMENTATION FREEZE: READY**

เหตุผล: ครบทุกเงื่อนไขของข้อ 10 ไม่เหลือ True Conflict และ Missing Decision ทั้ง 15 ข้อ (C-01 ถึง C-15) ต้องตัดสินตั้งแต่ Phase 1 เป็นต้นไป ไม่มีข้อใดต้องตัดสินก่อนหรือระหว่าง Phase 0 (ข้อที่เร็วที่สุดคือ C-06 ที่ Phase 1-2)

เงื่อนไขหลัง Freeze: การแก้เอกสารต้องเขียนบันทึกใน `docs/decisions/` และได้รับอนุมัติจากเจ้าของโครงการก่อน (ตาม `CLAUDE.md` §3 และ `IMPLEMENTATION_PLAN.md` §87)

## 7. คำสั่งเสนอสำหรับ Phase 0

ยังไม่ได้รัน ใช้ในสภาพแวดล้อมที่ต่อเน็ตและมี Docker ได้ (Session ที่ผมใช้ติดตั้ง npm/pip และรัน Docker ไม่ได้) ใช้คู่กับไฟล์ `CLAUDE_INITIAL_IMPLEMENTATION_PROMPT.md` ฉบับแก้

```text
ทำ Phase 0 (Project Setup) เท่านั้น ตาม CLAUDE.md §8 และ IMPLEMENTATION_PLAN.md §4
ห้ามเริ่ม Phase 1 (ไม่สร้าง Migration, Seed, ตารางฐานข้อมูล) และห้ามตัดสินเรื่องที่ค้างใน docs/decisions/README.md (C-01 ถึง C-15)

ก่อนเริ่ม: อ่าน CLAUDE.md, docs/decisions/0001-0006 และ docs/decisions/README.md แล้วสรุปแผน Phase 0 ให้ยืนยันก่อนลงมือ

ขอบเขต:
1. apps/web: Next.js + React + TypeScript + Tailwind CSS (App Router ไม่มี src/), หน้าแรกแบบขั้นต่ำ, ESLint, Dockerfile
2. apps/api: Node.js + Express + TypeScript ตามชั้น routes/controllers/services/repositories, GET /health (Root) ที่รายงานสถานะ backend, database, ai_service, ESLint, Dockerfile, เชื่อม PostgreSQL ด้วย node-postgres (pg) ไม่ใช้ ORM
3. services/ai: Python + FastAPI + Uvicorn + Pydantic, app/main.py รันด้วย python -m app.main, GET /health, requirements.txt ที่ตรึงเวอร์ชัน, Dockerfile, ยังไม่สร้าง /internal/analyze
4. docker-compose.yml: เพิ่ม frontend, backend, ai-service ต่อจาก postgres เดิม ใช้ชื่อ Service ตามเอกสาร (build context ./apps/web, ./apps/api, ./services/ai) พอร์ต 3000, 4000, 8000, 5432
5. Environment: ใช้ .env.example ที่มี ห้าม Commit .env
6. Git: git init, branch main และ develop, commit ตาม Conventional Commits
7. ตรึงเวอร์ชัน Node.js และ Python ด้วย lockfile/ไฟล์กำหนดเวอร์ชัน แล้วบันทึกการตัดสินใจใน docs/decisions/

ห้าม: เพิ่ม Feature นอกขอบเขต, Authentication, Admin Dashboard, ใช้ข้อมูลผู้ใช้จริง, แก้ Source of Truth โดยไม่มีบันทึกใน docs/decisions/

เกณฑ์ผ่าน (IMPLEMENTATION_PLAN §4): docker compose up --build เริ่มทุก Service ได้, GET http://localhost:4000/health, http://localhost:8000/health และ http://localhost:3000 ตอบสำเร็จ, backend ติดต่อ PostgreSQL และ ai-service ได้, ผ่าน lint, type check และ unit test พื้นฐานของทั้ง 3 Service

รายงานตาม CLAUDE.md §11 เพิ่มหัวข้อ Commands to Run และระบุผลทดสอบจริง ถ้าทดสอบข้อใดไม่ได้ให้ระบุว่า "ไม่ได้ทดสอบ" พร้อมเหตุผล
```

