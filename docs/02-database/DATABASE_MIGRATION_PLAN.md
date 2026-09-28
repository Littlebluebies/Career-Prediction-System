# DATABASE_MIGRATION_PLAN.md

# Database Migration Plan

## Career Prediction and Skill Gap Analysis System

---

## 1. Purpose

เอกสารนี้กำหนดแผนการสร้างและจัดการ **PostgreSQL Database Migration** สำหรับระบบ

> “ระบบทำนายอาชีพสำหรับนักศึกษาคณะเทคโนโลยีสื่อสารมวลชนโดยอิงการวิเคราะห์ทักษะและความต้องการของตลาดแรงงาน”

โดยมีหน้าที่เปลี่ยนโครงสร้างฐานข้อมูลที่กำหนดไว้ใน `DATABASE.md` ให้กลายเป็น Migration ที่สามารถนำไปสร้างฐานข้อมูลจริงได้อย่างเป็นลำดับและตรวจสอบย้อนกลับได้

เอกสารนี้เป็นเอกสารด้าน **Database Implementation** ไม่ใช่เอกสารกำหนดโครงสร้างข้อมูลใหม่

---

# 2. Source of Truth

การพัฒนาฐานข้อมูลต้องอ้างอิงเอกสารตามลำดับดังนี้

```text
PROJECT_SPEC.md
        ↓
TECH_STACK.md
        ↓
DATABASE.md
        ↓
DATABASE_MIGRATION_PLAN.md
        ↓
Actual Migration Files
```

### กฎสำคัญ

`DATABASE.md` เป็น **Source of Truth ของ Database Schema**

`DATABASE_MIGRATION_PLAN.md` เป็น **Source of Truth ของลำดับและแนวทาง Migration**

หากต้องการเปลี่ยนโครงสร้าง Database:

```text
Requirement Change
        ↓
Update DATABASE.md
        ↓
Update Related Specs
        ↓
Create New Migration
        ↓
Test Migration
```

ห้ามเปลี่ยน Database โดยตรงโดยไม่มี Migration

---

# 3. Technology

Database หลักของระบบ:

```text
PostgreSQL
```

Backend:

```text
Node.js
Express.js
TypeScript
```

AI/NLP:

```text
Python
```

Infrastructure:

```text
Docker
Docker Compose
```

Database ต้องใช้ PostgreSQL syntax เท่านั้น

ห้ามใช้ syntax ที่ออกแบบเฉพาะสำหรับ:

```text
MySQL
MariaDB
MongoDB
```

---

# 4. Migration Philosophy

Migration ต้องมีคุณสมบัติดังนี้

* Ordered
* Reproducible
* Traceable
* Reviewable
* Testable
* Version Controlled
* Environment Independent
* Safe for incremental schema changes

เป้าหมายคือสามารถสร้าง Database ใหม่จากศูนย์ได้ด้วยขั้นตอนเดียวกันทุก Environment

ตัวอย่าง:

```text
Empty PostgreSQL Database
        ↓
Run Migration 001
        ↓
Run Migration 002
        ↓
Run Migration 003
        ↓
...
        ↓
Latest Migration
        ↓
Complete Database
```

---

# 5. Migration Directory

โครงสร้าง Database:

```text
database/
├── migrations/
│   ├── 001_create_schema.sql
│   ├── 002_create_major.sql
│   ├── 003_create_user_session.sql
│   ├── 004_create_career_family.sql
│   ├── 005_create_skill.sql
│   ├── 006_create_skill_alias.sql
│   ├── 007_create_occupation.sql
│   ├── 008_create_occupation_alias.sql
│   ├── 009_create_occupation_skill.sql
│   ├── 010_create_dataset_version.sql
│   ├── 011_create_resume.sql
│   ├── 012_create_portfolio.sql
│   ├── 013_create_portfolio_project.sql
│   ├── 014_create_user_skill.sql
│   ├── 015_create_skill_evidence.sql
│   ├── 016_create_job_posting.sql
│   ├── 017_create_job_posting_skill.sql
│   ├── 018_create_career_result.sql
│   ├── 019_create_skill_gap.sql
│   ├── 020_create_user_feedback.sql
│   └── 021_create_indexes.sql
│
├── seed/
│   ├── development/
│   ├── reference/
│   └── README.md
│
├── schema/
│   └── README.md
│
└── README.md
```

โครงสร้างนี้ใช้กับ SQL Migration Files ตาม `docs/decisions/0003-database-tooling.md` หลักการแยก Migration, Seed และ Schema Documentation ต้องคงไว้

---

# 6. Migration Naming Convention

ใช้รูปแบบ:

```text
NNN_action_target.sql
```

ตัวอย่าง:

```text
001_create_schema.sql
002_create_major.sql
003_create_user_session.sql
```

เมื่อ Database มีการเปลี่ยนแปลงในอนาคต (ตัวอย่างรูปแบบชื่อเท่านั้น ไม่ใช่รายการที่วางแผนไว้):

```text
022_add_<column>_to_<table>.sql
023_create_<table>.sql
024_add_<name>_index.sql
```

ห้ามย้อนกลับไปแก้ Migration ที่ถูก Apply ไปแล้วใน Environment ที่ใช้งานจริง

---

# 7. Migration Immutability

Migration ที่ถูกใช้งานแล้วถือเป็น **Immutable**

ตัวอย่าง:

```text
001_create_schema.sql
```

หากถูก Apply ไปแล้ว:

```text
ห้ามแก้ไฟล์เดิม
```

หากต้องการเปลี่ยน Schema:

```text
Existing Migration
        ↓
Create New Migration
```

เช่น:

```text
022_add_new_column.sql
```

แทนการแก้:

```text
005_create_skill.sql
```

---

# 8. Migration Metadata

หากไม่ได้ใช้ Migration Framework ที่มีระบบจัดการ Version ให้อัตโนมัติ ระบบควรมีตารางสำหรับบันทึก Migration ที่ถูก Apply แล้ว

ตัวอย่างแนวคิด:

```sql
CREATE TABLE schema_migrations (
    version TEXT PRIMARY KEY,
    applied_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

ตัวอย่างข้อมูล:

```text
001_create_schema.sql
002_create_major.sql
003_create_user_session.sql
...
```

หากใช้ Migration Tool ในภายหลัง และ Tool มีระบบ Migration Metadata อยู่แล้ว ไม่จำเป็นต้องสร้างระบบซ้ำ

---

# 9. Migration Execution Order

ลำดับ Migration ต้องคำนึงถึง Foreign Key Dependency

Dependency หลัก:

```text
major
  ↓
