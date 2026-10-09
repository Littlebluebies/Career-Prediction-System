# 0012: การตัดสินใจของ Phase 3 (Labour Market Dataset)

- สถานะ: Accepted
- วันที่: 2026-10-07
- ผู้ตัดสิน: เจ้าของโครงการ (เลือกตามข้อเสนอก่อนเริ่ม Phase 3 ทั้ง 8 ข้อ) ค่าตัวเลขในข้อ 3 เป็นค่าเริ่มต้นที่ปรับได้หลังปรึกษาอาจารย์ที่ปรึกษา

## บริบท

- `IMPLEMENTATION_PLAN.md` §12-17 และ `DATASET_SPEC.md` §10-26 กำหนด Pipeline, Field ที่ต้องเก็บ และสูตร Demand ไว้แล้ว ตาราง `job_posting` / `job_posting_skill` (Migration 016-017) มีคอลัมน์ครบ ไม่ต้องแก้ Schema
- เอกสารไม่ได้กำหนด: แหล่งข้อมูลและวิธีเก็บ, Sampling Scope (`DATASET_SPEC.md` §14 ให้ผู้วิจัยกำหนด, C-15), Raw Job Posting เข้า Git หรือไม่ (C-14), วิธีเพิ่ม Skill ที่ ESCO ไม่มี (ADR 0010 §10), เกณฑ์เพิ่ม Occupation ใหม่ (ADR 0010 §9), วิธีสกัด Skill ใน Phase 3 และความหมายของ Release ที่ครอบคลุมหลาย Dataset (C-08)
- ข้อกำหนดการใช้งานของเว็บหางาน เช่น JobThai (Terms of Service ข้อ 3.2) ห้ามทำซ้ำหรือเผยแพร่เนื้อหาโดยไม่ได้รับอนุญาตเป็นลายลักษณ์อักษร และ Repository เป็น Public

## การตัดสินใจ

1. **แหล่งข้อมูลและวิธีเก็บ:** ผู้วิจัยเก็บ Job Posting แบบ Manual จากเว็บหางาน 2 แหล่ง (ค่าเริ่มต้น: JobsDB และ JobThai) กรอกลง CSV ตาม `scripts/dataset/jobs/job_posting_template.csv` และคู่มือ `scripts/dataset/jobs/COLLECTION_GUIDE.md` ไม่ใช้ Bot / Scraper ไม่เผยแพร่ข้อความต้นฉบับ ควรแจ้งวิธีการนี้กับอาจารย์ที่ปรึกษา
2. **Raw Job Posting ไม่เข้า Git (C-14 ส่วน Job Posting):** Raw อยู่ที่ `datasets/raw/job_posting/<version>/` (อยู่ใน `.gitignore`) ผู้วิจัยสำรองเองในที่เก็บส่วนตัว Metadata บันทึกจำนวนแถวและ SHA-256 ของไฟล์ Raw ส่วน Processed ที่ Commit มีเฉพาะ Field ที่จำเป็นและไม่มีข้อความยาว (ชื่อตำแหน่ง, บริษัท, พื้นที่, ประสบการณ์, แหล่ง, URL, วันที่, Occupation, Skill ที่สกัดได้) `description` และ `requirements` ใน Reference Seed เป็น `NULL` และตัดข้อมูลส่วนบุคคล (ชื่อผู้ติดต่อ, อีเมล, เบอร์โทร, LINE ID) ตั้งแต่ขั้นเก็บ
3. **Sampling Scope (C-15 / `DATASET_SPEC.md` §14):** ค่าเริ่มต้น
    | เรื่อง | ค่า | เหตุผล |
    | --- | --- | --- |
    | Target Market | ประเทศไทย | `DATASET_SPEC.md` §37 |
    | Occupation Scope | 5 อาชีพจาก ESCO (ADR 0010 §8) + Back-end / Full-stack Developer (ข้อ 5) | `DATASET_SPEC.md` §38 |
    | แหล่ง | 2 เว็บ | ลด Bias จากแหล่งเดียว (§36) |
    | ช่วงเวลา | Posting ที่ยังเปิดรับในช่วงเก็บ 2-4 สัปดาห์ บันทึกวันเริ่มและวันสิ้นสุดใน Metadata (`sampling_period`) | ข้อมูลอยู่ในช่วงเวลาเดียวกัน |
    | จำนวน | อย่างน้อย 30 Posting ต่ออาชีพ รวมประมาณ 150-250 | สัดส่วน Demand ไม่แกว่งมากจาก Posting จำนวนน้อย |
