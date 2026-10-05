# scripts/dataset/

Pipeline สร้าง Reference Dataset (Phase 2) จาก ESCO แล้วนำเข้า Database
การตัดสินใจทั้งหมด: `docs/decisions/0010-phase-2-reference-data-decisions.md`
ใช้ Python 3.13 Standard Library เท่านั้น ไม่ต้องติดตั้ง Package (ADR 0010 §6)

```text
datasets/raw/esco/v1.2.1/*.csv          (ดาวน์โหลดเอง ไม่อยู่ใน Git)
        │  build_esco_reference.py
        ▼
datasets/processed/**.csv + datasets/metadata/*.json   (Commit)
        │  validate.py   (import.py เรียกให้อัตโนมัติ)
        │  import.py
        ▼
database/seed/reference/NN_<table>.seed.sql            (Generated, Commit)
        │  scripts/database/seed.sh reference
        ▼
PostgreSQL (career_system)
```

## ไฟล์

| ไฟล์ | หน้าที่ |
| --- | --- |
| `common.py` | ค่าที่ใช้ร่วมกัน: เวอร์ชัน ESCO / Dataset, Path, หมวดหมู่ที่อนุญาต, Career Family 15 กลุ่ม (`DATABASE.md` §19), ชื่อสาขาทางการ (ADR 0010 §18) |
| `build_esco_reference.py` | Raw ESCO -> ค้นหา Candidate -> ใช้ผลคัดเลือกของผู้วิจัย -> Occupation, Skill, Alias, Relation, หมวดหมู่ -> Processed CSV + Metadata |
| `validate.py` | Data Quality Checks (`DATASET_SPEC.md` §32-35) พิมพ์ `PASS` / `FAIL` ทีละข้อ ล้มเหลว = exit code 1 |
| `import.py` | รัน `validate.py` ก่อน ถ้าผ่านจึงสร้าง Reference Seed SQL |
| `esco/occupation_selection.csv` | ผลการตรวจ Candidate Occupation ของผู้วิจัย (include / exclude + Career Family + เหตุผล) |
| `esco/category_overrides.csv` | ข้อยกเว้นของกฎหมวดหมู่ Skill พร้อมเหตุผล (ADR 0010 §13) |

## วิธีใช้ (รันจาก Root ของ Repository)

```bash
# 0. ดาวน์โหลด ESCO v1.2.1 (Classification, English, CSV) ไปไว้ที่ datasets/raw/esco/v1.2.1/
# 1. สร้าง Processed Dataset + Metadata
py -3.13 scripts/dataset/build_esco_reference.py
# 2. ตรวจคุณภาพ (ไม่บังคับ import.py ตรวจให้อีกรอบ)
py -3.13 scripts/dataset/validate.py
# 3. สร้าง Reference Seed SQL
py -3.13 scripts/dataset/import.py
# 4. โหลดเข้า Database ใหม่ (ลบข้อมูล Development เดิม)
bash scripts/database/reset.sh reference
```

## กติกา

- ห้ามแก้ไฟล์ใน `datasets/processed/`, `datasets/metadata/` และ `database/seed/reference/` ด้วยมือ ให้แก้ Config หรือ Script แล้วรันใหม่
- ผลลัพธ์เป็น Deterministic: รันซ้ำด้วย Raw เดิมต้องได้ไฟล์เดิมทุกไบต์ (`git status` ต้องไม่มีการเปลี่ยนแปลง)
- ถ้า `build_esco_reference.py` เจอ Candidate ใหม่ที่ยังไม่มีใน `occupation_selection.csv` จะหยุดและให้ผู้วิจัยตรวจก่อน
- SHA-256 ของไฟล์ Raw อยู่ใน Metadata (`source_files`) ใช้ยืนยันว่าดาวน์โหลดเวอร์ชันเดียวกัน
- เปลี่ยนเวอร์ชัน Dataset: แก้ `DATASET_VERSION` ใน `common.py` (รูปแบบ `YYYY.NN`, ADR 0010 §4)