user_session

career_family
  ↓
occupation
  ↓
occupation_alias
  ↓
occupation_skill

skill
  ↓
skill_alias
  ↓
user_skill
  ↓
skill_evidence

dataset_version
  ↓
job_posting
  ↓
job_posting_skill

user_session
  ↓
resume
portfolio
  ↓
portfolio_project

occupation
  ↓
career_result
  ↓
skill_gap

user_session
  ↓
user_feedback
```

---

# 10. Migration 001 — Create Schema

ไฟล์:

```text
001_create_schema.sql
```

หน้าที่:

สร้าง PostgreSQL schema สำหรับระบบ

```sql
CREATE SCHEMA IF NOT EXISTS career_system;
```

และกำหนด:

```sql
SET search_path TO career_system, public;
```

Database Object หลักของระบบจะอยู่ภายใต้:

```text
career_system
```

---

# 11. Migration 002 — Major

ไฟล์:

```text
002_create_major.sql
```

สร้างตาราง:

```text
major
```

ใช้สำหรับเก็บข้อมูลสาขา/หลักสูตรที่เกี่ยวข้องกับระบบ

Fields หลัก:

```text
major_id
branch_name
major_name
is_active
created_at
```

มี Unique Constraint:

```text
(branch_name, major_name)
```

---

# 12. Faculty Major Scope

ระบบต้องรองรับ 4 กลุ่มหลักของคณะ

```text
1. เทคโนโลยีการผลิตภาพยนตร์และวิทยุโทรทัศน์

2. เทคโนโลยีการโฆษณาและประชาสัมพันธ์

3. เทคโนโลยีการพิมพ์ดิจิทัลและบรรจุภัณฑ์

4. ครีเอทีฟมีเดียเทคโนโลยี
```

Creative Media Technology ต้องรองรับอย่างน้อย:

```text
Web Full Stack
Game Development
```

อย่างไรก็ตาม ชื่อสาขา/หลักสูตรที่จะใส่ใน Production Seed ต้องตรวจสอบกับข้อมูลทางการของคณะก่อนใช้งานจริง

ห้ามสร้างชื่อหลักสูตรเพิ่มเติมจากการคาดเดา

---

# 13. Migration 003 — User Session

ไฟล์:

```text
003_create_user_session.sql
```

สร้าง:

```text
user_session
```

ระบบไม่มี Login

Session ใช้สำหรับการวิเคราะห์ชั่วคราว

Primary Key:

```text
UUID
```

Fields:

```text
session_id
major_id
consent_given
consent_given_at
created_at
expires_at
status
```

Status:

```text
ACTIVE
PROCESSING
COMPLETED
EXPIRED
DELETED
ERROR
```

Session ต้องสามารถเชื่อมโยงกับ Major ได้ แต่ Major ห้ามถูกใช้เป็น Hard Filter ของ Career Recommendation

---

# 14. Migration 004 — Career Family

ไฟล์:

```text
004_create_career_family.sql
```

สร้าง:

```text
career_family
```

Career Family เป็นระดับกลางระหว่าง:

```text
Faculty / Major
        ↓
Career Family
        ↓
Occupation
```

Career Family เริ่มต้น:

```text
CF01 Film & Video Production
CF02 Post-Production & Motion/VFX
CF03 Broadcast & Audio
CF04 Advertising & Creative
CF05 Digital Marketing & Content
CF06 PR & Corporate Communication
CF07 Graphic & Visual Communication
CF08 Packaging & Print Design
CF09 Prepress & Print Production
CF10 Web Development
CF11 UI/UX & Digital Product
CF12 Web Content & Growth
CF13 Game Design & Production
CF14 Game Development & Technical
CF15 Game Art & Animation
```

จำนวน Career Family ยังไม่ถือเป็นค่าถาวร

สามารถปรับจากผลการศึกษา Dataset และ Occupation Framework ได้

---

# 15. Migration 005 — Skill

ไฟล์:

```text
005_create_skill.sql
```

สร้าง:

```text
skill
```

เก็บ Canonical Skill

Fields หลัก:

```text
skill_id
skill_name
category
description
is_active
created_at
```

Category:

```text
TECHNICAL
DESIGN
CREATIVE
SOFTWARE_TOOL
COMMUNICATION
BUSINESS
OTHER
```

ตัวอย่าง Skill:

```text
HTML
CSS
JavaScript
TypeScript
React
Node.js
Python
SQL
Git
Figma
Adobe Photoshop
Adobe Illustrator
Adobe Premiere Pro
After Effects
Unity
Unreal Engine
UI Design
UX Design
Communication
Presentation
Project Management
```

รายการจริงต้องมาจาก Dataset Methodology

รายการด้านบนเป็นตัวอย่างสำหรับ Development / Seed เท่านั้น

---

# 16. Migration 006 — Skill Alias

ไฟล์:

```text
006_create_skill_alias.sql
```

สร้าง:

```text
skill_alias
```

ใช้ Mapping:

```text
Raw Skill
    ↓
Canonical Skill
```

ตัวอย่าง:

```text
React
React.js
ReactJS
```

→

```text
React
```

ตัวอย่าง:

```text
Adobe Photoshop
Photoshop
PS
```

→

```text
Adobe Photoshop
```

---

# 17. Migration 007 — Occupation

ไฟล์:

```text
007_create_occupation.sql
```

สร้าง:

```text
occupation
```

Fields หลัก:

```text
occupation_id
career_family_id
occupation_name
description
source
source_identifier
is_active
created_at
```

Occupation ต้องมี Source Traceability

ตัวอย่าง:

```text
ESCO
O*NET
Thai Labour Market
Job Posting Dataset
```

Occupation Framework ไม่ควรถูกสร้างจากความคิดเห็นของผู้พัฒนาเพียงอย่างเดียว

---

# 18. Occupation Source Strategy

Occupation Dataset ใช้แนวคิด:

```text
ESCO / O*NET
        +
Thai Labour Market Data
        ↓
Candidate Occupations
        ↓
Normalization
        ↓
