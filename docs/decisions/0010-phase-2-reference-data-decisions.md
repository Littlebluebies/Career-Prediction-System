# 0010: การตัดสินใจของ Phase 2 (Reference Data / Knowledge Dataset)

- สถานะ: Accepted
- วันที่: 2026-10-04
- ผู้ตัดสิน: เจ้าของโครงการ (เลือกตามข้อเสนอก่อนเริ่ม Phase 2)

## บริบท

`DATASET_SPEC.md` §2.3, §5.1 และ §58 ข้อ 4 ห้ามสร้าง Occupation จากความคิดเห็นของผู้พัฒนาเพียงอย่างเดียว ต้องเริ่มจากแหล่งมาตรฐาน (ESCO / O*NET) แต่ไม่ได้เลือกแหล่ง ขอบเขต รูปแบบ Version และวิธีจัดการข้อมูลดิบ นอกจากนี้ `IMPLEMENTATION_PLAN.md` §6 ให้สร้าง Occupation Skill ใน Phase 2 ขณะที่ `demand` ต้องคำนวณจาก Job Posting (`DATASET_SPEC.md` §24) ซึ่งเป็น Phase 3

## การตัดสินใจ

1. **แหล่งมาตรฐาน: ESCO** (European Skills, Competences, Qualifications and Occupations) เป็นแหล่งหลักของ Occupation, Skill และความสัมพันธ์ Occupation–Skill (essential / optional) ใช้ภาษาอังกฤษ บันทึกเวอร์ชันที่ใช้ใน Metadata ข้อมูลตลาดแรงงานไทยเข้ามาใน Phase 3 ผ่าน Job Posting
2. **ขอบเขต Phase 2: Pilot ของ Semester 1** (`CLAUDE.md` §15, `DATASET_SPEC.md` §38) เน้น CF10 Web Development และ CF11 UI/UX & Digital Product ส่วน Semester 2 ขยายด้วย Pipeline เดียวกัน (`DATASET_SPEC.md` §39-40)
3. **`occupation_skill` ใน Phase 2** สร้างเฉพาะความสัมพันธ์จาก ESCO พร้อม `source` ส่วน `importance` และ `demand` เป็น `NULL` และคำนวณภายหลัง (demand: Phase 3 ตาม `DATASET_SPEC.md` §24 / importance: ตาม `AI_MATCHING_SPEC.md`)
4. **รูปแบบ Version (C-08 ส่วนรูปแบบ):** `version` = `YYYY.NN` เช่น `2026.01` แยกจาก `dataset_name` ชื่อไฟล์ Metadata = `<dataset_name>_<version>.json` (ADR 0006) ส่วนนิยาม Release ที่ครอบคลุมหลาย Dataset (`dataset_version_id` ของ `career_result`) ยังเปิดอยู่ ตัดสินก่อน Phase 3
5. **ข้อมูลดิบ (C-14 ส่วนของแหล่งมาตรฐาน):** ไม่ Commit ชุดข้อมูล ESCO ฉบับเต็ม เก็บไว้ที่ `datasets/raw/esco/<esco-version>/` (อยู่ใน `.gitignore`) และบันทึก URL, เวอร์ชัน, วันที่ดาวน์โหลด และ SHA-256 ใน Metadata เพื่อให้ดาวน์โหลดเวอร์ชันเดียวกันแล้วทำซ้ำได้ ส่วนผลที่คัดแล้วใน `datasets/processed/` Commit ได้ เรื่อง Job Posting ดิบยังตัดสินใน Phase 3
6. **Script ประมวลผล: Python 3.13 ใน `scripts/dataset/`** ใช้เฉพาะ Standard Library (`FOLDER_STRUCTURE.md` §24)
7. **ชื่อสาขาทางการ:** เจ้าของโครงการตรวจชื่อจากข้อมูลทางการของคณะระหว่าง Phase 2 และใส่ใน Reference Seed ตอนท้าย Phase ระหว่างนี้ใช้ Development Seed (DEMO)

## หมายเหตุ

