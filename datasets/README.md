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
- `raw/` จะถูก Commit เข้า Git หรือไม่ ยังไม่ตัดสิน ตัดสินเมื่อเริ่ม Phase 3 (ADR 0005, C-14)