Final Occupation Framework
```

ผู้เชี่ยวชาญสามารถใช้ตรวจสอบความเหมาะสมของ Occupation Framework ได้

แต่ไม่ควรใช้ผู้เชี่ยวชาญเป็นแหล่งข้อมูลเดียวในการสร้าง Occupation ทั้งหมด

---

# 19. Migration 008 — Occupation Alias

ไฟล์:

```text
008_create_occupation_alias.sql
```

สร้าง:

```text
occupation_alias
```

ใช้รวมชื่ออาชีพที่มีความหมายใกล้เคียงกัน

ตัวอย่าง:

```text
Frontend Developer
Front-end Developer
Frontend Engineer
Junior Frontend Developer
```

สามารถ Map ไปยัง Canonical Occupation เดียวกันเมื่อมีหลักฐานรองรับ

---

# 20. Migration 009 — Occupation Skill

ไฟล์:

```text
009_create_occupation_skill.sql
```

สร้าง:

```text
occupation_skill
```

ตารางนี้เป็นความสัมพันธ์:

```text
Occupation
    ↕
Skill
```

Fields สำคัญ:

```text
occupation_id
skill_id
importance
demand
source
```

ค่าของ:

```text
importance
demand
```

ต้องมาจาก Methodology ที่กำหนดไว้ใน:

```text
DATASET_SPEC.md
AI_MATCHING_SPEC.md
```

ห้ามใส่ตัวเลขแบบสุ่มเพื่อให้ระบบดูสมจริง

---

# 21. Migration 010 — Dataset Version

ไฟล์:

```text
010_create_dataset_version.sql
```

สร้าง:

```text
dataset_version
```

ใช้ควบคุม Version ของ Dataset

ตัวอย่าง:

```text
occupation-v1
skill-v1
job-posting-2026-01
```

ข้อมูลควรระบุ:

```text
dataset_name
version_name
source_description
collected_at
processed_at
record_count
description
created_at
```

วัตถุประสงค์:

```text
Career Result
    ↓
Dataset Version
```

เพื่อให้สามารถตรวจสอบย้อนหลังได้ว่าผลลัพธ์ถูกคำนวณจากข้อมูล Version ใด

---

# 22. Migration 011 — Resume

ไฟล์:

```text
011_create_resume.sql
```

สร้าง:

```text
resume
```

เชื่อมกับ:

```text
user_session
```

เก็บข้อมูลเกี่ยวกับ:

```text
file_name
file_type
file_size_bytes
storage_reference
extracted_text
processing_status
created_at
```

ไม่ควรเก็บ Binary File ขนาดใหญ่ไว้ใน PostgreSQL หากไม่มีเหตุผลจำเป็น

ควรเก็บ:

```text
File Storage Reference
```

แทน

---

# 23. Resume Processing Status

Resume Processing ต้องรองรับสถานะ เช่น:

```text
PENDING
PROCESSING
COMPLETED
FAILED
```

Flow:

```text
Upload
 ↓
Validation
 ↓
Parsing
 ↓
Text Extraction
 ↓
Skill Extraction
 ↓
Evidence Analysis
```

---

# 24. Migration 012 — Portfolio

ไฟล์:

```text
012_create_portfolio.sql
```

สร้าง:

```text
portfolio
```

เชื่อมกับ:

```text
user_session
```

เก็บ:

```text
url
platform
status
accessible
created_at
```

Status ที่รองรับ:

```text
PENDING
ACCESSIBLE
INACCESSIBLE
INVALID
BLOCKED
LOGIN_REQUIRED
UNSUPPORTED
ERROR
```

---

# 25. Portfolio Rule

Portfolio URL ไม่ถือเป็นหลักฐานของ Skill โดยอัตโนมัติ

ระบบต้อง:

```text
Portfolio URL
      ↓
Accessibility Check
      ↓
Content Analysis
      ↓
Project Detection
      ↓
Technology / Artifact Detection
      ↓
Evidence
      ↓
Skill
```

หากเข้าถึง Portfolio ไม่ได้:

```text
INACCESSIBLE
```

ต้องไม่ตีความว่า:

```text
User ไม่มี Skill
```

---

# 26. Migration 013 — Portfolio Project

ไฟล์:

```text
013_create_portfolio_project.sql
```

สร้าง:

```text
portfolio_project
```

เชื่อมกับ:

```text
portfolio
```

เก็บ:

```text
title
description
url
technologies
created_at
```

Project เป็นหน่วยกลางสำหรับ Evidence Analysis

ตัวอย่าง:

```text
Portfolio
    ↓
Project
    ↓
Technology
    ↓
Evidence
    ↓
Skill
```

---

# 27. Migration 014 — User Skill

ไฟล์:

```text
014_create_user_skill.sql
```

สร้าง:

```text
user_skill
```

ใช้เก็บ Candidate Skill Profile

ความสัมพันธ์:

```text
Session
   ↓
User Skill
```

Fields สำคัญ:

```text
session_id
skill_id
confidence
source
created_at
```

Source:

```text
RESUME
PORTFOLIO
BOTH
```

ระบบต้องสามารถตรวจสอบย้อนกลับได้ว่า Skill ถูกตรวจพบจากแหล่งใด

---

# 28. Migration 015 — Skill Evidence

ไฟล์:

```text
015_create_skill_evidence.sql
```

สร้าง:

```text
skill_evidence
```

Evidence Types:

```text
RESUME_SKILL
RESUME_PROJECT
RESUME_EXPERIENCE
RESUME_CERTIFICATE
PORTFOLIO_PROJECT
PORTFOLIO_DESCRIPTION
PORTFOLIO_TECHNOLOGY
PORTFOLIO_ARTIFACT
```

ความสัมพันธ์:

```text
User Skill
    ↓
Evidence
    ↓
Resume / Portfolio / Project
```

Evidence เป็นองค์ประกอบสำคัญของ Explainable Recommendation

---

# 29. Migration 016 — Job Posting

ไฟล์:

```text
016_create_job_posting.sql
```

สร้าง:

```text
job_posting
```

Fields หลัก:

```text
job_id
job_title
company
description
requirements
experience
location
source
source_url
date_collected
occupation_id
dataset_version_id
created_at
```

Job Posting ต้องมี:

```text
source
date_collected
dataset_version
```

เพื่อให้ตรวจสอบได้ว่า Labour Market Signal มาจากข้อมูลช่วงใด

---

# 30. Labour Market Data Rule

ระบบต้องไม่สร้าง:

```text
Demand = 80%
```

หรือ

```text
React = High Demand
```

จากการคาดเดา

Demand ต้องผ่านกระบวนการ:

```text
Job Posting
 ↓
