# 0005: ความสะอาดของ Repository และการป้องกันข้อมูลส่วนบุคคล

- สถานะ: Accepted
- วันที่: 2026-09-20
- การยืนยัน: เจ้าของโครงการสั่งให้ดำเนินการต่อหลังตรวจว่าไม่ขัดกับชิ้นงาน (2026-09-20)
- ผู้ตัดสิน: เลือกตามคำสั่งให้แก้ความเสี่ยงโดยตรง เจ้าของโครงการเปลี่ยนได้

## บริบท

- `CLAUDE.md` §13-14 ห้าม Commit `.env`, Resume จริง, Portfolio ส่วนตัว, ข้อมูลนักศึกษาจริง และ Database Dump
- เอกสารต้นฉบับใช้ปลายบรรทัดแบบ CRLF และคำสั่งใน `ENVIRONMENT_SETUP.md` เป็นแบบ Windows ถ้า Shell Script หรือไฟล์ SQL ถูกแปลงเป็น CRLF Script จะรันใน Docker หรือ Git Bash ไม่ได้ และ Checksum ของ Migration (0003) จะไม่ตรงกัน
- `tests/fixtures/` เป็นที่ที่ไฟล์ Resume ตัวอย่างมักถูกวาง ซึ่งเป็นจุดเสี่ยงที่ข้อมูลจริงจะหลุดเข้า Git

## การตัดสินใจ

1. เพิ่ม `.gitattributes`: `* text=auto` และบังคับ LF สำหรับ `*.sh`, `*.sql`, `*.yml`, `*.yaml`, `Dockerfile*`, `.env.example` และตั้งไฟล์ PDF, DOC, DOCX, รูปภาพเป็น binary
2. `.gitignore` กัน `.env*` (ยกเว้น `.env.example`), `storage/`, `uploads/`, `temporary/`, `*.dump`, `*.backup`, `*.bak`, `*.sql.gz`
3. เพิ่ม `tests/fixtures/README.md` ระบุว่า Fixture ต้องเป็นข้อมูลสังเคราะห์ที่สร้างขึ้นเองเท่านั้น
4. `datasets/README.md` ระบุว่าห้ามใส่ Resume, Portfolio หรือข้อมูลนักศึกษาจริงใน Dataset
5. ข้อมูลที่ส่งไป Python Service มีเฉพาะที่จำเป็นต่อการวิเคราะห์ (`API.md` §36)

## เรื่องที่ยังเปิด

- `datasets/raw/` จะถูก Commit เข้า Git หรือไม่ Job Posting ดิบอาจมีขนาดใหญ่และมีเงื่อนไขลิขสิทธิ์ของแหล่งข้อมูล ตัดสินใจเมื่อเริ่ม Phase 3 และตรวจเงื่อนไขของแหล่งข้อมูลก่อน
- การใช้ Resume ของผู้ใช้จริงเป็น Evaluation Dataset ต้องมีความยินยอมและขั้นตอนความเป็นส่วนตัวก่อน (`ENVIRONMENT_SETUP.md` §56)
