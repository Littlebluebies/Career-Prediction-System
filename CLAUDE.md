# CLAUDE.md

# Career Prediction System

## 1. Project

ชื่อโครงการ:

ระบบทำนายอาชีพสำหรับนักศึกษาคณะเทคโนโลยีสื่อสารมวลชนโดยอิงการวิเคราะห์ทักษะและความต้องการของตลาดแรงงาน

English:

Career Prediction and Skill Gap Analysis System for Mass Communication Technology Students Based on Skill Evidence and Labour Market Demand.

---

# 2. Project Goal

ระบบมีหน้าที่ประเมินความเหมาะสมของอาชีพจาก:

* Skills ที่ตรวจพบ
* Resume Evidence
* Portfolio Evidence
* Occupation Knowledge
* Labour Market Demand

จากนั้น:

```text
Candidate Skill Profile
        ↓
Career Matching
        ↓
Top 3–5 Career Recommendations
        ↓
Explainable Recommendation
        ↓
Skill Gap Analysis
        ↓
Development Guidance
```

ระบบไม่ได้รับประกันว่าผู้ใช้จะได้งาน

---

# 3. Source of Truth

ก่อนแก้ไขหรือสร้างระบบ ให้ตรวจสอบเอกสารตามลำดับ:

```text
PROJECT_SPEC.md
        ↓
TECH_STACK.md
        ↓
DATABASE.md
        ↓
DATASET_SPEC.md
        ↓
AI_MATCHING_SPEC.md
        ↓
UI_UX_SPEC.md
        ↓
API.md
        ↓
IMPLEMENTATION_PLAN.md
        ↓
FOLDER_STRUCTURE.md
        ↓
ENVIRONMENT_SETUP.md
        ↓
DATABASE_MIGRATION_PLAN.md
```

ไฟล์จริงอยู่ภายใต้:

```text
docs/
```

แบ่งเป็น `00-source-of-truth`, `01-architecture`, `02-database`, `03-ai-data`, `04-design` และ `decisions` การตัดสินใจทางเทคนิคที่เอกสารเปิดให้เลือกภายหลังบันทึกที่ `docs/decisions/`

หากมีข้อขัดแย้ง:

1. หยุดก่อน Implement ส่วนที่ได้รับผลกระทบ
2. ระบุเอกสารที่ขัดแย้ง
3. อธิบายความขัดแย้ง
4. เสนอวิธีแก้
5. ห้ามแก้ Source of Truth โดยอัตโนมัติ

---

# 4. Locked Technology Stack

Frontend:

```text
Next.js
React
TypeScript
Tailwind CSS
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

Database:

```text
PostgreSQL
```

Infrastructure:

```text
Docker
Docker Compose
```

Version Control:

```text
Git
GitHub
```

ห้ามเปลี่ยน Technology Stack โดยไม่ได้รับอนุญาต

---

# 5. Architecture

```text
User
 ↓
Next.js
 ↓ REST API
Express.js
 ↓
Service Layer
 ↓
Repository Layer
 ↓
PostgreSQL

Express.js
 ↓
Python AI/NLP Service
```

Responsibilities:

```text
Next.js
= UI / Frontend

Express
= API / Business Logic / Orchestration

Python
= AI / NLP / Data Processing

PostgreSQL
= Main Database
```

ห้าม:

```text
Next.js → PostgreSQL
```

โดยตรง

ห้ามให้ Python กลายเป็น Main Backend

ห้ามสร้าง Backend ซ้ำระหว่าง Next.js และ Express

---

# 6. Core Rules

## No Login

ระบบไม่มี User Login

ใช้ Temporary Session

---

## Major Is Context

Major ใช้เป็น Context เท่านั้น

ห้ามใช้ Major เป็น Hard Filter ของ Career

ผู้ใช้สามารถได้รับ Career Recommendation ที่อยู่นอก Major หาก Skills และ Evidence สอดคล้อง

---

## Evidence-Based

Portfolio URL ไม่ถือเป็น Evidence โดยอัตโนมัติ

ต้องวิเคราะห์:

```text
Portfolio
 ↓
Project
 ↓
Description / Technology / Artifact
 ↓
Evidence
 ↓
Skill
```

---

## Evidence Not Found

ห้ามสรุปว่า:

```text
User ไม่มี Skill
```

เพียงเพราะไม่พบข้อมูล

ใช้:

```text
Evidence Not Found
ยังไม่พบหลักฐานของ Skill
```

---

## Career Score

ใช้:

```text
Career Match Score
Career Compatibility Score
```

ห้ามใช้:

```text
Employment Probability
Chance of Getting Hired
```

---

## Labour Market

ห้ามสร้าง Demand จากการคาดเดา

Demand ต้องมาจาก:

```text
Job Posting
 ↓
Skill Extraction
 ↓
Skill Normalization
 ↓
Demand Analysis
```

---

# 7. Database Rules

PostgreSQL เท่านั้น

Schema ต้องอ้างอิง:

```text
docs/02-database/DATABASE.md
docs/02-database/DATABASE_MIGRATION_PLAN.md
```

ห้าม:

* ใช้ MySQL syntax
* ใช้ MariaDB syntax
* ใช้ MongoDB เป็น Main Database
* แก้ Applied Migration
* สร้าง Table ใหม่โดยไม่มี Requirement
* ใส่ข้อมูล User จริงใน Seed

Schema Change:

```text
Requirement
 ↓
Update Documentation
 ↓
