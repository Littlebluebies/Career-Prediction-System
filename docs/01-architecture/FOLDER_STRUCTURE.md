# FOLDER_STRUCTURE.md

# Career Prediction and Skill Gap Analysis System

## Project Folder Structure Specification

**Project:** Career Prediction and Skill Gap Analysis System for Mass Communication Technology Students
**Frontend:** Next.js + React + TypeScript + Tailwind CSS
**Backend:** Node.js + Express.js + TypeScript
**AI/NLP:** Python
**Database:** PostgreSQL
**Container:** Docker + Docker Compose
**Version Control:** Git + GitHub

> **แก้ไขโครงสร้าง (Layout Revision):** Application อยู่ใน `apps/web`, `apps/api`, `services/ai` และเอกสารอยู่ใน `docs/00-source-of-truth` ถึง `docs/04-design` ตามการตัดสินใจของเจ้าของโครงการ ดู `docs/decisions/0001-repository-layout.md`

---

# 1. Purpose

เอกสารนี้กำหนดโครงสร้าง Folder และ File ของระบบ เพื่อให้การพัฒนาระบบเป็นไปในทิศทางเดียวกัน

เป้าหมายหลัก:

* แยก Frontend / Backend / AI / Database อย่างชัดเจน
* ลดการเขียน Code ซ้ำ
* ลดการเชื่อมต่อผิด Layer
* รองรับการพัฒนาเป็นทีม
* รองรับ Docker
* รองรับการทดสอบ
* รองรับการขยายระบบใน Semester 2
* ทำให้ Claude สามารถสร้าง Code ตาม Architecture ที่กำหนดได้

---

# 2. Architecture

ระบบใช้ Architecture:

```text
                         USER
                           │
                           ▼
                ┌────────────────────┐
                │      FRONTEND      │
                │      Next.js       │
                │ React + TypeScript │
                │    Tailwind CSS    │
                └─────────┬──────────┘
                          │
                       REST API
                          │
                          ▼
                ┌────────────────────┐
                │      BACKEND       │
                │ Node.js + Express  │
                │    + TypeScript    │
                └──────┬───────┬─────┘
                       │       │
                       │       │ HTTP / JSON
                       │       ▼
                       │ ┌────────────────┐
                       │ │   AI SERVICE   │
                       │ │     Python     │
                       │ └────────────────┘
                       │
                       ▼
                ┌────────────────────┐
                │     PostgreSQL     │
                └────────────────────┘
```

หลักการสำคัญ:

```text
Next.js → Express
Express → PostgreSQL
Express → Python
Python → AI/NLP Processing
```

ห้าม:

```text
Next.js → PostgreSQL
Next.js → Python
Python → Next.js
```

โดยตรง

---

# 3. Root Folder

โครงสร้างระดับ Root:

```text
Career-Prediction-System/
│
├── apps/
│   ├── web/
│   └── api/
│
├── services/
│   └── ai/
│
├── database/
├── datasets/
├── docs/
├── scripts/
├── tests/
│
├── docker-compose.yml
├── .env.example
├── .gitattributes
├── .gitignore
├── CLAUDE.md
└── README.md
```

หน้าที่ของแต่ละ Application:

```text
apps/web      = Frontend (Next.js)
apps/api      = Backend (Express)
services/ai   = AI/NLP Service (Python)
```

Dockerfile ของแต่ละ Service อยู่ในโฟลเดอร์ของ Service นั้น ไม่มีโฟลเดอร์ `docker/` แยก

ไฟล์ LICENSE จะเพิ่มเมื่อเจ้าของโครงการเลือกสัญญาอนุญาต

---

# 4. Frontend

Frontend ใช้:

```text
Next.js
React
TypeScript
Tailwind CSS
```

โครงสร้าง:

```text
apps/web/
│
├── app/
│   ├── page.tsx
│   ├── layout.tsx
│   ├── globals.css
│   │
│   ├── analysis/
│   │   ├── page.tsx
│   │   ├── resume/
│   │   │   └── page.tsx
│   │   ├── portfolio/
│   │   │   └── page.tsx
│   │   ├── consent/
│   │   │   └── page.tsx
│   │   └── processing/
│   │       └── page.tsx
│   │
│   ├── results/
│   │   ├── page.tsx
│   │   ├── career/
│   │   │   └── [resultId]/
│   │   │       └── page.tsx
│   │   └── skill-gap/
│   │       └── [resultId]/
│   │           └── page.tsx
│   │
│   └── feedback/
│       └── page.tsx
│
├── components/
│   ├── ui/
│   ├── form/
│   ├── analysis/
│   ├── career/
│   ├── skill/
│   ├── feedback/
│   └── layout/
│
├── lib/
│   ├── api/
│   ├── validation/
│   ├── utils/
│   └── constants/
│
├── types/
├── hooks/
├── config/
├── public/
│   ├── images/
│   ├── icons/
│   └── assets/
│
├── tests/
├── next.config.ts
├── tailwind.config.ts
├── tsconfig.json
├── package.json
└── README.md
```