Skill Extraction
 ↓
Skill Normalization
 ↓
Skill Frequency
 ↓
Demand Signal
```

---

# 31. Migration 017 — Job Posting Skill

ไฟล์:

```text
017_create_job_posting_skill.sql
```

สร้าง:

```text
job_posting_skill
```

ความสัมพันธ์:

```text
Job Posting
    ↕
Skill
```

เก็บ:

```text
job_id
skill_id
confidence
created_at
```

ใช้เป็นข้อมูลพื้นฐานสำหรับคำนวณ:

```text
Skill Demand
```

---

# 32. Migration 018 — Career Result

ไฟล์:

```text
018_create_career_result.sql
```

สร้าง:

```text
career_result
```

เชื่อม:

```text
Session
    ↓
Occupation
```

Fields:

```text
result_id
session_id
occupation_id
score
rank_position
explanation
algorithm_version
dataset_version_id
created_at
```

`score` หมายถึง:

```text
Career Match Score
```

หรือ

```text
Career Compatibility Score
```

ไม่ใช่:

```text
Employment Probability
```

ระบบต้องไม่แสดงผลว่า:

```text
มีโอกาสได้งาน 85%
```

หากไม่มีหลักฐานรองรับและไม่ใช่สิ่งที่ระบบได้รับการออกแบบให้ทำนาย

---

# 33. Career Result Traceability

Career Result ต้องตรวจสอบย้อนกลับได้:

```text
Career Result
      ↓
Occupation
      ↓
Occupation Skill
      ↓
Required Skill
      ↓
Candidate User Skill
      ↓
Evidence
      ↓
Resume / Portfolio
```

และ Labour Market:

```text
Career Result
      ↓
Occupation
      ↓
Occupation Skill
      ↓
Demand
      ↓
Job Posting Skill
      ↓
Job Posting
      ↓
Dataset Version
```

---

# 34. Migration 019 — Skill Gap

ไฟล์:

```text
019_create_skill_gap.sql
```

สร้าง:

```text
skill_gap
```

ความสัมพันธ์:

```text
Career Result
      ↓
Skill Gap
```

Status:

```text
MATCHED
PARTIAL
EVIDENCE_NOT_FOUND
```

Priority:

```text
HIGH
MEDIUM
LOW
```

---

# 35. Evidence Not Found Rule

ระบบต้องไม่แสดง:

```text
คุณไม่มี TypeScript
```

เพียงเพราะ Resume และ Portfolio ไม่พบ TypeScript

ให้ใช้:

```text
ยังไม่พบหลักฐานของ TypeScript
```

หรือ:

```text
Evidence Not Found
```

หลักการ:

```text
No Evidence
≠
No Skill
```

---

# 36. Skill Gap Priority

Priority ต้องพิจารณาจาก:

```text
Skill Importance
+
Labour Market Demand
+
Candidate Evidence
```

ไม่ควรกำหนด:

```text
HIGH
MEDIUM
LOW
```

แบบสุ่ม

ตัวอย่างแนวคิด:

```text
High Importance
+
High Demand
+
Evidence Not Found
        ↓
HIGH Priority
```

รายละเอียด Algorithm ต้องอ้างอิง:

```text
AI_MATCHING_SPEC.md
```

---

# 37. Migration 020 — User Feedback

ไฟล์:

```text
020_create_user_feedback.sql
```

สร้าง:

```text
user_feedback
```

ใช้สำหรับ:

```text
SUS
User Satisfaction
Comment
```

Fields:

```text
feedback_id
session_id
sus_score
satisfaction
comment
created_at
```

SUS ต้องใช้โครงสร้างมาตรฐาน 10 ข้อ

ไม่ควรดัดแปลงข้อคำถามมาตรฐานโดยไม่มีเหตุผลทาง Methodology

---

# 38. Migration 021 — Indexes

ไฟล์:

```text
021_create_indexes.sql
```

สร้าง Index ที่จำเป็นต่อ Query หลัก

ตัวอย่างกลุ่ม Index:

```text
user_session.major_id
user_session.status
user_session.expires_at

resume.session_id
portfolio.session_id

portfolio_project.portfolio_id

user_skill.session_id
user_skill.skill_id

skill_evidence.user_skill_id

occupation.career_family_id
occupation_alias.occupation_id

occupation_skill.occupation_id
occupation_skill.skill_id

job_posting.occupation_id
job_posting.dataset_version_id
job_posting.date_collected

job_posting_skill.job_id
job_posting_skill.skill_id

career_result.session_id
career_result.occupation_id

skill_gap.result_id

user_feedback.session_id
```

Index ต้องสร้างจาก Query Pattern จริงด้วย

ไม่ควรสร้าง Index ทุก Column โดยไม่มีเหตุผล

---

# 39. Foreign Key Dependency

Dependency ต้องมีโครงสร้างโดยประมาณดังนี้:

```text
major
 └── user_session
       ├── resume
       ├── portfolio
       │     └── portfolio_project
       ├── user_skill
       │     └── skill_evidence
       ├── career_result
       │     └── skill_gap
       └── user_feedback


career_family
 └── occupation
       ├── occupation_alias
       ├── occupation_skill
       └── career_result


skill
 ├── skill_alias
 ├── user_skill
 ├── occupation_skill
 └── job_posting_skill


dataset_version
 ├── job_posting
 └── career_result


job_posting
 └── job_posting_skill
```

Migration ต้องสร้าง Parent Table ก่อน Child Table

---

# 40. Transaction Strategy

Migration ควรทำงานแบบ Atomic เมื่อ PostgreSQL รองรับ

แนวคิด:

```text
BEGIN
    CREATE / ALTER
    CREATE constraints
    CREATE required indexes
