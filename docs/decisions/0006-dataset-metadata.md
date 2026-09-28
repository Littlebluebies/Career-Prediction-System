# 0006: ที่เก็บและรูปแบบ Dataset Metadata

- สถานะ: Accepted
- วันที่: 2026-09-20
- การยืนยัน: เจ้าของโครงการสั่งให้ดำเนินการต่อหลังตรวจว่าไม่ขัดกับชิ้นงาน (2026-09-20)
- ผู้ตัดสิน: เลือกตามคำสั่งให้แก้ความเสี่ยงโดยตรง เจ้าของโครงการเปลี่ยนได้ก่อนเริ่ม Phase 3

## บริบท

- `DATASET_SPEC.md` §32 ต้องการให้ทุก Dataset บันทึก Metadata และ `FOLDER_STRUCTURE.md` §23 กำหนดโฟลเดอร์ `datasets/metadata/` แต่แผนผังที่เจ้าของโครงการกำหนดไม่มีโฟลเดอร์นี้
- รายการฟิลด์ใน `DATASET_SPEC.md` §32 กับ `FOLDER_STRUCTURE.md` §23 ไม่เหมือนกัน
- ตาราง `dataset_version` (`DATABASE.md` §25) มีคอลัมน์ไม่ครบทุกฟิลด์ของ §32
- ผลลัพธ์ทุกรายการต้องย้อนไปถึง Dataset Version ได้ (`CLAUDE.md` §17)

## การตัดสินใจ

1. เพิ่มโฟลเดอร์ `datasets/metadata/`
2. บันทึก 1 ไฟล์ JSON ต่อ 1 Dataset Version ชื่อ `<dataset_name>_<version>.json`
3. ฟิลด์บังคับตาม `DATASET_SPEC.md` §32: `dataset_name`, `version`, `source`, `collection_date`, `coverage`, `description`, `number_of_records`, `processing_method`
4. ฟิลด์เสริมจาก `FOLDER_STRUCTURE.md` §23: `sampling_period`, `processing_version`, `schema_version`, `notes`
5. ไฟล์ Metadata เป็นบันทึกฉบับเต็ม ตาราง `dataset_version` เก็บเฉพาะบางฟิลด์ Script นำเข้าจะแปลงดังนี้ ไม่เพิ่มคอลัมน์ใหม่เพราะยังไม่มี Requirement (`CLAUDE.md` §7)

   | ไฟล์ Metadata | คอลัมน์ `dataset_version` |
   | --- | --- |
   | `dataset_name` | `dataset_name` |
   | `version` | `version_name` |
   | `source` | `source_description` |
   | `collection_date` | `collected_at` |
   | `number_of_records` | `record_count` |
   | `description` | `description` |
   | `coverage`, `processing_method` | ไม่มีคอลัมน์ อยู่ในไฟล์ Metadata เท่านั้น |

6. ค่า `DATASET_VERSION` ใน `.env` ต้องตรงกับ `version` ของไฟล์ Metadata ที่มีอยู่จริง ยกเว้นค่า placeholder `development` ที่ใช้กับ Seed ก่อนมี Dataset จริง (`ENVIRONMENT_SETUP.md` §15)
7. Script ตรวจ Metadata อยู่ใน `scripts/dataset/` สร้างใน Phase 3

## ผลที่ตามมา

- เอกสารที่แก้: `FOLDER_STRUCTURE.md` §19, §23, `DATASET_SPEC.md` §54
- ถ้าภายหลังต้องเก็บ `coverage` หรือ `processing_method` ในฐานข้อมูล ให้ทำ Migration ใหม่ตามขั้นตอนใน `CLAUDE.md` §7