ไม่ใช้โฟลเดอร์ `src/` โฟลเดอร์ที่ยังไม่มีใน Scaffold เริ่มต้น (`hooks/`, `config/`, `lib/utils/`, `lib/constants/`) สร้างเมื่อมีโค้ดที่ต้องใช้

---

# 5. Frontend App Pages

## Home

```text
apps/web/app/page.tsx
```

หน้าหลักของระบบ

ประกอบด้วย:

* Hero
* System Introduction
* How It Works
* Features
* Privacy Information
* Start Analysis Button

---

# 6. Analysis Pages

```text
apps/web/app/analysis/
```

ใช้สำหรับ Workflow ก่อนเริ่มวิเคราะห์

```text
analysis/
├── page.tsx
├── resume/
│   └── page.tsx
├── portfolio/
│   └── page.tsx
├── consent/
│   └── page.tsx
└── processing/
    └── page.tsx
```

Flow:

```text
Major
 ↓
Resume
 ↓
Portfolio
 ↓
Consent
 ↓
Processing
```

---

# 7. Results Pages

```text
apps/web/app/results/
```

ใช้สำหรับแสดงผลการวิเคราะห์

```text
results/
├── page.tsx
├── career/
│   └── [resultId]/
│       └── page.tsx
└── skill-gap/
    └── [resultId]/
        └── page.tsx
```

---

# 8. Reusable UI Components

Components ที่ควรมี:

```text
components/
├── ui/
│   ├── Button.tsx
│   ├── Input.tsx
│   ├── Select.tsx
│   ├── Modal.tsx
│   ├── Alert.tsx
│   ├── Toast.tsx
│   ├── LoadingState.tsx
│   └── EmptyState.tsx
│
├── form/
│   ├── MajorSelector.tsx
│   ├── ResumeUploader.tsx
│   ├── PortfolioUrlInput.tsx
│   └── ConsentForm.tsx
│
├── analysis/
│   ├── ProgressStepper.tsx
│   ├── AnalysisStatus.tsx
│   ├── SkillProfile.tsx
│   └── EvidenceList.tsx
│
├── career/
│   ├── CareerCard.tsx
│   ├── CareerList.tsx
│   ├── CareerExplanation.tsx
│   └── CareerComparison.tsx
│
├── skill/
│   ├── SkillChip.tsx
│   ├── SkillGapCard.tsx
│   └── SkillGapList.tsx
│
├── feedback/
│   └── SUSForm.tsx
│
└── layout/
    ├── Header.tsx
    ├── Footer.tsx
    └── Container.tsx
```

Components ต้องสามารถนำกลับมาใช้ซ้ำได้

ไม่ควรสร้าง Component ซ้ำสำหรับหน้าที่มี UI ลักษณะเดียวกัน

---

# 9. Frontend API Layer

API Client:

```text
apps/web/lib/api/
```

โครงสร้าง:

```text
api/
├── client.ts
├── session.ts
├── resume.ts
├── portfolio.ts
├── analysis.ts
├── career.ts
├── skill-gap.ts
└── feedback.ts
```

หน้าที่:

```text
client.ts
    ↓
HTTP Configuration

session.ts
    ↓
Session API

resume.ts
    ↓
Resume API

portfolio.ts
    ↓
Portfolio API

analysis.ts
    ↓
Analysis API

career.ts
    ↓
Career API

skill-gap.ts
    ↓
Skill Gap API

feedback.ts
    ↓
Feedback API
```

ห้ามกระจาย `fetch()` ไปทั่ว Component

---

# 10. Frontend Types

```text
apps/web/types/
```

ตัวอย่าง:

```text
session.ts
resume.ts
portfolio.ts
skill.ts
career.ts
skill-gap.ts
feedback.ts
api.ts
```

ตัวอย่าง:

```ts
export interface CareerResult {
  resultId: number;
  occupationName: string;
  score: number;
  rank: number;
  matchedSkills: string[];
  explanation: string;
}
```

Type ต้องสอดคล้องกับ API Contract

---

# 11. Frontend Validation

```text
apps/web/lib/validation/
```

ใช้สำหรับ:

* Form Validation
* URL Validation
* File Validation เบื้องต้น
* Input Validation

แต่ Backend ต้อง Validate ซ้ำเสมอ

Frontend Validation ไม่ถือเป็น Security Boundary

---

# 12. Backend

Backend ใช้:

```text
Node.js
Express.js
TypeScript
```

โครงสร้าง:

