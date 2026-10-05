# datasets/

Dataset ของระบบ Source of Truth: `docs/03-ai-data/DATASET_SPEC.md`

| โฟลเดอร์ | หน้าที่ | อ้างอิง |
| --- | --- | --- |
| `raw/` | ข้อมูลต้นฉบับ **ห้ามแก้โดยตรง** | FOLDER_STRUCTURE §20 |
| `processed/` | ข้อมูลหลัง Cleaning, Deduplication, Normalization, Skill Extraction, Occupation Mapping | FOLDER_STRUCTURE §21 |
| `evaluation/` | Annotation, Ground Truth สำหรับ Evaluation (ต้องมีที่มาชัดเจน) | FOLDER_STRUCTURE §22, DATASET_SPEC §54 |
| `metadata/` | 1 ไฟล์ JSON ต่อ 1 Dataset Version ชื่อ `<dataset_name>_<version>.json` | ADR 0006 |

เมื่อเริ่มมีข้อมูล ให้แบ่งโฟลเดอร์ย่อยใน `raw/` และ `processed/` ตามชนิด เช่น
`occupation/`, `skill/`, `job_posting/`, `occupation_skill/` (DATASET_SPEC §54)

## Metadata (ADR 0006)

ฟิลด์บังคับ: `dataset_name`, `version`, `source`, `collection_date`, `coverage`,
`description`, `number_of_records`, `processing_method`

ฟิลด์เสริม: `sampling_period`, `processing_version`, `schema_version`, `notes`

## กติกา

- **ห้ามใส่ Resume, Portfolio หรือข้อมูลนักศึกษาจริงใน Dataset** (ADR 0005 ข้อ 4, `CLAUDE.md` §13)
- Labour Market Demand ต้องมาจาก Job Posting -> Skill Extraction -> Skill Normalization -> Demand Analysis
  ห้ามสร้างจากการคาดเดา (`CLAUDE.md` §6)
- ทุกผลลัพธ์ต้องย้อนไปถึง Dataset Version ได้ (`CLAUDE.md` §17)
- `raw/esco/` ไม่ Commit (ดาวน์โหลดซ้ำได้ เวอร์ชันและ SHA-256 อยู่ใน `metadata/`, ADR 0010 §5) ส่วน `raw/` ของ Job Posting ตัดสินใน Phase 3 (C-14)
- ไฟล์ใน `processed/` และ `metadata/` สร้างโดย `scripts/dataset/` ห้ามแก้ด้วยมือ (ดู `scripts/dataset/README.md`)

## Reference Dataset ปัจจุบัน (Phase 2, ESCO v1.2.1, version 2026.01)

| ไฟล์ | เนื้อหา |
| --- | --- |
| `processed/occupation/esco_candidates.csv` | Candidate จากการค้นคำ + ผลตรวจของผู้วิจัย |
| `processed/occupation/occupation.csv`, `occupation_alias.csv` | Occupation 5 อาชีพ (CF10 / CF11) และ Alias |
| `processed/skill/skill.csv`, `skill_alias.csv` | Skill พร้อมหมวดหมู่และกฎที่ใช้ (`category_rule`) และ Alias |
| `processed/skill/dropped_aliases.csv` | Alias ที่ถูกตัด (ชี้หลาย Skill หรือซ้ำชื่อหลัก) พร้อมเหตุผล |
| `processed/occupation_skill/occupation_skill.csv` | ความสัมพันธ์ essential / optional |
| `metadata/*_2026.01.json` | Metadata ตาม ADR 0006 |
