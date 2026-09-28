# docs/decisions/

โฟลเดอร์นี้บันทึกการตัดสินใจที่เอกสาร Source of Truth เปิดให้เลือกภายหลัง และการตัดสินใจที่ทำให้ต้องแก้เอกสาร

ตาม `CLAUDE.md` §3 และ `IMPLEMENTATION_PLAN.md` §87 เมื่อเอกสารขัดกันหรือต้องเปลี่ยนสิ่งที่ล็อกไว้ ให้ทำตามลำดับ:

```text
ระบุปัญหาและเอกสารที่เกี่ยวข้อง -> บันทึกการตัดสินใจที่นี่ -> แก้เอกสาร -> Implement
```

## รูปแบบไฟล์

ตั้งชื่อ `NNNN-หัวข้อสั้น.md` เริ่มด้วยสถานะ วันที่ และผู้ตัดสิน จากนั้นมี 4 หัวข้อ: บริบท, การตัดสินใจ, เหตุผล (ถ้ามี), ผลที่ตามมา (เอกสารและโค้ดที่ต้องแก้)

## รายการ

| เลข | เรื่อง | สถานะ |
| --- | --- | --- |
| [0001](0001-repository-layout.md) | โครงสร้าง Repository, package manager | Accepted |
| [0002](0002-phase-numbering-and-semester-1-scope.md) | เลข Phase และขอบเขต Semester 1 | Accepted |
| [0003](0003-database-tooling.md) | Migration, DB client, Rollback, PostgreSQL version | Accepted |
| [0004](0004-ai-service.md) | Python framework, โครงสร้าง, Internal endpoint | Accepted |
| [0005](0005-repository-hygiene-and-privacy.md) | `.gitattributes`, `.gitignore`, Fixture, ข้อมูลส่วนบุคคล | Accepted |
| [0006](0006-dataset-metadata.md) | ที่เก็บและรูปแบบ Dataset Metadata | Accepted |
| [0007](0007-documentation-audit-and-freeze.md) | Documentation Audit และ Freeze (READY) — Audit Record ไม่ใช่ Source of Truth ใหม่ | Accepted |
| [0008](0008-runtime-and-dependency-versions.md) | Runtime (Node 24 / Python 3.13) และ Dependency Versions ที่ตรึงสำหรับ Phase 0 | Accepted |

0001 ถึง 0006 ตัดสินโดยเจ้าของโครงการ (โครงสร้างหลัก) และ Claude (รายละเอียดที่เหลือ ตามคำสั่งให้แก้ความเสี่ยงโดยตรง) เจ้าของโครงการสั่งให้ดำเนินการต่อหลังตรวจว่าไม่ขัดกับชิ้นงาน (2026-09-20) และเปลี่ยนได้ก่อนเริ่มเขียนโค้ดส่วนที่เกี่ยวข้อง

เอกสารที่แนบตอนเริ่มโครงการเป็นฉบับเดิม ให้ใช้ฉบับใน `docs/` ซึ่งแก้ตามการตัดสินใจเหล่านี้แล้ว

## เรื่องที่ยังเปิดอยู่

รายการนี้มาจาก Documentation Audit (2026-09-20) รายงานฉบับเต็มอยู่ใน [0007](0007-documentation-audit-and-freeze.md) รหัส C-xx ตรงกับรายงาน ทุกข้อรอเจ้าของโครงการตัดสิน ไม่ขัดขวาง Phase 0

| รหัส | เรื่อง | ข้อเสนอ | ตัดสินก่อน |
| --- | --- | --- | --- |
| C-01 | Contract ที่ Express ใช้เรียก Python สำหรับ Matching, Skill Gap, Guidance (`API.md` มีแต่ `/internal/analyze`) | Express โหลด Occupation Profile และ Demand จาก DB ส่งให้ Python (เช่น `POST /internal/match`) แล้วบันทึกผลเอง | Phase 7 |
| C-02 | ที่เก็บ Analysis stage 12 ค่า (`user_session.status` มี 6 ค่า) | เก็บ `PROCESSING` ใน DB และ Stage ในหน่วยความจำ หรือเพิ่มคอลัมน์ผ่าน Migration ใหม่ | Phase 9 |
| C-03 | เวลาประมวลผล Resume เทียบกับ Consent | Upload เก็บชั่วคราวเท่านั้น ประมวลผลหลัง `/analyze` และ Vertical Slice ใช้ข้อมูลสังเคราะห์ | Phase 4 |
| C-04 | ระยะเวลาเก็บข้อมูล และ Endpoint ลบตามคำขอ | กำหนดค่าเดียวใช้ทั้ง Consent, Session TTL และ Cleanup | Phase 10 และก่อน Production |
| C-05 | SUS: ใครคำนวณ เก็บรายข้อไหม และ Feedback ถูกลบพร้อม Session | Backend คำนวณ และกำหนดที่เก็บ Feedback ที่ไม่ถูกลบตาม Session | Phase 9-12 |
| C-06 | แถวใน `major` ของสาขาที่ไม่มี Sub-major และวิธีดึงรายการ Major | กำหนด Convention ของ `major_name` และ `GET /majors` หรือ Config | Phase 1-2 |
| C-07 | สเกลและรูปแบบแสดง Match Score | เก็บ 0-100 แสดงทศนิยม 1 ตำแหน่ง | Phase 7 |
| C-08 | รูปแบบ Version ของ Dataset และ Algorithm และความหมายของ `dataset_version_id` | รูปแบบเดียว และนิยาม Release ที่ครอบคลุมหลาย Dataset | Phase 3 |
| C-09 | ที่เก็บคะแนนกลางทางและ Version ย่อย | Log หรือไฟล์ หรือรวมใน `algorithm_version` | Phase 7 |
| C-10 | วิธีตัดสินป้าย Cross-Major | Config ที่ไม่บังคับ ไม่ใช้เป็น Filter | Phase 7-10 |
| C-11 | ที่เก็บ Evaluation Dataset | ไฟล์ใน `datasets/evaluation/` (ไม่เพิ่มตาราง) | Phase 12 |
| C-12 | กติกาลำดับ Source of Truth และป้าย Draft กับ LOCKED | ตามหน้าที่: CLAUDE.md, TECH_STACK.md, DATABASE.md และตาราง `ENVIRONMENT_SETUP.md` §62 | ตอนประกาศ Freeze |
| C-13 | ผลลัพธ์กรณีหลักฐานไม่เพียงพอ | ตอบสถานะสำเร็จพร้อมข้อความข้อจำกัด ไม่ใช้ Error | Phase 6, 9 |
| C-14 | `datasets/raw/` เข้า Git หรือไม่, `LICENSE`, ขอบเขต Dataset Dashboard, อ้างอิง ARCHITECTURE.md ที่ไม่มี | ตัดสินตามเวลาที่เกี่ยวข้อง | ตามเวลา |
| C-15 | พารามิเตอร์วิจัย (แหล่งข้อมูล, น้ำหนัก, Threshold, Top-K, Evaluation Protocol) | กำหนดจากงานวิจัย | Phase 3, 7, 12 |
| - | เวอร์ชัน Node.js และ Python ที่ตรึง (`ENVIRONMENT_SETUP.md` §7, §9) | ตรึงด้วย lockfile ตอนเริ่ม | Phase 0 |