COMMIT
```

หากเกิด Error:

```text
ROLLBACK
```

ไม่ควรปล่อย Database อยู่ในสถานะครึ่งหนึ่งของ Migration

ข้อยกเว้น เช่น PostgreSQL operation ที่ไม่สามารถทำงานภายใน Transaction ได้ ต้องจัดการตามข้อจำกัดของ PostgreSQL และ Migration Tool ที่เลือกใช้

หากมีการใช้:

```text
CREATE INDEX CONCURRENTLY
```

ต้องตรวจสอบ Transaction Requirement ก่อนใช้งาน

---

# 41. Idempotency

Migration ต้องเข้าใจความแตกต่างระหว่าง:

```text
Migration
```

และ

```text
Initialization Script
```

Migration ที่ถูก Apply แล้วไม่ควรถูกรันซ้ำ

ดังนั้น:

```text
Migration Version
```

ต้องถูกตรวจสอบก่อน Apply

อย่างไรก็ตามคำสั่งเริ่มต้นบางประเภท เช่น:

```sql
CREATE SCHEMA IF NOT EXISTS
```

สามารถใช้เพื่อช่วยให้ Initialization มีความปลอดภัยมากขึ้นได้

แต่ไม่ควรใช้ `IF NOT EXISTS` เพื่อซ่อน Schema Error ใน Migration ที่ควรตรวจสอบอย่างจริงจัง

---

# 42. Seed Strategy

Seed ต้องแยกออกจาก Migration

```text
Migration
    ↓
สร้างโครงสร้าง Database

Seed
    ↓
ใส่ข้อมูลเริ่มต้น
```

ห้ามนำข้อมูล User จริงเข้า Seed

---

# 43. Seed Categories

แบ่งเป็น 3 กลุ่ม

## 43.1 Development Seed

ใช้สำหรับ:

```text
Development
Testing
Demo
```

เช่น:

```text
Sample Major
Sample Skill
Sample Occupation
Sample Job Posting
```

ข้อมูลต้องระบุชัดเจนว่าเป็น:

```text
DEMO / TEST DATA
```

---

## 43.2 Reference Seed

ใช้สำหรับข้อมูล Reference ที่ผ่านการตรวจสอบแล้ว เช่น:

```text
Career Family
Major
Canonical Skill
Occupation
Occupation Alias
```

ข้อมูลจริงต้องผ่านกระบวนการ:

```text
Source Collection
 ↓
Validation
 ↓
Normalization
 ↓
Import
```

---

## 43.3 Labour Market Dataset

Job Posting ไม่ควรถูกมองเป็น Static Seed แบบถาวร

ควรใช้:

```text
Dataset Import Pipeline
```

เช่น:

```text
CSV / JSON
 ↓
Validation
 ↓
Cleaning
 ↓
Normalization
 ↓
Deduplication
 ↓
Skill Extraction
 ↓
Occupation Mapping
 ↓
PostgreSQL
```

---

# 44. Initial Major Seed

Development Environment สามารถมีข้อมูลเริ่มต้นสำหรับ:

```text
เทคโนโลยีการผลิตภาพยนตร์และวิทยุโทรทัศน์
เทคโนโลยีการโฆษณาและประชาสัมพันธ์
เทคโนโลยีการพิมพ์ดิจิทัลและบรรจุภัณฑ์
ครีเอทีฟมีเดียเทคโนโลยี
```

และภายใต้ Creative Media Technology:

```text
Web Full Stack
Game Development
```

แต่ก่อน Production ต้องตรวจสอบชื่อทางการกับข้อมูลหลักสูตรของคณะ

---

# 45. Initial Career Family Seed

Development Seed สามารถเริ่มจาก:

```text
CF01 Film & Video Production
CF02 Post-Production & Motion/VFX
CF03 Broadcast & Audio
CF04 Advertising & Creative
CF05 Digital Marketing & Content
CF06 PR & Corporate Communication
CF07 Graphic & Visual Communication
CF08 Packaging & Print Design
CF09 Prepress & Print Production
CF10 Web Development
CF11 UI/UX & Digital Product
CF12 Web Content & Growth
CF13 Game Design & Production
CF14 Game Development & Technical
CF15 Game Art & Animation
```

รายการนี้เป็น:

```text
Initial Framework
```

ไม่ใช่ Final Occupation Dataset

---

# 46. Development Skill Seed

สำหรับการพัฒนา MVP สามารถใช้ Skill ตัวอย่าง เช่น:

```text
HTML
CSS
JavaScript
TypeScript
React
Next.js
Node.js
Express.js
Python
SQL
PostgreSQL
Git
Figma
Adobe Photoshop
Adobe Illustrator
UI Design
UX Design
Communication
Presentation
Project Management
```

ข้อมูลเหล่านี้ใช้เพื่อ:

```text
Development
Testing
Demo
```

ไม่ควรนำไปอ้างว่าเป็น Skill Taxonomy ที่สมบูรณ์ของคณะโดยไม่มี Dataset Methodology รองรับ

---

# 47. Development Occupation Seed

สำหรับ Vertical Slice สามารถสร้าง Occupation ตัวอย่าง เช่น:

```text
Front-end Developer
Back-end Developer
Full-stack Developer
Web Developer
UI/UX Designer
Graphic Designer
Video Editor
Game Programmer
Game Designer
```

ต้องระบุว่า:

```text
DEMO / DEVELOPMENT DATA
```

จนกว่าจะถูกแทนที่ด้วย Occupation Framework จาก:

```text
ESCO / O*NET
+
Thai Labour Market
+
Normalization
+
Optional Expert Validation
```

---

# 48. No Real User Data in Seed

ห้ามใส่ข้อมูลจริงของนักศึกษาใน:

```text
Migration
Seed
Repository
Docker Image
GitHub
```

โดยเฉพาะ:

```text
Resume
Email
Phone Number
Personal Address
Portfolio Credentials
Private Portfolio
Personal Identification Data
```

---

# 49. Migration Testing

Migration ต้องผ่านอย่างน้อย 5 ระดับ

## Test 1 — Fresh Database

สร้าง PostgreSQL Database ใหม่จากศูนย์

```text
Empty DB
 ↓
All Migrations
 ↓
