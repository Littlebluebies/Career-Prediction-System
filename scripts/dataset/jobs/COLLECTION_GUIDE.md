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

### ผลค้นหาที่เป็นอาชีพอื่นใน Scope

ค้นคำหนึ่งแล้วเจอตำแหน่งของอาชีพอื่นที่อยู่ในตารางข้างบน (เช่น ค้น `frontend developer` แล้วเจอ Full-stack หรือ Web Developer) **ให้เก็บด้วย**

- ช่อง `search_keyword` ใส่คำที่ใช้ค้นจริง ไม่ต้องเปลี่ยนตามชื่อตำแหน่ง
- อาชีพของ Posting ตัดสินจาก `job_title` และเนื้อหาในขั้น Occupation Mapping ไม่ใช่จากคำค้น
- นับเป้าหมาย 30 ต่ออาชีพจากชื่อตำแหน่ง ไม่ใช่จากคำค้น
- ไล่ผลค้นหา **ตามลำดับที่เว็บแสดง** แล้วเก็บทุกประกาศที่เข้าเกณฑ์ ไม่เลือกเฉพาะตัวที่น่าสนใจ (ลด Selection Bias)
- ถ้าเจอประกาศที่เก็บไปแล้วจากคำค้นอื่น ข้ามไป

## 3. เกณฑ์คัดเข้า / คัดออก (DATASET_SPEC §12-13)

เก็บเมื่อ:

- ตรงกับอาชีพในตารางข้างบน
- มี Job Description หรือ Requirement ที่อ่านแล้วรู้ว่าต้องใช้ทักษะอะไร
- ยังเปิดรับสมัครในวันที่เก็บ

ไม่เก็บ:

- ไม่มีรายละเอียดงานหรือ Requirement (มีแต่ชื่อตำแหน่งและเงินเดือน)
- ตำแหน่งนอก Scope เช่น Graphic Designer, Data Engineer, IT Support
- ประกาศซ้ำที่เห็นชัดว่าเป็นตำแหน่งเดียวกันของบริษัทเดียวกัน (Script ตรวจซ้ำให้อีกรอบ)
- ประกาศที่หาแหล่งที่มาไม่ได้ (ไม่มี URL ที่เปิดดูได้)

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
| `company` | ✅ | ชื่อบริษัทตามประกาศ ถ้าประกาศซ่อนชื่อ (เช่น "บริษัทชั้นนำ") ใส่ `Confidential` |
| `location` | | จังหวัดหรือเขต เช่น `Bangkok`, `Chonburi`, `Remote` |
| `employment_type` | | `Full-time`, `Contract`, `Internship`, ... |
| `experience` | | ตามประกาศ เช่น `1-3 years`, `ไม่จำกัด` |
| `education` | | ตามประกาศ เช่น `ปริญญาตรี วิทยาการคอมพิวเตอร์` |
| `responsibilities` | | หน้าที่ความรับผิดชอบ Copy ทั้งส่วน |
| `requirements` | ✅* | คุณสมบัติผู้สมัคร Copy ทั้งส่วน |
| `description` | ✅* | ส่วนอื่นของประกาศที่บอกทักษะหรือเทคโนโลยี |
| `notes` | | หมายเหตุของผู้วิจัย เช่น เหตุผลที่ไม่แน่ใจ |

\* ต้องมีอย่างน้อยหนึ่งช่อง ระหว่าง `requirements` และ `description` ถ้าไม่มีทั้งสองอย่าง ไม่ต้องเก็บประกาศนั้น

ช่องที่ไม่มี ✅ ถ้าประกาศไม่บอก ให้เว้นว่าง ไม่ต้องใส่ `-` หรือ `ไม่ระบุ`

Copy ข้อความตามต้นฉบับ ไม่ต้องจัดรูปแบบ ไม่ต้องแปล ขั้น Cleaning ทำโดย Script

### ส่วนไหนของประกาศใส่ช่องไหน

| ส่วนในประกาศ | ช่อง |
| --- | --- |
| หน้าที่ความรับผิดชอบ (Responsibilities, งานที่ต้องทำ) | `responsibilities` |
| คุณสมบัติที่ต้องมี และ Bonus / Nice to have / Preferred (**Copy หัวข้อมาด้วย** เช่น `Bonus Points (Optional):`) | `requirements` |
| ส่วนอื่นที่พูดถึงทักษะหรือเครื่องมือ เช่น Tech Stack ของทีม | `description` |
| สวัสดิการ, เงินเดือน, ข้อมูลบริษัททั่วไป | ไม่เก็บ |

หัวข้อที่ซ้ำกับชื่อช่อง (เช่น `Required Skills :-`) ไม่ต้อง Copy ถ้าประกาศไม่แบ่งหัวข้อเลย ใส่ทั้งหมดใน `description`
หัวข้อ Bonus / Nice to have ต้องอยู่ในข้อความเสมอ ใช้แยกระดับ Requirement ในอนาคต (`DATASET_SPEC.md` §20)

### ประกาศเดียวรับหลายตำแหน่ง

ถ้าประกาศเดียวแยกคุณสมบัติตามตำแหน่ง (เช่น "For Frontend Developer: ..." และ "For Fullstack Developer: ...") ให้**แยกเป็นหลายแถว แถวละ 1 ตำแหน่ง** เพราะ 1 Posting ใน Dataset ผูกกับ 1 Occupation

- `posting_ref` คนละรหัส, `source_url` / `company` / `date_collected` เหมือนกันทุกแถว
- `job_title` ใช้ชื่อตำแหน่งตามหัวข้อย่อยในประกาศ (เช่น `Frontend Developer`)
- `requirements` ของแต่ละแถว = ส่วนที่ใช้ร่วมกันทุกตำแหน่ง + ส่วนของตำแหน่งนั้นเท่านั้น + ส่วน Bonus / Nice to have (ถ้าใช้ร่วมกัน)
- `notes` เขียน `split from multi-role posting; original title: <ชื่อหัวประกาศ>`

ถ้าประกาศรับหลายตำแหน่งแต่ใช้คุณสมบัติชุดเดียวกัน ไม่ต้องแยก เก็บเป็นแถวเดียว และเขียนใน `notes` ว่า `multi-role posting, shared requirements`

### ประกาศเดียวรับอาชีพเดียวกันหลายระดับ (ADR 0012 ข้อ 9)

ถ้าประกาศรับตำแหน่งเดียวกันหลายระดับ (เช่น Junior / Intermediate / Senior Full-stack) **ไม่ต้องแยกแถว** ให้รวมเป็นแถวเดียว

- `job_title` = ชื่อหัวประกาศ
- `requirements` = ส่วนที่ใช้ร่วมกัน + ส่วนของทุกระดับ โดย Copy หัวข้อระดับมาด้วย (เช่น `Junior:`, `Senior:`)
- `notes` = `multi-level posting merged: Junior, Senior`

ถ้าเคยแยกไว้แล้ว ให้รวมเนื้อหาเข้าแถวแรก แล้ว**ไม่ต้องลบแถวที่เหลือ** แต่เขียน `notes` ของแถวนั้นว่า `exclude: merged into JP-xxxx`

### การคัดออกภายหลัง

ถ้าต้องตัดแถวใดออก (เก็บผิด Scope, ถูกรวม, ซ้ำ) **ห้ามลบแถวและห้ามเปลี่ยน `posting_ref`** ให้เขียน `notes` ขึ้นต้นด้วย `exclude:` ตามด้วยเหตุผล เช่น `exclude: out of scope (mobile only)` Script จะนับและรายงานเหตุผลการคัดออก

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