4. **Skill ที่ ESCO ไม่มี:** เพิ่มเป็น Canonical Skill ใหม่ผ่านไฟล์ Curated `scripts/dataset/jobs/new_skills.csv` ทุกแถวต้องมีหมวดหมู่ เหตุผล และ Source = Job Posting Dataset เพิ่มได้เมื่อพบในอย่างน้อย **3** Posting (พารามิเตอร์วิจัย ปรับได้) ถ้าชื่อใหม่ชนกับ Alias ของ ESCO (เช่น `HTML` เป็น Alias ของ "use markup languages") ให้ตัด Alias นั้นออกและบันทึกใน `dropped_aliases.csv`
5. **Occupation Mapping และ Occupation ใหม่:** Map ชื่อตำแหน่งด้วย `occupation_alias` และคำค้นในชื่อตำแหน่ง แถวที่ Map ไม่ได้หรือกำกวมต้องผ่านการตรวจของผู้วิจัยในไฟล์ Review (บันทึกการตัดสินและเหตุผล) เพิ่ม **Back-end Developer** และ **Full-stack Developer** ใน CF10 โดย `source` = Job Posting Dataset เมื่อพบอย่างน้อย **10** Posting (พารามิเตอร์วิจัย ปรับได้) Posting นอก Scope ถูกตัดออกตาม `DATASET_SPEC.md` §13 พร้อมเหตุผล
6. **การสกัด Skill ใน Phase 3:** Dictionary / Alias (Method A ใน `AI_MATCHING_SPEC.md` §16) เขียนด้วย Python Standard Library ใน `scripts/dataset/` ผู้วิจัยสุ่มตรวจผลการสกัด (อย่างน้อย 20 Posting) และบันทึก Precision ใน Metadata `job_posting_skill.confidence` เป็น `NULL` NLP และ Semantic Matching ทำใน Phase 6
7. **Demand และ Importance:** คำนวณ `occupation_skill.demand` ตามสูตร `DATASET_SPEC.md` §24 ทุกคู่ Occupation-Skill ที่มีข้อมูล คู่ที่พบใน Posting แต่ ESCO ไม่ได้โยงไว้ สร้างแถวใหม่โดย `source` ระบุ Job Posting Dataset และ Version `importance` ยังเป็น `NULL` จนกว่า `AI_MATCHING_SPEC.md` จะกำหนดวิธี (Phase 7) ไม่ตั้ง Threshold ตัดทิ้งใน Phase นี้
8. **Version และ Release (C-08):** Job Posting Dataset ใช้ Version `2026.02` และเพิ่มแถว `dataset_version` ที่ `dataset_name = 'release'`, `version_name = '2026.02'` โดย `description` ระบุ Dataset และ Version ที่ประกอบเป็น Release นี้ `career_result.dataset_version_id` ชี้ไปที่แถว Release ไม่แก้ Schema

## เหตุผล

- การเก็บแบบ Manual และไม่เผยแพร่ Raw เคารพข้อกำหนดของแหล่งข้อมูลและความเป็นส่วนตัว และอธิบายได้ใน Chapter 3 (`DATASET_SPEC.md` §53)
- Raw ไม่อยู่ใน Git แต่มี Checksum เหมือน ESCO (ADR 0010 §5) CI ยังตรวจ Processed -> Seed ได้ (ADR 0011)
- Skill เฉพาะเทคโนโลยีจำเป็นต่อ Skill Gap ที่มีประโยชน์ การใช้เฉพาะ Skill กว้างของ ESCO จะหยาบเกินไป
- Dictionary / Alias อธิบายได้และทำซ้ำได้ ไม่ต้องเลือก Model ก่อนเวลา (`AI_MATCHING_SPEC.md` ยังเป็น TO BE FINALIZED)
- Release ใน `dataset_version` ทำให้ผลลัพธ์ย้อนกลับไปถึงทุก Dataset ได้ (`CLAUDE.md` §17) โดยไม่เพิ่ม Schema

## ผลที่ตามมา

- `.gitignore` เพิ่ม `datasets/raw/job_posting/`
- ไฟล์ใหม่: `scripts/dataset/jobs/job_posting_template.csv`, `scripts/dataset/jobs/COLLECTION_GUIDE.md` (ขั้นนี้) และ Pipeline ของ Phase 3 (ขั้นถัดไป)
- `docs/decisions/README.md`: ปิด C-08, ปิด C-14 ส่วน Job Posting, ปิด C-15 ส่วนแหล่งข้อมูลของ Phase 3
- CI (ADR 0011 ข้อ 10): ขยาย `validate.py` และ Job `dataset` ให้ครอบคลุม Job Posting และเพิ่มเทสต์ Reference Seed ใน PR ของ Phase 3

## ส่วนเพิ่มเติม (2026-10-09): หน่วยนับของ Job Posting

- ผู้ตัดสิน: เจ้าของโครงการ (เลือกแบบ A หลังตรวจข้อมูล 30 แถวแรก)

9. **หน่วยนับ = 1 ประกาศ x 1 อาชีพ:** ประกาศที่รับหลายอาชีพและแยกคุณสมบัติตามอาชีพ ให้แยกเป็น 1 แถวต่ออาชีพ ส่วนประกาศที่รับอาชีพเดียวกันหลายระดับ (เช่น Junior / Senior) ให้รวมเป็นแถวเดียว โดย `requirements` รวมส่วนที่ใช้ร่วมกันและส่วนของทุกระดับพร้อมหัวข้อระดับ เหตุผล: ไม่ให้บริษัทเดียวถูกนับซ้ำใน Demand ของอาชีพเดียวกัน (`DATASET_SPEC.md` §18) แถวที่ถูกรวมไม่ถูกลบ แต่ระบุ `notes` เป็น `exclude: merged into <posting_ref>` เพื่อให้รหัสเดิมยังตรวจย้อนกลับได้