New Migration
 ↓
Test
```

---

# 8. Development Strategy

พัฒนาแบบ Incremental

ห้ามสร้างทุก Feature ในครั้งเดียว

ลำดับหลัก:

```text
Phase 0
Project Setup

Phase 1
Database

Phase 2
Reference Data

Phase 3
Labour Market Dataset

Phase 4
Resume Processing

Phase 5
Portfolio Processing

Phase 6
Skill & Evidence Pipeline

Phase 7
Career Matching

Phase 8
Skill Gap & Guidance

Phase 9
Backend API

Phase 10
Frontend

Phase 11
Integration & Testing

Phase 12
Evaluation

Phase 13
Deployment
```

---

# 9. Current Development Rule

ในแต่ละ Session ให้ทำเฉพาะ Phase ที่ผู้ใช้มอบหมาย

ห้ามข้าม Phase โดยไม่ได้รับคำสั่ง

หาก Phase ปัจจุบันยังไม่ผ่าน Test:

```text
DO NOT
```

ไปยัง Phase ถัดไป

---

# 10. Implementation Loop

ทุก Feature ต้องใช้:

```text
Understand
 ↓
Plan
 ↓
Implement
 ↓
Run
 ↓
Test
 ↓
Fix
 ↓
Verify
 ↓
Report
```

---

# 11. Required Report

เมื่อทำ Task เสร็จ ให้รายงาน:

```text
## Implemented

สิ่งที่ทำ

## Files Created

ไฟล์ที่สร้าง

## Files Modified

ไฟล์ที่แก้

## Database Changes

ถ้ามี

## API Changes

ถ้ามี

## Test Results

ผลการทดสอบ

## Known Issues

ปัญหาที่เหลือ

## Next Step

ขั้นตอนถัดไป
```

---

# 12. Coding Rules

ใช้:

```text
TypeScript
ESLint
Validation
Error Handling
Reusable Components
Environment Variables
Layered Architecture
```

Backend:

```text
Route
 ↓
Controller
 ↓
Service
 ↓
Repository
 ↓
Database
```

Business Logic ไม่ควรอยู่ใน Route โดยตรง

---

# 13. Security

ห้าม Hard-code:

```text
Password
API Key
Secret
Token
Credential
```

ห้าม Commit:

```text
.env
Real Resume
Private Portfolio Data
Production Database Dump
Real Student Data
```

---

# 14. Privacy

Resume และ Portfolio เป็นข้อมูลที่ต้องจัดการอย่างระมัดระวัง

Flow:

```text
Upload
 ↓
Process
 ↓
Analyze
 ↓
Return Result
 ↓
Retention Policy
 ↓
Delete
```

---

# 15. Semester Scope

## Semester 1

Pilot:

```text
Creative Media Technology
        ↓
Web Full Stack
```

เป้าหมายแรกคือสร้าง Vertical Slice ที่ทำงานจริง

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
Candidate Skill Profile
```

เมื่อ Vertical Slice ผ่านการทดสอบ ให้ต่อยอดเป็น Semester 1 MVP ตาม `IMPLEMENTATION_PLAN.md` §75 และ §80 (Portfolio, Career Matching, Explanation, Skill Gap, Guidance) ดู `docs/decisions/0002-phase-numbering-and-semester-1-scope.md`

---

## Semester 2

ขยายระบบให้รองรับทั้งคณะ:

```text
Film & TV
Advertising & PR
Digital Printing & Packaging
Creative Media Technology
```

และ:

```text
Web Full Stack
Game Development
```

---

# 16. Do Not Overengineer

ห้ามเพิ่ม Feature ที่ไม่ได้อยู่ใน Scope เช่น:

* Authentication
* Payment
* Social Login
* Chat System
* Marketplace
* Mobile Application
* Unnecessary Microservices

เว้นแต่ผู้ใช้สั่งโดยตรง

---

# 17. Important Principle

ระบบนี้ต้องรักษา:

```text
Evidence
+
Explainability
+
Labour Market Traceability
+
Dataset Version
+
Algorithm Version
```

Career Recommendation ต้องสามารถอธิบายได้ว่า:

```text
ทำไม Career นี้จึงถูกแนะนำ
↓
Matched Skills คืออะไร
↓
Evidence มาจากไหน
↓
ตลาดแรงงานต้องการ Skill อะไร
↓
Skill Gap คืออะไร
```

---

# 18. Before Coding

ก่อนเริ่ม Task ใหม่:

1. อ่าน Relevant Documentation
2. ตรวจ Existing Code
3. ตรวจ Database Schema
4. ตรวจ API Contract
5. ตรวจ Dependency
6. วาง Implementation Plan
7. จากนั้นจึงแก้ Code

ห้ามสมมติว่า Code ยังไม่มี

ให้ตรวจ Repository ก่อนเสมอ

---

# 19. Do Not Delete Existing Work

ห้ามลบหรือเขียนทับระบบเดิมโดยไม่มีเหตุผล

ก่อน Refactor:

```text
Inspect
 ↓
Explain
 ↓
Plan
 ↓
Modify
```

หากมีวิธีแก้แบบ Minimal Change ให้เลือกวิธีนั้นก่อน

---

# 20. Definition of Good Implementation

Implementation ที่ดีต้อง:

* ตรงกับ Source of Truth
* ทำงานจริง
* Test ได้
* Traceable
* Maintainable
* Secure
* ไม่ Overengineer
* รองรับการขยาย Semester 2

---

# END