```text
apps/api/
│
├── src/
│   │
│   ├── app.ts
│   ├── server.ts
│   │
│   ├── routes/
│   │   ├── session.routes.ts
│   │   ├── resume.routes.ts
│   │   ├── portfolio.routes.ts
│   │   ├── consent.routes.ts
│   │   ├── analysis.routes.ts
│   │   ├── career.routes.ts
│   │   ├── skill-gap.routes.ts
│   │   └── feedback.routes.ts
│   │
│   ├── controllers/
│   │   ├── session.controller.ts
│   │   ├── resume.controller.ts
│   │   ├── portfolio.controller.ts
│   │   ├── consent.controller.ts
│   │   ├── analysis.controller.ts
│   │   ├── career.controller.ts
│   │   ├── skill-gap.controller.ts
│   │   └── feedback.controller.ts
│   │
│   ├── services/
│   │   ├── session.service.ts
│   │   ├── resume.service.ts
│   │   ├── portfolio.service.ts
│   │   ├── analysis.service.ts
│   │   ├── career.service.ts
│   │   ├── skill-gap.service.ts
│   │   └── feedback.service.ts
│   │
│   ├── repositories/
│   │   ├── session.repository.ts
│   │   ├── resume.repository.ts
│   │   ├── portfolio.repository.ts
│   │   ├── skill.repository.ts
│   │   ├── occupation.repository.ts
│   │   ├── career.repository.ts
│   │   ├── skill-gap.repository.ts
│   │   └── feedback.repository.ts
│   │
│   ├── clients/
│   │   └── python.client.ts
│   │
│   ├── validators/
│   │   ├── session.validator.ts
│   │   ├── resume.validator.ts
│   │   ├── portfolio.validator.ts
│   │   ├── analysis.validator.ts
│   │   └── feedback.validator.ts
│   │
│   ├── middlewares/
│   │   ├── error.middleware.ts
│   │   ├── request-id.middleware.ts
│   │   ├── rate-limit.middleware.ts
│   │   └── upload.middleware.ts
│   │
│   ├── config/
│   │   ├── env.ts
│   │   ├── database.ts
│   │   └── ai.ts
│   │
│   ├── types/
│   ├── utils/
│   └── constants/
│
├── tests/
├── package.json
├── tsconfig.json
└── README.md
```

`utils/` และ `constants/` สร้างเมื่อมีโค้ดที่ต้องใช้ ชื่อไฟล์ TypeScript ใช้ kebab-case ตาม §39

---

# 13. Backend Layer Responsibilities

## Routes

รับ HTTP Request

```text
Route
 ↓
Controller
```

ไม่ควรใส่ Business Logic จำนวนมากใน Route

---

## Controllers

รับ:

```text
Request
```

ส่ง:

```text
Response
```

หน้าที่หลัก:

* Parse Request
* เรียก Service
* ส่ง HTTP Response

ไม่ควรเขียน SQL โดยตรง

---

## Services

เป็น Business Logic Layer

ตัวอย่าง:

```text
analysis.service.ts
```

รับผิดชอบ:

```text
Validate Analysis State
 ↓
Call Resume Processing
 ↓
Call Portfolio Processing
 ↓
Call Python
 ↓
Build Candidate Profile
 ↓
Match Careers
 ↓
Generate Skill Gap
 ↓
Save Result
```

---

## Repositories

รับผิดชอบ Database Access

ตัวอย่าง:

```text
career.repository.ts
```

ทำ:

```text
SELECT
INSERT
UPDATE
DELETE
```

กับ PostgreSQL

Service ไม่ควรเขียน SQL กระจายเอง

---

# 14. Python AI Service

โครงสร้าง:

```text
services/ai/
│
├── app/
│   │
│   ├── main.py
│   │
│   ├── api/
│   │   └── analyze.py
│   │
│   ├── services/
│   ├── pipelines/
│   │
│   ├── extractors/
│   │   ├── resume_parser.py
│   │   ├── portfolio_analyzer.py
│   │   ├── skill_extractor.py
│   │   └── evidence_analyzer.py
│   │
│   ├── normalizers/
│   │   ├── text_cleaner.py
│   │   ├── skill_normalizer.py
│   │   └── occupation_normalizer.py
│   │
│   ├── matching/
│   │   ├── matching_engine.py
│   │   ├── ranking_engine.py
│   │   ├── explanation_engine.py
│   │   ├── skill_gap_engine.py
│   │   └── guidance_engine.py
│   │
│   ├── models/
│   │   ├── skill.py
│   │   ├── evidence.py
│   │   └── analysis.py
│   │
│   └── schemas/
│       ├── analyze_request.py
│       └── analyze_response.py
│
├── tests/
├── requirements.txt
└── README.md
```

