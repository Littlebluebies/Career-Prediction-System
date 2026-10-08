# คู่มือเก็บ Job Posting (Phase 3, Dataset 2026.02)

การตัดสินใจ: `docs/decisions/0012-phase-3-labour-market-decisions.md`
ข้อกำหนด: `DATASET_SPEC.md` §10-18, §36-37, §52-53

> ไฟล์ที่เก็บจริงเป็น **Raw Data** ห้าม Commit เข้า Git (อยู่ใน `.gitignore` แล้ว) และให้สำรองไว้ในที่เก็บส่วนตัว เช่น Google Drive

## 1. ไฟล์และที่เก็บ

1. Copy `scripts/dataset/jobs/job_posting_template.csv` ไปเป็น
   `datasets/raw/job_posting/2026.02/job_postings.csv`
2. แก้ไฟล์ด้วย **Google Sheets** (แนะนำ) แล้ว Download เป็น CSV
   หรือ Excel แล้ว Save As เป็น **"CSV UTF-8 (Comma delimited)"** เท่านั้น
   (CSV แบบธรรมดาของ Excel ทำให้ภาษาไทยเสีย)
3. 1 แถว = 1 Posting ข้อความหลายบรรทัดใส่ในช่องเดียวได้ ไม่ต้องรวมเป็นบรรทัดเดียว

## 2. ขอบเขตการเก็บ (ADR 0012 §3)

| เรื่อง | ค่า |
| --- | --- |
| แหล่ง | JobsDB และ JobThai |
| ประเทศ | ไทย (รวม Remote ที่บริษัทอยู่ในไทย) |
| ช่วงเวลา | 2-4 สัปดาห์ จดวันเริ่มและวันสุดท้ายที่เก็บ |
| เป้าหมาย | อย่างน้อย 30 Posting ต่ออาชีพ รวมประมาณ 150-250 |

คำค้น (ใช้ชื่อตำแหน่งกว้างๆ ไม่ใช้ชื่อเทคโนโลยี เพื่อไม่ให้ผลเอียงไปทางเทคโนโลยีใดเทคโนโลยีหนึ่ง):

| อาชีพ | คำค้น |
| --- | --- |
| Front-end / UI Developer | `frontend developer`, `front-end developer`, `ui developer` |
| Back-end Developer | `backend developer`, `back-end developer` |
| Full-stack Developer | `full stack developer`, `fullstack developer` |
| Web Developer | `web developer`, `web application developer`, `web programmer` |
| UI/UX / Web Designer | `ux ui designer`, `ui designer`, `ux designer`, `web designer` |

## 3. เกณฑ์คัดเข้า / คัดออก (DATASET_SPEC §12-13)

เก็บเมื่อ:

- ตรงกับอาชีพในตารางข้างบน
- มี Job Description หรือ Requirement ที่อ่านแล้วรู้ว่าต้องใช้ทักษะอะไร
- ยังเปิดรับสมัครในวันที่เก็บ

ไม่เก็บ:

- ไม่มีรายละเอียดงานหรือ Requirement (มีแต่ชื่อตำแหน่งและเงินเดือน)
- ตำแหน่งนอก Scope เช่น Graphic Designer, Data Engineer, IT Support
- ประกาศซ้ำที่เห็นชัดว่าเป็นตำแหน่งเดียวกันของบริษัทเดียวกัน (Script ตรวจซ้ำให้อีกรอบ)
- ประกาศที่ไม่รู้ว่าบริษัทไหน หรือหาแหล่งที่มาไม่ได้

ถ้าไม่แน่ใจ ให้เก็บไว้และเขียนเหตุผลในช่อง `notes` ขั้น Review จะตัดสินอีกครั้ง

## 4. ความหมายของแต่ละคอลัมน์

| คอลัมน์ | บังคับ | วิธีกรอก |
| --- | --- | --- |
| `posting_ref` | ✅ | รหัสที่ตั้งเอง เรียงต่อกัน `JP-0001`, `JP-0002`, ... ห้ามซ้ำ ห้ามเปลี่ยนภายหลัง |
| `source` | ✅ | `JobsDB` หรือ `JobThai` สะกดเหมือนกันทุกแถว |
| `source_url` | ✅ | URL ของประกาศ |
| `search_keyword` | ✅ | คำค้นที่ใช้แล้วเจอประกาศนี้ (จากตารางข้อ 2) |
| `date_collected` | ✅ | วันที่เก็บ รูปแบบ `YYYY-MM-DD` เช่น `2026-10-12` |
| `date_posted` | | วันที่ประกาศ ถ้าหน้าเว็บแสดง `YYYY-MM-DD` |
| `job_title` | ✅ | ชื่อตำแหน่ง **ตามที่เขียนในประกาศ** ไม่ต้องแก้ |
| `company` | ✅ | ชื่อบริษัทตามประกาศ |
| `location` | | จังหวัดหรือเขต เช่น `Bangkok`, `Chonburi`, `Remote` |
| `employment_type` | | `Full-time`, `Contract`, `Internship`, ... |
| `experience` | | ตามประกาศ เช่น `1-3 years`, `ไม่จำกัด` |
| `education` | | ตามประกาศ เช่น `ปริญญาตรี วิทยาการคอมพิวเตอร์` |
| `responsibilities` | | หน้าที่ความรับผิดชอบ Copy ทั้งส่วน |
| `requirements` | ✅* | คุณสมบัติผู้สมัคร Copy ทั้งส่วน |
| `description` | ✅* | ส่วนอื่นของประกาศที่บอกทักษะหรือเทคโนโลยี |
| `notes` | | หมายเหตุของผู้วิจัย เช่น เหตุผลที่ไม่แน่ใจ |

\* ต้องมีอย่างน้อยหนึ่งช่อง ระหว่าง `requirements` และ `description`

Copy ข้อความตามต้นฉบับ ไม่ต้องจัดรูปแบบ ไม่ต้องแปล ขั้น Cleaning ทำโดย Script

## 5. ข้อมูลส่วนบุคคล (ห้ามเก็บ)

ห้ามคัดลอก: ชื่อผู้ติดต่อ / HR, อีเมล, เบอร์โทร, LINE ID, ที่อยู่ละเอียด
ถ้าอยู่กลางข้อความ ให้แทนด้วย `[removed]` ตอนวาง

## 6. ตัวอย่าง 1 แถว (ข้อมูลสังเคราะห์ ไม่ใช่ประกาศจริง)

| คอลัมน์ | ค่า |
| --- | --- |
| `posting_ref` | `JP-0001` |
| `source` | `JobsDB` |
| `source_url` | `https://example.com/job/0000` |
| `search_keyword` | `frontend developer` |
| `date_collected` | `2026-10-12` |
| `job_title` | `Junior Front-end Developer` |
| `company` | `Example Co., Ltd.` |
| `location` | `Bangkok` |
| `experience` | `0-2 years` |
| `requirements` | `- Experience with HTML, CSS and JavaScript` (ขึ้นบรรทัดใหม่) `- Knowledge of React is a plus` |

## 7. ระหว่างเก็บ

- จดวันแรกและวันสุดท้ายที่เก็บ (ใช้เป็น `sampling_period` ใน Metadata)
- นับจำนวนต่ออาชีพเป็นระยะ ให้ได้อย่างน้อย 30 ต่ออาชีพ ถ้าอาชีพไหนหาไม่ได้ครบ ให้จดไว้ เป็นข้อมูลสำหรับรายงาน Bias (`DATASET_SPEC.md` §36)
- สำรองไฟล์ทุกครั้งหลังเก็บเพิ่ม