- `datasets/raw/esco/` เก็บตามแหล่ง (ESCO เป็นชุดเดียวที่มีทั้ง Occupation และ Skill) ส่วน `datasets/processed/` แบ่งตามชนิด (`occupation/`, `skill/`, `occupation_skill/`) ตามตัวอย่างใน `DATASET_SPEC.md` §54
- การตรวจผลการคัดเลือกโดยผู้วิจัยหรือผู้เชี่ยวชาญเป็นขั้น Validation ไม่ใช่แหล่งข้อมูลหลัก (`DATABASE_MIGRATION_PLAN.md` §18)

## ผลที่ตามมา

- `.gitignore` เพิ่ม `datasets/raw/esco/`
- `docs/decisions/README.md`: C-08 ตัดสินส่วนรูปแบบ Version แล้ว และ C-14 ตัดสินส่วนข้อมูลดิบของแหล่งมาตรฐานแล้ว

## ส่วนเพิ่มเติม (2026-10-05): ผลการสำรวจ ESCO v1.2.1 และการตัดสินใจเพิ่ม

- ผู้ตัดสิน: เจ้าของโครงการ
- ข้อมูล: ESCO v1.2.1, Classification, English, CSV ดาวน์โหลด 2026-10-05 10:24 (UTC+07:00)

ผลการสำรวจ: occupations 3,043, skills 13,960, occupation-skill relations 126,051 (essential 67,600 / optional 58,451)

8. **เกณฑ์คัดเลือก Occupation ของ Pilot:** ค้นคำของอาชีพเป้าหมายใน `DATASET_SPEC.md` §38 จาก `preferredLabel` และ `altLabels` ของ ESCO แล้วให้ผู้วิจัยตรวจ คัดออกพร้อมบันทึกเหตุผล ผลเบื้องต้นได้ 5 อาชีพ: CF10 = web developer (2513.5), user interface developer (2512.5) / CF11 = user interface designer (2513.3), user experience analyst (2511.19), web designer (2166.15) คัดออก: technical communicator (altLabel "user experience designer" แต่หน้าที่หลักคือเขียนเอกสารเทคนิค ขัด `DATASET_SPEC.md` §7.2), cloud software developer (altLabel "full stack cloud software engineer" เป็นงาน Cloud)
9. **Back-end / Full-stack Developer:** ESCO ไม่มี จึงไม่สร้างใน Phase 2 และพิจารณาเป็น Candidate Occupation ใน Phase 3 เมื่อพบใน Job Posting ไทย (source = Job Posting Dataset) ตาม `DATASET_SPEC.md` §5.1
10. **ชื่อ Skill:** `skill_name` = ESCO `preferredLabel` ส่วน ESCO `altLabels` เป็น `skill_alias` โดย Alias ที่ชี้ไปหลาย Skill ถูกตัดทิ้งและนับจำนวน เทคโนโลยีที่ ESCO ไม่มี (เช่น React, Node.js, Figma) เพิ่มใน Phase 3 จาก Job Posting
11. **ความสัมพันธ์ Occupation–Skill:** นำเข้าทั้ง essential และ optional โดยไม่กรอง บันทึกชนิดใน `occupation_skill.source` เช่น `ESCO v1.2.1: essential`
12. **Traceability ของ Skill:** ไม่แก้ Schema ใน Phase 2 ESCO URI ของ Skill อยู่ใน `datasets/processed/skill/` และ Metadata ส่วน Occupation ใช้ `occupation.source` / `source_identifier` (ESCO URI)

## ส่วนเพิ่มเติม 2 (2026-10-05): หมวดหมู่ Skill และ Pipeline นำเข้า

- ผู้ตัดสิน: เจ้าของโครงการ (ข้อ 13 เลือกแบบ A) ข้อ 14-17 เป็นรายละเอียดการ Implement ตามข้อเสนอ เปลี่ยนได้ก่อนปิด Phase 2