`config/`, `utils/` และ `evaluation/` ไม่อยู่ใน Scaffold เริ่มต้น เพิ่มเมื่อมีโค้ดที่ต้องใช้ (`evaluation/` ใช้ใน Phase 12) Web framework คือ FastAPI + Uvicorn ดู `docs/decisions/0004-ai-service.md`

---

# 15. Python Module Responsibilities

โมดูลเชิง Logic ใน `AI_MATCHING_SPEC.md` §85 ถูกจัดลงโฟลเดอร์ดังนี้

## api

รับ Request จาก Express (`POST /internal/analyze`, `GET /health`) แล้วเรียก `services/`

ไม่มี Logic การวิเคราะห์ใน Endpoint

---

## services

ประสานงานหนึ่ง Analysis Request

รวมถึง Candidate Profile, Occupation Profile และ Market Analyzer (ชั่วคราว จนกว่าจะกำหนด Contract ของ Matching ดู `docs/decisions/README.md`)

---

## pipelines

กำหนดลำดับขั้นตอน:

```text
Parse
 ↓
Clean
 ↓
Extract
 ↓
Normalize
 ↓
Candidate Profile
 ↓
Match
 ↓
Skill Gap
 ↓
Guidance
```

---

## extractors

อ่านข้อมูลจาก:

```text
Resume
Portfolio
```

แล้วสกัด:

```text
Skill Detection
Skill Extraction
Evidence Extraction
```

---

## normalizers

ทำ:

```text
Text Cleaning
Text Normalization
Whitespace Cleaning
Encoding Handling
Skill Normalization
Occupation Normalization
```

ตัวอย่าง Skill Normalization:

```text
React.js
ReactJS
React
```

ให้เป็น:

```text
React
```

---

## matching

รับ:

```text
Candidate Skill Profile
+
Occupation Skill Profile
+
Labour Market Signal
```

แล้วสร้าง Matching Result ตาม Algorithm ที่กำหนดไว้ใน `AI_MATCHING_SPEC.md`

ประกอบด้วย Matching, Ranking, Explanation, Skill Gap และ Guidance

Semantic Similarity (Embedding) ใช้เมื่อจำเป็นและเหมาะสมกับ methodology ไม่จำเป็นต้องใช้ Embedding ทุกจุดของระบบ

---

## models

Domain Data Class เช่น Skill, Evidence, Analysis

---

## schemas

Request และ Response Schema ของ Internal API ตาม `API.md` §35-37

---

# 16. Database

โครงสร้าง:

```text
database/
│
├── migrations/
│   ├── 001_create_schema.sql
│   ├── 002_create_major.sql
│   └── ...                   (001-021 ตาม DATABASE_MIGRATION_PLAN.md §5)
│
├── seed/
│   ├── development/          (DEMO / TEST DATA)
│   ├── reference/            (ข้อมูลอ้างอิงที่ตรวจสอบแล้ว)
│   └── README.md
│
├── schema/
│   └── README.md
│
└── README.md
```

---

# 17. Migration Rules

Database Schema ต้องเปลี่ยนผ่าน Migration

ตัวอย่าง:

```text
001_create_schema.sql
002_create_major.sql
021_create_indexes.sql
```

ห้ามแก้ Production Database โดยการแก้ Schema แบบไม่มี Migration

ทุก Schema Change ต้องสามารถ Trace ได้

---

# 18. Seed Data

Seed Data ใช้สำหรับ:

```text
Development
Testing
Demo
Initial System Setup
```

ตัวอย่าง:

```text
seed/development/major.seed.sql
seed/development/skill.seed.sql
seed/development/occupation.seed.sql
```

ข้อมูลใน `seed/development/` ต้องระบุว่าเป็น DEMO / TEST DATA ส่วน `seed/reference/` ใช้เมื่อข้อมูลผ่านการตรวจสอบแล้ว

Seed Data ห้ามถูกนำเสนอเป็น Labour Market Dataset จริง หากยังไม่ได้ผ่านกระบวนการเก็บและตรวจสอบข้อมูล

---

# 19. Dataset Folder

ข้อมูล Dataset:

```text
datasets/
│
├── raw/
├── processed/
├── evaluation/
├── metadata/
│
└── README.md
```

เมื่อเริ่มมีข้อมูล ให้แบ่งโฟลเดอร์ย่อยตามชนิด เช่น `occupation/`, `skill/`, `job_posting/`, `occupation_skill/` (ตาม `DATASET_SPEC.md` §54)

---

# 20. Raw Dataset

```text
datasets/raw/
```

เก็บข้อมูลต้นฉบับ

ตัวอย่าง:

```text
raw/
└── job_posting/
    ├── source-a/
    ├── source-b/
    └── source-c/
```

ห้ามแก้ข้อมูลต้นฉบับโดยตรง