Success
```

---

## Test 2 — Migration Order

ตรวจสอบว่า:

```text
001
002
003
...
021
```

ทำงานตามลำดับ Dependency

---

## Test 3 — Foreign Key

ทดสอบว่าไม่สามารถสร้างข้อมูล Child ที่ไม่มี Parent ได้

ตัวอย่าง:

```text
occupation_skill
```

ต้องไม่สามารถอ้าง:

```text
occupation_id
```

ที่ไม่มีอยู่จริง

---

## Test 4 — Constraints

ตรวจสอบ:

```text
PRIMARY KEY
FOREIGN KEY
UNIQUE
NOT NULL
CHECK
```

---

## Test 5 — Index

ตรวจสอบ Index สำคัญว่าถูกสร้างครบและ Query สามารถใช้ได้อย่างเหมาะสม

---

# 50. Rollback Strategy

โครงการนี้ใช้ Approach B (SQL Migration) แบบ Reverse Migration ไม่มีไฟล์ down การแก้ไขทำด้วย Migration ใหม่ที่ย้อนการเปลี่ยนแปลง ดู `docs/decisions/0003-database-tooling.md`

รายละเอียดของทั้งสองแนวทางเก็บไว้เพื่ออ้างอิง

มีสองแนวทางหลัก:

### Approach A — Migration Tool

Tool จัดการ:

```text
up
down
version
rollback
```

### Approach B — SQL Migration

กำหนด Rollback SQL อย่างชัดเจนหรือสร้าง Reverse Migration

ตัวอย่าง:

```text
022_add_portfolio_metadata.sql
```

ไม่ควรใช้:

```text
DROP DATABASE
```

เพื่อแก้ปัญหา Migration ใน Production

---

# 51. Fresh Database Reproducibility

เป้าหมายสำคัญ:

```text
Developer A
+
Developer B
+
CI/CD
```

ควรสามารถสร้าง Schema เดียวกันจาก Migration Repository เดียวกัน

```text
Git Repository
       ↓
Migration Files
       ↓
PostgreSQL
       ↓
Same Schema
```

---

# 52. Docker Database Flow

Development:

```text
docker compose up
        ↓
PostgreSQL Container
        ↓
Database Ready
        ↓
Run Migrations
        ↓
Run Seed
        ↓
Backend
        ↓
Frontend
```

ไม่ควรพึ่งพา Database ที่ติดตั้งเฉพาะเครื่องใดเครื่องหนึ่ง

---

# 53. Environment Separation

อย่างน้อยควรแยก:

```text
Development
Test
Production
```

ตัวอย่าง:

```text
career_system_dev
career_system_test
career_system_prod
```

Production Database ต้องไม่ใช้ข้อมูล Demo

Test Database ต้องไม่ใช้ข้อมูลส่วนตัวจริง

---

# 54. Database Backup

Production ต้องมีแผน Backup

ตัวอย่าง:

```text
PostgreSQL
    ↓
Backup
    ↓
Secure Storage
```

Backup ต้องไม่ถูก Commit เข้า Git Repository

เช่น:

```text
*.sql
*.dump
*.backup
```

ควรอยู่ใน `.gitignore` หากเป็นไฟล์ Backup ที่สร้างจาก Environment จริง

---

# 55. Privacy and Retention

ข้อมูล Resume และ Portfolio ที่เกี่ยวข้องกับ User Session ถือเป็นข้อมูลที่ต้องจัดการอย่างระมัดระวัง

หลักการ:

```text
Upload
 ↓
Process
 ↓
Analyze
 ↓
Return Result
 ↓
Temporary Storage
 ↓
Delete / Retention Policy
```

Session หมดอายุแล้วควรมีกระบวนการ:

```text
Expiration
 ↓
Cleanup
```

ไม่ควรเก็บ Resume และ Portfolio ไว้ถาวรโดยไม่มีเหตุผล

---

# 56. Schema Change Management

หาก Requirement ใหม่ต้องการ Column ใหม่:

ตัวอย่าง:

```text
ต้องการเพิ่ม portfolio_hash
```

ต้องดำเนินการ:

```text
1. วิเคราะห์ Requirement
2. Update DATABASE.md
3. ตรวจสอบ AI_MATCHING_SPEC.md
4. ตรวจสอบ UI_UX_SPEC.md
5. ตรวจสอบ API.md
6. สร้าง Migration ใหม่
7. Test Migration
8. Update Documentation
```

ห้ามแก้ Database โดยตรงแล้วค่อยมาแก้ Documentation ภายหลัง

---

# 57. Example Schema Change

สมมติว่าต้องเพิ่ม:

```text
portfolio.last_checked_at
```

ห้ามแก้:

```text
012_create_portfolio.sql
```

หาก Migration ถูก Apply แล้ว

ให้สร้าง:

```text
022_add_portfolio_last_checked_at.sql
```

ตัวอย่าง:

```sql
ALTER TABLE portfolio
ADD COLUMN last_checked_at TIMESTAMPTZ;
```

จากนั้น Test:

```text
Fresh DB
Existing DB
Application
API
Portfolio Analyzer
```

---

# 58. Migration and AI Compatibility

Database Schema ต้องรองรับ AI Pipeline:

```text
Resume
 ↓
Extracted Text
 ↓
Skill
 ↓
User Skill
 ↓
Evidence
```

และ:

```text
Job Posting
 ↓
Job Posting Skill
 ↓
Occupation Skill
 ↓
Career Matching
```

ดังนั้น Schema Change ที่กระทบข้อมูลเหล่านี้ต้องตรวจสอบ:

```text
AI_MATCHING_SPEC.md
DATASET_SPEC.md
```

ทุกครั้ง

---

# 59. Migration and API Compatibility

API ไม่ควรขึ้นกับ Database Schema โดยตรง

Architecture:

```text
Next.js
   ↓
Express API
   ↓
Service
   ↓
Repository
   ↓
PostgreSQL
```

หาก Schema เปลี่ยน:

```text
Database
 ↓
Repository
 ↓
Service
 ↓
API Response
```

ต้องตรวจสอบทุก Layer ที่ได้รับผลกระทบ

---

# 60. Migration and Frontend Compatibility

Frontend ไม่ควรอ่าน Database โดยตรง

ห้าม:

```text
Next.js
   ↓
PostgreSQL
```

ต้องเป็น:

```text
Next.js
   ↓
Express API
   ↓
PostgreSQL
```

หาก Schema เปลี่ยนและ API Response เปลี่ยน ต้องตรวจสอบ UI ที่เกี่ยวข้อง

---

# 61. CI Migration Test

ในอนาคต GitHub/CI สามารถทำ:

```text
Push Code
   ↓
Start PostgreSQL
   ↓
Run All Migrations
   ↓
Run Seed
   ↓
Run Tests
   ↓
Build
```

หาก Migration ล้มเหลว:

```text
CI = FAILED
```

ไม่ควร Merge Code ที่ทำให้ Fresh Database สร้างไม่ได้

---

# 62. Migration Documentation

`database/README.md` ควรอธิบาย:

```text
Database Purpose
Migration Tool
How to Run Migration
How to Reset Development DB
How to Run Seed
How to Run Tests
How to Create New Migration
Migration Naming Convention
Rollback Policy
Environment Variables
```

---

# 63. Recommended Development Commands

คำสั่งจริงต้องปรับตาม Migration Tool ที่เลือกใน Phase 0

แนวคิด:

```bash
# Start PostgreSQL
docker compose up -d postgres

