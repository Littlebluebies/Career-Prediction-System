# 0001: โครงสร้าง Repository

- สถานะ: Accepted
- วันที่: 2026-09-20
- การยืนยัน: เจ้าของโครงการสั่งให้ดำเนินการต่อหลังตรวจว่าไม่ขัดกับชิ้นงาน (2026-09-20)
- ผู้ตัดสิน: เจ้าของโครงการกำหนดโครงสร้างหลัก ส่วนรายละเอียดที่เหลือเลือกตามคำสั่งให้แก้ความเสี่ยงโดยตรง เจ้าของโครงการเปลี่ยนได้ก่อนเริ่มเขียนโค้ด

## บริบท

`FOLDER_STRUCTURE.md` ฉบับเดิม (§3, §54) ใช้ `frontend/`, `backend/`, `ai-service/`, `docker/`, `LICENSE` และวาง `docs/` แบบแบน เจ้าของโครงการกำหนดโครงสร้างใหม่ `CLAUDE.md` และ `DATABASE_MIGRATION_PLAN.md` §5 ใช้โครงสร้างใหม่นี้อยู่แล้ว

## การตัดสินใจ

1. Application อยู่ใน `apps/web` (Next.js), `apps/api` (Express) และ `services/ai` (Python) `apps/web` ไม่มีโฟลเดอร์ `src/`
2. เอกสารอยู่ใน `docs/00-source-of-truth`, `01-architecture`, `02-database`, `03-ai-data`, `04-design` และ `decisions`
3. ไม่มีโฟลเดอร์ `docker/` Dockerfile ของแต่ละ Service อยู่ในโฟลเดอร์ของ Service นั้น ไฟล์ LICENSE เพิ่มเมื่อเจ้าของโครงการเลือกสัญญาอนุญาต
4. ชื่อ Service ใน `docker-compose.yml` คงเดิม (`frontend`, `backend`, `ai-service`, `postgres`) เพราะ `AI_SERVICE_URL=http://ai-service:8000` ใช้ชื่อ Service เป็น Hostname เปลี่ยนเฉพาะ build context
5. เพิ่มจากแผนผังที่เจ้าของโครงการกำหนด 4 จุด เพราะเอกสารระบุไว้:
   - `apps/api/src/clients/` เก็บ `python.client.ts` (`FOLDER_STRUCTURE.md` §12, `API.md` §64)
   - `datasets/metadata/` (`DATASET_SPEC.md` §32, ดู 0006)
   - `database/seed/README.md` และ `database/schema/README.md` (`DATABASE_MIGRATION_PLAN.md` §5)
   - `.gitattributes` (ดู 0005)
6. ชื่อไฟล์ TypeScript ใช้ kebab-case ตาม `FOLDER_STRUCTURE.md` §39 ตัวอย่างเดิมที่เป็น camelCase (`skillGap.*`, `requestId`, `rateLimit`) ถูกแก้ และ `middleware/` เปลี่ยนเป็น `middlewares/`
7. Package manager คือ npm (ค่าเริ่มต้นใน `ENVIRONMENT_SETUP.md` §8) แต่ละ App มี `package.json` ของตัวเอง ไม่ใช้ Workspace และไม่มี `package.json` ที่ Root
8. โฟลเดอร์ที่เอกสารระบุแต่ยังไม่อยู่ใน Scaffold (`utils/`, `constants/`, `hooks/`, `config/`, `evaluation/`) สร้างเมื่อมีโค้ดที่ต้องใช้

## ผลที่ตามมา

เอกสารที่แก้ให้ตรงกับโครงสร้างนี้:

| เอกสาร | ส่วนที่แก้ |
| --- | --- |
| FOLDER_STRUCTURE | §3, §4, §5-§7, §9-§12, §14-§19, §23, §25, §26, §31, §42, §43, §49-§52, §54, §56 |
| ENVIRONMENT_SETUP | §11, §17, §19-§23, §32-§35, §67 |
| TECH_STACK | §39-§42 |
| IMPLEMENTATION_PLAN | §4 |
| API | §64, §65 |

ไฟล์ต้นฉบับที่แนบมาตอนเริ่มโครงการยังเป็นฉบับเดิม ให้ใช้ฉบับใน `docs/`