---

# 21. Processed Dataset

```text
datasets/processed/
```

เก็บข้อมูลหลัง:

```text
Cleaning
Deduplication
Normalization
Skill Extraction
Occupation Mapping
```

---

# 22. Evaluation Dataset

```text
datasets/evaluation/
```

ใช้สำหรับ:

```text
Skill Extraction Evaluation
Career Recommendation Evaluation
Ground Truth
Testing
```

ข้อมูล Ground Truth ต้องมีที่มาชัดเจน

---

# 23. Dataset Metadata

```text
datasets/metadata/
```

เก็บ:

```text
dataset_name
version
source
collection_date
coverage
description
number_of_records
processing_method
```

ฟิลด์ข้างบนเป็นฟิลด์บังคับตาม `DATASET_SPEC.md` §32 ฟิลด์เสริมคือ `sampling_period`, `processing_version`, `schema_version`, `notes`

บันทึก 1 ไฟล์ต่อ 1 Dataset Version เป็น JSON ชื่อ `<dataset_name>_<version>.json` ดู `docs/decisions/0006-dataset-metadata.md`

---

# 24. Scripts

```text
scripts/
```

ใช้สำหรับ Automation เช่น:

```text
scripts/
├── database/
│   ├── migrate.sh
│   ├── seed.sh
│   └── reset.sh
│
├── dataset/
│   ├── validate.py
│   ├── clean.py
│   ├── normalize.py
│   └── import.py
│
└── development/
    └── setup.sh
```

Scripts ต้องมี README หรือ Comment อธิบายการใช้งานที่สำคัญ

---

# 25. Documentation

```text
docs/
```

เก็บเอกสาร Project Specification

```text
docs/
├── 00-source-of-truth/
│   ├── PROJECT_SPEC.md
│   ├── TECH_STACK.md
│   └── IMPLEMENTATION_PLAN.md
├── 01-architecture/
│   ├── FOLDER_STRUCTURE.md
│   ├── API.md
│   └── ENVIRONMENT_SETUP.md
├── 02-database/
│   ├── DATABASE.md
│   └── DATABASE_MIGRATION_PLAN.md
├── 03-ai-data/
│   ├── DATASET_SPEC.md
│   └── AI_MATCHING_SPEC.md
├── 04-design/
│   └── UI_UX_SPEC.md
└── decisions/
    └── README.md
```

ไฟล์เหล่านี้เป็น Source of Truth สำหรับการพัฒนา `CLAUDE.md` อยู่ที่ Root ส่วน `docs/decisions/` บันทึกการตัดสินใจทางเทคนิคที่เอกสารข้างบนเปิดให้เลือกภายหลัง

---

# 26. Testing Structure

```text
tests/
├── integration/
├── e2e/
└── fixtures/
```

นอกจากนี้แต่ละ Application สามารถมี Unit Tests ของตัวเอง:

```text
apps/web/tests/
apps/api/tests/
services/ai/tests/
```

---

# 27. Test Levels

ระบบต้องรองรับ:

```text
Unit Test
     ↓
Integration Test
     ↓
End-to-End Test
     ↓
System Test
     ↓
User Evaluation
```

---

# 28. Unit Tests

ทดสอบ Logic แต่ละส่วน

ตัวอย่าง:

```text
Skill Normalization
URL Validation
Score Calculation
Skill Gap Classification
API Validation
```

---

# 29. Integration Tests

ทดสอบ:

```text
Express
 ↓
PostgreSQL
```

และ:

```text
Express
 ↓
Python
```

---

# 30. End-to-End Tests

ทดสอบ Workflow จริง:

```text
Open Website
 ↓
Select Major
 ↓
Upload Resume
 ↓
Add Portfolio
 ↓
Consent
 ↓
Analyze
 ↓
View Career Results
 ↓
View Skill Gap
 ↓
Submit Feedback
```

---

# 31. Docker

Root:

```text
docker-compose.yml
```

สามารถประกอบด้วย Services:

```text
services:
  frontend
  backend
  ai-service
  postgres
```

Build context ของแต่ละ Service:

```text
frontend    -> ./apps/web
backend     -> ./apps/api
ai-service  -> ./services/ai
```

ชื่อ Service คงเดิม เพราะ `AI_SERVICE_URL=http://ai-service:8000` ใช้ชื่อ Service เป็น Hostname

Architecture:

```text
┌──────────────┐
│   frontend   │
│   Next.js    │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   backend    │
│   Express    │
└───┬──────┬───┘
    │      │
    │      ▼
    │  ┌──────────────┐
    │  │  ai-service  │
    │  │    Python    │
    │  └──────────────┘
    │
    ▼
┌──────────────┐
│  PostgreSQL  │
└──────────────┘
```

---