# Run migrations
<database-migration-command>

# Run development seed
<database-seed-command>

# Check database
<database-status-command>

# Run tests
npm test
```

ไม่ควรเขียน Command ที่ขึ้นกับ Tool ใด Tool หนึ่งเป็นข้อบังคับจนกว่าจะตัดสินใจเลือก Migration Tool

---

# 64. Migration Tool Decision

ใน Phase 0 ต้องเลือกวิธีจัดการ Migration อย่างเป็นทางการ

ตัวเลือกสามารถเป็น:

```text
SQL Migration Files
```

หรือ

```text
TypeScript/Node.js Migration Tool
```

หลักเกณฑ์:

* PostgreSQL Support
* TypeScript Compatibility
* Transaction Support
* Migration Versioning
* Rollback Support
* Docker Compatibility
* CI Compatibility
* Team Maintainability
* SQL Transparency

ไม่ควรเลือก Tool เพียงเพราะเป็น Tool ที่ได้รับความนิยม

ต้องเลือกตาม Architecture ของ Project

ตัดสินใจแล้ว: SQL Migration Files พร้อมตาราง `schema_migrations` ดู `docs/decisions/0003-database-tooling.md`

---

# 65. ORM Rule

หากภายหลังเลือก ORM เช่น:

```text
Prisma
Drizzle
TypeORM
```

ต้องตรวจสอบว่า ORM ไม่ทำให้ Database Schema ขัดกับ:

```text
DATABASE.md
```

ORM เป็น Implementation Layer

ไม่ใช่ Source of Truth สูงกว่า Database Design

โครงการนี้เลือกไม่ใช้ ORM (ใช้ node-postgres เขียน SQL ใน Repository Layer) ดู `docs/decisions/0003-database-tooling.md`

---

# 66. No Arbitrary Schema Expansion

Claude ห้ามสร้าง Table ใหม่เพียงเพราะคิดว่าน่าจะมีประโยชน์

ก่อนสร้าง Table ใหม่ต้องตอบ:

```text
1. Table นี้แก้ปัญหาอะไร?
2. Requirement ใดต้องใช้?
3. มี Table เดิมที่รองรับหรือไม่?
4. DATABASE.md ต้องอัปเดตหรือไม่?
5. API ต้องเปลี่ยนหรือไม่?
6. AI Pipeline ต้องเปลี่ยนหรือไม่?
```

หากตอบไม่ได้:

```text
Do Not Add Table
```

---

# 67. Database Versioning

ระบบต้องสามารถระบุ Version ของข้อมูลสำคัญ:

```text
Schema Version
Dataset Version
Algorithm Version
```

ตัวอย่าง:

```text
Schema:
migration-024

Dataset:
job-posting-2026-01

Algorithm:
matching-v1
```

ผลลัพธ์ Career Recommendation ต้องสามารถ Trace กลับไปยัง:

```text
Algorithm Version
+
Dataset Version
```

---

# 68. End-to-End Data Traceability

เป้าหมายสูงสุดของ Database:

```text
User Input
    ↓
Session
    ↓
Resume / Portfolio
    ↓
Evidence
    ↓
User Skill
    ↓
Occupation Skill
    ↓
Job Posting
    ↓
Market Demand
    ↓
Career Result
    ↓
Skill Gap
    ↓
Guidance
    ↓
Feedback
```

Database ต้องสนับสนุน Traceability นี้โดยไม่สร้างความสัมพันธ์ที่เกินความจำเป็น

---

# 69. Semester 1 Database Scope

Semester 1 เป็น Pilot:

```text
Creative Media Technology
        ↓
Web Full Stack
```

Database ควรสร้าง Schema เต็มที่รองรับระบบหลัก แต่ Dataset สามารถเริ่มจาก Scope ที่เล็กกว่าได้

ตัวอย่าง:

```text
Web Development
UI/UX
Related Digital Careers
```

ไม่จำเป็นต้องเก็บ Labour Market Dataset ของทุก Career Family ให้ครบตั้งแต่วันแรก

---

# 70. Semester 2 Database Expansion

Semester 2 ต้องขยาย Dataset ไปยัง:

```text
Film & TV
Advertising & PR
Digital Printing & Packaging
Creative Media Technology
```

และต้องรองรับ:

```text
Web Full Stack
Game Development
```

Database Schema ไม่ควรถูกออกแบบให้ใช้ได้เฉพาะ Web Full Stack

---

# 71. Development Priority

ลำดับการทำจริง:

```text
1. Database Schema
2. Migration
3. Reference Seed
4. Dataset Pipeline
5. Backend Repository
6. Resume Processing
7. Portfolio Processing
8. Skill Extraction
9. Candidate Skill Profile
10. Career Matching
11. Skill Gap
12. Explanation
13. API
14. Frontend
15. Evaluation
```

---

# 72. Vertical Slice

ก่อนสร้างระบบเต็ม ให้สร้าง Vertical Slice:

```text
Major Selection
      ↓
Create Session
      ↓
Upload Resume
      ↓
Extract Basic Skills
      ↓
Normalize Skills
      ↓
Save User Skills
      ↓
Return Candidate Skill Profile
```

หาก Vertical Slice นี้ทำงานครบ:

```text
Database
+
Backend
+
AI
+
Frontend
```

จึงค่อยเพิ่ม Portfolio และ Career Matching

---

# 73. Testing Checklist

ก่อนถือว่า Database Migration พร้อม ต้องตรวจสอบ:

### Schema

* [ ] Schema `career_system` ถูกสร้าง
* [ ] ทุก Core Table ถูกสร้าง
* [ ] Primary Keys ถูกต้อง
* [ ] Foreign Keys ถูกต้อง
* [ ] Unique Constraints ถูกต้อง
* [ ] Check Constraints ถูกต้อง
* [ ] NOT NULL ถูกต้อง
* [ ] Indexes ถูกต้อง

### Migration

* [ ] Migration มีลำดับ
* [ ] Migration Version ถูกบันทึก
* [ ] Fresh Database ทำงานได้
* [ ] Migration ไม่พึ่งข้อมูลจากเครื่อง Developer
* [ ] Migration ไม่ใช้ MySQL/MariaDB syntax

### Seed

* [ ] Development Seed แยกจาก Migration
* [ ] Reference Seed แยกจาก Labour Market Import
* [ ] ไม่มีข้อมูล User จริง
* [ ] ไม่มี Password
* [ ] ไม่มี API Key
* [ ] ไม่มี Private Credential

### Application

* [ ] Backend เชื่อม PostgreSQL ได้
* [ ] Repository Query ทำงาน
* [ ] AI Result บันทึกได้
* [ ] Career Result Traceable
* [ ] Skill Gap Traceable

---

# 74. Definition of Done

`DATABASE_MIGRATION_PLAN.md` ถือว่าถูก Implement เมื่อ:

```text
[✓] PostgreSQL ถูกใช้เป็น Main Database