13. **หมวดหมู่ Skill (`skill.category`):** ใช้กฎจากลำดับชั้น Skill ของ ESCO ตรวจตามลำดับ ใช้กฎแรกที่ตรง และบันทึกกฎที่ใช้ในคอลัมน์ `category_rule` ของ `datasets/processed/skill/skill.csv` เพื่อให้ตรวจย้อนได้ (`DATASET_SPEC.md` §34)

    | กฎ | กลุ่ม ESCO ที่เป็นบรรพบุรุษ (code + preferredLabel ใน `skillGroups_en.csv`) | หมวดหมู่ |
    | --- | --- | --- |
    | R1 | S1.11 designing systems and products, S1.12 creating artistic, visual or instructive materials | DESIGN |
    | R2 | S1 communication, collaboration and creativity | COMMUNICATION |
    | R3 | S4 management skills, 04 business, administration and law | BUSINESS |
    | R4 | 02 arts and humanities | CREATIVE |
    | R5 | 06 information and communication technologies (icts), S5 working with computers, S7 constructing | TECHNICAL |
    | R6 | S2 information skills, 03 social sciences, journalism and information | OTHER |

    ข้อยกเว้นอยู่ใน `scripts/dataset/esco/category_overrides.csv` ทุกแถวต้องมีเหตุผล ใช้ 3 เกณฑ์: ชื่อซอฟต์แวร์หรือประเภทซอฟต์แวร์ -> SOFTWARE_TOOL (ESCO ไม่มีกลุ่มนี้), ความรู้ด้านการออกแบบ Interaction / Usability -> DESIGN, และ natural language processing -> TECHNICAL ผล Pilot: TECHNICAL 101, SOFTWARE_TOOL 28, BUSINESS 20, COMMUNICATION 16, DESIGN 15, OTHER 8, CREATIVE 3 (รวม 191) เจ้าของโครงการ (และอาจารย์ที่ปรึกษา) ตรวจผลก่อนปิด Phase
14. **Pipeline (`scripts/dataset/`, ชื่อไฟล์ตาม `FOLDER_STRUCTURE.md` §24 และ `DATASET_SPEC.md` §55 ที่อนุญาตให้ตั้งชื่อตาม Stack):** `build_esco_reference.py` (Raw -> Processed + Metadata), `validate.py` (Data Quality Checks ตาม `DATASET_SPEC.md` §32-35), `import.py` (ตรวจด้วย `validate.py` แล้วสร้าง Reference Seed SQL), `common.py` (ค่า Version, Path และค่าที่อนุญาตที่ใช้ร่วมกัน) ผลลัพธ์ต้องเหมือนเดิมทุกครั้งที่รันซ้ำ (Deterministic) ส่วน `validate.py` สร้างใน Phase 2 เร็วกว่าที่ ADR 0006 ข้อ 7 ระบุ (Phase 3) เพราะต้องตรวจข้อมูลก่อนนำเข้า
15. **การนำเข้า: สร้างไฟล์ SQL แทนการเขียนลง Database ตรง** `import.py` สร้าง `database/seed/reference/NN_<table>.seed.sql` (Commit เข้า Git, ห้ามแก้ด้วยมือ) และโหลดด้วย `scripts/database/seed.sh reference` ใน Transaction เดียว เหตุผล: Python ใช้ Standard Library ได้ต่อ (ไม่ต้องมี Database Driver), ข้อมูลที่เข้า Database ตรวจได้ใน Git, ใช้ `seed.sh` และ `ON CONFLICT DO NOTHING` แบบเดียวกับ Phase 1 Metadata แปลงลง `dataset_version` ตาม ADR 0006 ข้อ 5 (`processed_at` เว้นว่างเพราะไม่มีในตารางแปลง)
16. **แยกข้อมูล DEMO กับ Reference (`DATASET_SPEC.md` §56):** `seed.sh` และ `reset.sh` รับโหมด `development` (ค่าเริ่มต้น) หรือ `reference` และ `seed.sh` หยุดถ้า Database มีข้อมูลของอีกโหมดอยู่แล้ว `test.sh` ทดสอบทั้ง 2 โหมดบน Test Database ใหม่แต่ละรอบ (`database/schema/tests_reference.sql`)
17. **Career Family ใน Reference Seed:** ใส่ครบ 15 กลุ่มตาม `DATABASE.md` §19 (Initial Framework) ส่วน Occupation มีเฉพาะ CF10 / CF11 ตามข้อ 2 ส่วนตาราง `major` ยังว่างใน Reference Seed จนกว่าจะได้ชื่อสาขาทางการ (ข้อ 7)