# 32. Docker Network

Services ควรสื่อสารผ่าน Docker Network

ตัวอย่าง:

```text
frontend
   ↓
backend:4000

backend
   ↓
ai-service:8000

backend
   ↓
postgres:5432
```

Frontend ไม่ควรเข้าถึง PostgreSQL Container โดยตรง

---

# 33. Environment Variables

Root:

```text
.env.example
```

ตัวอย่าง:

```env
NODE_ENV=development

DATABASE_URL=postgresql://...

AI_SERVICE_URL=http://ai-service:8000

NEXT_PUBLIC_API_BASE_URL=http://localhost:4000/api

SESSION_TTL_MINUTES=60

MAX_RESUME_SIZE_MB=10
```

ห้าม Commit `.env`

ต้องใช้:

```text
.env
```

ใน Local Environment

และ:

```text
.env.example
```

สำหรับตัวอย่าง Configuration เท่านั้น

---

# 34. Git Ignore

`.gitignore` ต้องไม่ Commit:

```text
.env
.env.local
node_modules/
__pycache__/
*.pyc
.next/
dist/
build/
uploads/
temporary/
logs/
```

รวมถึงไฟล์ Resume หรือ Portfolio ของ User

---

# 35. Temporary Storage

ไม่ควรเก็บ Resume ของ User ใน Git Repository

Temporary Storage ตัวอย่าง:

```text
storage/
└── temporary/
```

แต่ Folder นี้ต้อง:

```text
.gitignore
```

และต้องมี Cleanup Process

---

# 36. User Data Flow

```text
Resume
   ↓
Temporary Storage
   ↓
Text Extraction
   ↓
Skill Extraction
   ↓
Evidence
   ↓
Database
   ↓
Result
   ↓
Retention Period
   ↓
Delete
```

ไม่ควรเก็บ Resume ถาวรโดยไม่มีเหตุผล

---

# 37. Knowledge Data Flow

ข้อมูลระบบ:

```text
Occupation
Skill
Career Family
Occupation Skill
```

เป็น Knowledge Data

ไม่ควรถูกลบเมื่อ User Session หมดอายุ

---

# 38. Labour Market Data Flow

```text
Job Posting
      ↓
Raw Dataset
      ↓
Cleaning
      ↓
Deduplication
      ↓
Skill Extraction
      ↓
Skill Normalization
      ↓
Occupation Mapping
      ↓
Occupation Skill Profile
      ↓
Database
```

---

# 39. File Naming Convention

TypeScript:

```text
kebab-case
```

ตัวอย่าง:

```text
skill-gap.service.ts
career-result.repository.ts
```

React Component:

```text
PascalCase
```

ตัวอย่าง:

```text
CareerCard.tsx
SkillGapCard.tsx
ResumeUploader.tsx
```

Python:

```text
snake_case
```

ตัวอย่าง:

```text
skill_extractor.py
resume_parser.py
```

SQL Migration:

```text
NNN_description.sql
```

ตัวอย่าง:

```text
001_create_schema.sql
002_create_major.sql
```

---

# 40. Naming Convention

Database:

```text
snake_case
```

ตัวอย่าง:

```text
session_id
occupation_id
skill_id
created_at
```

TypeScript Variables:

```text
camelCase
```

ตัวอย่าง:

```ts
sessionId
occupationId
skillId
```

React Components:

```text
PascalCase
```

---

# 41. Separation of Concerns

ห้าม:

```text
React Component
 ↓
SQL Query
```

ห้าม:

```text
Controller
 ↓
Large AI Algorithm
```

ห้าม:

```text
Python Parser
 ↓
Frontend UI
```

ควรเป็น:

```text
Component
 ↓
API Client
 ↓
Express Route
 ↓
Controller
 ↓
Service
 ↓
Repository
 ↓
PostgreSQL
```

และ AI:

```text
Service
 ↓
Python Client
 ↓
Python AI Service
```

---

# 42. Career Matching Location

Career Matching Logic ต้องไม่กระจายหลายที่

แนะนำ:

```text
apps/api/src/services/
```

สำหรับ Orchestration

และ:

```text
services/ai/app/matching/
```

สำหรับ AI/NLP/Matching Algorithm ที่เป็น Python

ต้องกำหนด Responsibility ให้ชัดเจน

ตัวอย่าง:

```text
Express
→ เรียก Matching Process
→ จัดการ Transaction
→ บันทึก Result

Python
→ NLP
→ Similarity
→ Skill Processing
→ Algorithmic AI Processing
```

---

# 43. Configuration

Configuration ที่เปลี่ยนได้ควรอยู่ใน:

```text
apps/api/src/config/
services/ai/app/config/
apps/web/config/
```

ไม่ควร Hard-code:

```text
API URL
Database URL
AI Service URL
File Size
Session TTL
Algorithm Version
Dataset Version
```

---

# 44. Algorithm Configuration

ตัวอย่าง:

```env
ALGORITHM_VERSION=career-matching-v1
```

แต่ Weight ของ Matching ต้องไม่ถูกกำหนดแบบสุ่ม

ตัวจริงต้องมาจาก:

```text
Research
Dataset
Methodology
Evaluation
```

---

# 45. Dataset Version Configuration

ตัวอย่าง:

```env
DATASET_VERSION=2026-01
```

ค่าใช้งานจริงต้องสอดคล้องกับ Dataset ที่มีอยู่จริง

ห้ามระบุ Version ที่ไม่มีอยู่

---

# 46. Semester 1 Structure

Semester 1 เน้น Pilot:

```text
Creative Media Technology
        ↓
Web Full Stack
```

แต่ Folder Structure ต้องไม่สร้างระบบเฉพาะ Web Full Stack แบบ Hard-coded

ต้องออกแบบให้:

```text
Major
 ↓
Occupation
 ↓
Skill
```

สามารถเพิ่มสาขาอื่นภายหลังได้

---

# 47. Semester 2 Expansion

Semester 2 เพิ่ม:

```text
Film & Television
Advertising & Public Relations
Digital Printing & Packaging
Creative Media Technology
```

และ:

```text
Creative Media Technology
├── Web Full Stack
└── Game Development
```

ไม่ควรสร้าง:

```text
web-backend/
game-backend/
film-backend/
```

แยกกันโดยไม่จำเป็น

ใช้ Core Backend เดียว

---

# 48. Shared Domain Structure

ระบบควรใช้ Domain Model กลาง:

```text
Major
Career Family
Occupation
Skill
Job Posting
Candidate Profile
Evidence
Career Result
Skill Gap
Feedback
```

ดังนั้นการเพิ่ม Major ใหม่ไม่ควรต้องสร้างระบบใหม่

---

# 49. Documentation Rule

เมื่อแก้ Architecture ต้องตรวจสอบ:

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

เพื่อไม่ให้เอกสารขัดแย้งกัน

---

# 50. Claude Implementation Rules

ก่อนสร้าง Code ให้ Claude:

```text
1. อ่าน PROJECT_SPEC.md
2. อ่าน DATABASE.md
3. อ่าน DATASET_SPEC.md
4. อ่าน AI_MATCHING_SPEC.md
5. อ่าน UI_UX_SPEC.md
6. อ่าน TECH_STACK.md
7. อ่าน IMPLEMENTATION_PLAN.md
8. อ่าน API.md
9. อ่าน FOLDER_STRUCTURE.md
10. อ่าน ENVIRONMENT_SETUP.md
11. อ่าน DATABASE_MIGRATION_PLAN.md
```

จากนั้น:

```text
สร้าง Project Structure
        ↓
ตรวจสอบ Dependency
        ↓
สร้าง Docker
        ↓
สร้าง Database Migration
        ↓
สร้าง Backend Skeleton
        ↓
สร้าง AI Service Skeleton
        ↓
สร้าง Frontend Skeleton
```

ห้ามสร้าง Feature ทั้งหมดพร้อมกันในครั้งเดียว

---

# 51. Recommended Development Order

ลำดับการสร้าง Project:

```text
Phase 0   Project Setup
Phase 1   Database
Phase 2   Reference Data
Phase 3   Labour Market Dataset
Phase 4   Resume Processing
Phase 5   Portfolio Processing
Phase 6   Skill & Evidence Pipeline
Phase 7   Career Matching
Phase 8   Skill Gap & Guidance
Phase 9   Backend API
Phase 10  Frontend
Phase 11  Integration & Testing
Phase 12  Evaluation
Phase 13  Deployment
```

เลข Phase นี้ตรงกับ `CLAUDE.md` §8 และ `IMPLEMENTATION_PLAN.md` §3 และเป็นเลขเดียวที่ใช้ทั้งโครงการ ดู `docs/decisions/0002-phase-numbering-and-semester-1-scope.md`

---

# 52. First Vertical Slice

ไม่ควรสร้างระบบทั้งหมดก่อน

ให้เริ่มจาก Vertical Slice ขนาดเล็ก:

```text
Major Selection
      ↓
Create Session
      ↓
Upload Resume
      ↓
Extract Basic Text
      ↓
Extract Basic Skills
      ↓
Normalize Skills
      ↓
Save User Skills
      ↓
Return Candidate Skill Profile
```

เมื่อ Vertical Slice นี้ทำงานครบ:

```text
Frontend
   ↕
Express
   ↕
PostgreSQL
   ↕
Python
```