[✓] Migration Directory ถูกสร้าง

[✓] Migration มีลำดับชัดเจน

[✓] Core Schema จาก DATABASE.md ถูกแปลงเป็น Migration

[✓] Foreign Key Dependency ถูกต้อง

[✓] Fresh Database สามารถสร้างได้

[✓] Seed แยกจาก Migration

[✓] Development/Test/Production แยกกัน

[✓] ไม่มีข้อมูลส่วนบุคคลจริงใน Repository

[✓] Migration Version ถูกติดตาม

[✓] Database สามารถ Trace Career Result ได้

[✓] Dataset Version ถูกบันทึก

[✓] Algorithm Version ถูกบันทึก

[✓] Schema สามารถรองรับ Semester 1 และ Semester 2
```

---

# 75. Final Rules for Claude

Claude ต้องอ่านเอกสารต่อไปนี้ก่อน Implement:

```text
PROJECT_SPEC.md
DATABASE.md
DATASET_SPEC.md
AI_MATCHING_SPEC.md
UI_UX_SPEC.md
TECH_STACK.md
IMPLEMENTATION_PLAN.md
API.md
FOLDER_STRUCTURE.md
ENVIRONMENT_SETUP.md
DATABASE_MIGRATION_PLAN.md
```

จากนั้นให้ปฏิบัติตามกฎ:

1. PostgreSQL เท่านั้น
2. ห้ามใช้ MySQL/MariaDB syntax
3. ห้ามใช้ MongoDB เป็น Main Database
4. ห้ามสร้าง Database Schema ใหม่โดยไม่ตรวจสอบ `DATABASE.md`
5. ห้ามแก้ Applied Migration เดิม
6. Schema Change ต้องสร้าง Migration ใหม่
7. Migration ต้องสามารถสร้าง Fresh Database ได้
8. Foreign Key ต้องถูกสร้างตาม Dependency
9. Seed ต้องแยกจาก Migration
10. ห้ามใส่ข้อมูล User จริงใน Seed
11. ห้ามใส่ Password หรือ API Key ใน Database Seed
12. ห้ามสร้าง Labour Market Demand แบบสมมติ
13. ห้ามใช้ Major เป็น Hard Filter ของ Career
14. ห้ามใช้ Career Match Score เป็น Employment Probability
15. ต้องรักษา Evidence Traceability
16. ต้องรักษา Dataset Traceability
17. ต้องรักษา Algorithm Version
18. ต้องรองรับ Semester 1 Web Full Stack Pilot
19. ต้องรองรับ Semester 2 Whole Faculty Expansion
20. หาก Schema Change กระทบ AI/API/UI ให้ตรวจสอบเอกสารที่เกี่ยวข้อง
21. ทุก Migration ต้องผ่าน Fresh Database Test
22. ห้ามสร้าง Table ใหม่โดยไม่มี Requirement รองรับ
23. ห้ามนำข้อมูลจริงของนักศึกษาเข้า Git
24. ห้ามทำให้ Python AI Service กลายเป็นเจ้าของ Database Schema
25. Backend เป็นผู้ควบคุม Application-Level Database Operation

---

# 76. Final Database Architecture

```text
                    PostgreSQL
                         │
                career_system schema
                         │
        ┌────────────────┼────────────────┐
        │                │                │
     Knowledge       User Session     Labour Market
        │                │                │
  ┌─────┼─────┐     ┌────┼────┐       ┌──┴──────┐
  │     │     │     │    │    │       │         │
Skill Occupation  Resume Portfolio  Job Posting Dataset
  │     │          │      │           │
  │     │          │   Project        │
  │     │          │      │           │
  └─────┴──────────┴──────┴───────────┘
                 │
          Evidence / Profile
                 │
          Career Matching
                 │
          Career Result
                 │
             Skill Gap
                 │
             Guidance
                 │
             Feedback
```

---

# 77. Final Project Flow

```text
User
 ↓
Next.js
 ↓
Express API
 ↓
PostgreSQL Session
 ↓
Resume / Portfolio
 ↓
Python AI/NLP
 ↓
Skill Extraction
 ↓
Skill Normalization
 ↓
Evidence
 ↓
Candidate Skill Profile
 ↓
Occupation Knowledge
 +
Labour Market Dataset
 ↓
Career Matching
 ↓
Career Result
 ↓
Skill Gap
 ↓
Development Guidance
 ↓
User Feedback
```

---

# 78. Status

```text
Project Concept: LOCKED
Core Workflow: LOCKED
No Login: LOCKED
Major as Context: LOCKED
Cross-Major Matching: LOCKED
Resume + Portfolio: LOCKED
Evidence-Based Analysis: LOCKED
Labour Market Orientation: LOCKED
Explainable Recommendation: LOCKED
Skill Gap: LOCKED
Development Guidance: LOCKED
Evaluation Framework: LOCKED
Semester 1 Web Full Stack Pilot: LOCKED
Semester 2 Whole Faculty Expansion: LOCKED

Technology Stack: LOCKED
Frontend: Next.js + React + TypeScript + Tailwind CSS
Backend: Node.js + Express.js + TypeScript
AI/NLP: Python
Database: PostgreSQL
Container: Docker + Docker Compose
Version Control: Git + GitHub

Database Schema: DATABASE.md
Migration Strategy: DATABASE_MIGRATION_PLAN.md
Dataset Specification: DATASET_SPEC.md
AI/NLP Methodology: AI_MATCHING_SPEC.md
UI/UX Specification: UI_UX_SPEC.md
Technology Specification: TECH_STACK.md
Implementation Plan: IMPLEMENTATION_PLAN.md
Environment Setup: ENVIRONMENT_SETUP.md
```

---

# END OF DATABASE_MIGRATION_PLAN.md