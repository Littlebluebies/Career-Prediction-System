# 0004: Python AI Service

- สถานะ: Accepted (ตัวเลือกที่ Claude เลือกตามคำสั่งให้แก้ความเสี่ยงโดยตรง เจ้าของโครงการเปลี่ยนได้ก่อนเริ่ม Phase 0)
- วันที่: 2026-09-20
- การยืนยัน: เจ้าของโครงการสั่งให้ดำเนินการต่อหลังตรวจว่าไม่ขัดกับชิ้นงาน (2026-09-20)

## บริบท

- ไม่มีเอกสารใดระบุ Web framework ของ Python Service (`ENVIRONMENT_SETUP.md` §33 เขียนว่า "ตาม Framework ที่เลือกใช้")
- โครงสร้างโฟลเดอร์ไม่ตรงกัน: `FOLDER_STRUCTURE.md` §14 (`parsers/`, `preprocessing/`), `TECH_STACK.md` §42 (`extraction/`, `evidence/`, `ranking/`, `gap_analysis/`) และ `API.md` §65
- Internal endpoint ไม่ตรงกัน: `TECH_STACK.md` §13 ใช้ `POST /process/resume` และ field `text` ส่วน `API.md` §35-37 ใช้ `POST /internal/analyze` (หรือ `/process/analyze`) และ field `resume_text`
- ตำแหน่งไฟล์เริ่มต้นเป็น `app/main.py` ใน `FOLDER_STRUCTURE.md` และ `ENVIRONMENT_SETUP.md` แต่เป็น `main.py` ที่ Root ใน `API.md` §65

## การตัดสินใจ

1. **Framework:** FastAPI + Uvicorn + Pydantic โฟลเดอร์ `schemas/` เก็บ Pydantic model ของ Request/Response ตาม `API.md` §36-37 ทำให้ FastAPI ตรวจสอบ Contract ให้อัตโนมัติ
2. **โฟลเดอร์:** ตามโครงสร้างที่เจ้าของโครงการกำหนดใน `services/ai/app/` (`api`, `services`, `pipelines`, `extractors`, `normalizers`, `matching`, `models`, `schemas`) โมดูลใน `AI_MATCHING_SPEC.md` §85 จัดลงดังนี้

   | โมดูลใน AI_MATCHING_SPEC §85 | โฟลเดอร์ |
   | --- | --- |
   | resume_parser, portfolio_analyzer, skill_extractor, evidence_analyzer | `extractors/` |
   | skill_normalizer | `normalizers/` |
   | candidate_profile, occupation_profile, market_analyzer | `services/` (ชั่วคราว จนกว่าจะกำหนด Contract ของ Matching) |
   | matching_engine, ranking_engine, explanation_engine, skill_gap_engine, guidance_engine | `matching/` |
   | ลำดับขั้นตอนของหนึ่ง Analysis Request | `pipelines/` |

3. **Endpoint (ชุดเริ่มต้น):** `POST /internal/analyze` ตาม `API.md` §35-37 และ `GET /health` ใช้ตั้งแต่ Phase 0 ถึง Phase 6 ตัวอย่างใน `TECH_STACK.md` §13 แก้ให้ตรงกัน Contract ที่ Express ใช้เรียก Matching, Skill Gap และ Guidance ใน Python ยังไม่ได้กำหนด ต้องตัดสินก่อน Phase 7 (ดูรายการ C-01 ใน `docs/decisions/README.md`)
4. **ไฟล์เริ่มต้น:** `services/ai/app/main.py` รันด้วย `python -m app.main` ตาม `ENVIRONMENT_SETUP.md` §33
5. **ความปลอดภัย:** ปิดหน้า `/docs` และ `/openapi.json` นอก Development และไม่เปิด Port ของ Service นี้สู่ภายนอก (`API.md` §35)

## ผลที่ตามมา

- เอกสารที่แก้: `FOLDER_STRUCTURE.md` §14-15, `TECH_STACK.md` §12, §13, §42, `API.md` §35, §65, `ENVIRONMENT_SETUP.md` §33
- `services/ai/requirements.txt` ยังว่าง เพิ่ม `fastapi`, `uvicorn`, `pydantic` พร้อมเวอร์ชันที่ตรึงไว้ตอนเริ่ม Phase 0