จึงขยายไป Portfolio และ Career Matching จนครบ Semester 1 MVP ตาม `IMPLEMENTATION_PLAN.md` §75 และ §80

---

# 53. Definition of Done — Project Structure

โครงสร้าง Project ถือว่าพร้อมเริ่ม Development เมื่อ:

* [ ] Root Folder ถูกสร้าง
* [ ] Frontend Folder ถูกสร้าง
* [ ] Backend Folder ถูกสร้าง
* [ ] AI Service Folder ถูกสร้าง
* [ ] Database Folder ถูกสร้าง
* [ ] Dataset Folder ถูกสร้าง
* [ ] Docs Folder ถูกสร้าง
* [ ] Scripts Folder ถูกสร้าง
* [ ] Tests Folder ถูกสร้าง
* [ ] Docker Compose ถูกเตรียม
* [ ] Environment Template ถูกเตรียม
* [ ] Git Ignore ถูกเตรียม
* [ ] Frontend Layer แยกจาก Backend
* [ ] Backend Layer แยกจาก AI
* [ ] Repository Layer แยกจาก Service
* [ ] Database Migration แยกจาก Seed
* [ ] Raw Dataset แยกจาก Processed Dataset
* [ ] Evaluation Dataset แยกออกจาก Production Dataset
* [ ] Temporary User Data ไม่อยู่ใน Git
* [ ] Documentation ถูกเก็บใน docs/
* [ ] Naming Convention ถูกกำหนด
* [ ] First Vertical Slice ถูกกำหนด

---

# 54. Final Folder Tree

โครงสร้างภาพรวมสุดท้าย:

```text
Career-Prediction-System/
│
├── apps/
│   ├── web/
│   │   ├── app/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── lib/
│   │   ├── types/
│   │   ├── config/
│   │   ├── public/
│   │   ├── tests/
│   │   ├── package.json
│   │   └── README.md
│   │
│   └── api/
│       ├── src/
│       │   ├── routes/
│       │   ├── controllers/
│       │   ├── services/
│       │   ├── repositories/
│       │   ├── clients/
│       │   ├── validators/
│       │   ├── middlewares/
│       │   ├── config/
│       │   ├── types/
│       │   ├── utils/
│       │   └── constants/
│       ├── tests/
│       ├── package.json
│       └── README.md
│
├── services/
│   └── ai/
│       ├── app/
│       │   ├── main.py
│       │   ├── api/
│       │   ├── services/
│       │   ├── pipelines/
│       │   ├── extractors/
│       │   ├── normalizers/
│       │   ├── matching/
│       │   ├── models/
│       │   └── schemas/
│       ├── tests/
│       ├── requirements.txt
│       └── README.md
│
├── database/
│   ├── migrations/
│   ├── seed/
│   │   ├── development/
│   │   ├── reference/
│   │   └── README.md
│   ├── schema/
│   └── README.md
│
├── datasets/
│   ├── raw/
│   ├── processed/
│   ├── evaluation/
│   ├── metadata/
│   └── README.md
│
├── docs/
│   ├── 00-source-of-truth/
│   ├── 01-architecture/
│   ├── 02-database/
│   ├── 03-ai-data/
│   ├── 04-design/
│   └── decisions/
│
├── scripts/
│   ├── database/
│   ├── dataset/
│   └── development/
│
├── tests/
│   ├── integration/
│   ├── e2e/
│   └── fixtures/
│
├── docker-compose.yml
├── .env.example
├── .gitattributes
├── .gitignore
├── CLAUDE.md
└── README.md
```

---

# 55. Final Architecture Rule

ระบบนี้ต้องยึดหลัก:

```text
                     FRONTEND
                       Next.js
                          │
                          │ REST API
                          ▼
                     BACKEND
                   Express + TS
                     │       │
                     │       │ HTTP/JSON
                     │       ▼
                     │   AI SERVICE
                     │     Python
                     │
                     ▼
                   DATABASE
                  PostgreSQL
```

และ:

```text
Frontend
≠
Backend
≠
AI Service
≠
Database
```

แต่ละ Layer มีหน้าที่เฉพาะของตัวเอง

---

# 56. Document Status

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

Technology Stack: LOCKED

Frontend:
Next.js + React + TypeScript + Tailwind CSS

Backend:
Node.js + Express.js + TypeScript

AI/NLP:
Python

Database:
PostgreSQL

Container:
Docker + Docker Compose

Version Control:
Git + GitHub

Architecture:
Frontend → Express → PostgreSQL
Express → Python AI Service

Folder Structure: LOCKED (Revised: apps/web, apps/api, services/ai ดู docs/decisions/0001-repository-layout.md)

Semester 1:
Creative Media Technology → Web Full Stack Pilot

Semester 2:
Whole Faculty Expansion
```

---

# END OF FOLDER_STRUCTURE.md