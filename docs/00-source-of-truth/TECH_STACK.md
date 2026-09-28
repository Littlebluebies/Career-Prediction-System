# TECH_STACK.md

# Career Prediction and Skill Gap Analysis System

## Technology Stack & Technical Architecture Specification

> **Document Status:** LOCKED
> **Purpose:** Technical Single Source of Truth สำหรับการพัฒนาระบบ
> **Related Documents:** `PROJECT_SPEC.md`, `DATABASE.md`, `DATASET_SPEC.md`, `AI_MATCHING_SPEC.md`, `UI_UX_SPEC.md`, `IMPLEMENTATION_PLAN.md`

---

# 1. Document Purpose

เอกสารนี้กำหนด Technology Stack, Software Architecture, Development Tools, Communication Contract และแนวทางการพัฒนาระบบสำหรับ

> **ระบบทำนายอาชีพสำหรับนักศึกษาคณะเทคโนโลยีสื่อสารมวลชนโดยอิงการวิเคราะห์ทักษะและความต้องการของตลาดแรงงาน**

ระบบใช้การวิเคราะห์ข้อมูลจาก

* Resume
* Portfolio
* Skills
* Occupations
* Labour Market / Job Postings

เพื่อสร้าง

* Candidate Skill Profile
* Career Recommendation
* Explainable Career Recommendation
* Skill Gap Analysis
* Development Guidance

ระบบไม่ได้ทำนายว่า User จะได้งานหรือประกอบอาชีพนั้นแน่นอน แต่เป็นการประเมิน **Career Compatibility / Match Score**

---

# 2. Technology Stack Overview

ระบบใช้ Technology Stack ดังนี้

| Layer             | Technology                        | Role                            |
| ----------------- | --------------------------------- | ------------------------------- |
| Frontend          | Next.js                           | Web Application                 |
| UI                | React                             | Component-based UI              |
| Language          | TypeScript                        | Type Safety                     |
| Styling           | Tailwind CSS                      | UI Styling                      |
| Backend           | Node.js                           | Backend Runtime                 |
| API               | Express.js                        | REST API                        |
| Backend Language  | TypeScript                        | Business Logic                  |
| AI/NLP            | Python                            | AI/NLP/Data Processing          |
| Database          | PostgreSQL                        | Relational Database             |
| Container         | Docker                            | Environment Isolation           |
| Orchestration     | Docker Compose                    | Local Multi-service Environment |
| Version Control   | Git                               | Source Control                  |
| Repository        | GitHub                            | Code Repository                 |
| Testing           | TypeScript / Python Testing Tools | Automated Testing               |
| API Communication | REST / JSON                       | Service Communication           |

---

# 3. Architecture

ระบบใช้ **Service-Oriented Web Architecture**

```text
┌──────────────────────────────┐
│            USER              │
│ Resume + Portfolio + Major   │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│          NEXT.JS             │
│     React + TypeScript       │
│       Tailwind CSS           │
│                              │
│          Frontend            │
└──────────────┬───────────────┘
               │ REST / JSON
               ▼
┌──────────────────────────────┐
│       EXPRESS.JS API         │
│      Node.js + TypeScript    │
│                              │
│ • API                        │
│ • Validation                 │
│ • Business Logic             │
│ • Session Management         │
│ • Orchestration              │
│ • Database Access            │
└───────┬──────────────┬───────┘
        │              │
        │              │ HTTP/JSON
        │              ▼
        │     ┌─────────────────────┐
        │     │    PYTHON AI/NLP    │
        │     │                     │
        │     │ • Resume Parsing    │
        │     │ • NLP               │
        │     │ • Skill Extraction  │
        │     │ • Normalization     │
        │     │ • Embedding         │
        │     │ • Matching          │
        │     │ • Evaluation        │
        │     └─────────────────────┘
        │
        ▼
┌──────────────────────────────┐
│         POSTGRESQL           │
│                              │
│ • User Session               │
│ • Resume                     │
│ • Portfolio                  │
│ • Skills                     │
│ • Occupations                │
│ • Job Postings               │
│ • Matching Results            │
│ • Skill Gap                  │
│ • Feedback                   │
└──────────────────────────────┘

        Docker Compose
              │
      ┌───────┴────────┐
      │                │
      ▼                ▼
 PostgreSQL       Application
 Container         Services
```

---

# 4. Responsibility of Each Technology

## 4.1 Next.js

Next.js เป็น Frontend Framework หลัก

หน้าที่:

* Render Web Application
* Routing
* Page Management
* React Components
* Form UI
* File Upload UI
* Portfolio URL Input
* Loading / Processing State
* Career Results
* Skill Gap Visualization
* Feedback Form
* Responsive UI

Next.js ต้องไม่ทำหน้าที่เป็น Main Backend API ของระบบ

Frontend จะเรียก Express API ผ่าน HTTP

```text
Next.js
   ↓
REST API
   ↓
Express.js
```

---

# 5. React

React ใช้สำหรับสร้าง UI Components

ตัวอย่าง Components:

```text
Button
Input
Select
UploadBox
URLInput
ProgressStepper
SkillChip
EvidenceCard
CareerCard
SkillGapCard
GuidanceCard
Alert
Toast
Modal
LoadingState
EmptyState
```

หลักการ:

* Components ต้อง Reusable
* ไม่ใส่ Business Logic สำคัญไว้ใน UI
* ไม่คำนวณ Career Score ที่ Frontend
* ไม่เข้าถึง PostgreSQL โดยตรง

---

# 6. TypeScript

TypeScript ใช้เป็นภาษาหลักของ

* Next.js
* Express.js
* Backend Services

เหตุผล:

* Type Safety
* ลด Runtime Error
* ทำ API Contract ได้ชัดเจน
* เหมาะกับระบบที่มี Data Model จำนวนมาก
* ช่วยให้ Frontend และ Backend ใช้โครงสร้างข้อมูลที่สอดคล้องกัน

ควรกำหนด Type สำหรับข้อมูลสำคัญ เช่น

```text
Session
Resume
Portfolio
Skill
Evidence
Occupation
CareerResult
SkillGap
Feedback
```

---

# 7. Tailwind CSS

Tailwind CSS ใช้สำหรับ UI Styling

หลักการ:

* Responsive First
* Reusable Components
* Consistent Spacing
* Consistent Typography
* Accessible Contrast
* ไม่กระจาย CSS แบบไม่มีโครงสร้าง

หากมี Design Token ของระบบ ให้กำหนดเป็นส่วนกลางแทนการใส่ค่าซ้ำในหลาย Component

---

# 8. Node.js

Node.js เป็น Runtime ของ Backend

หน้าที่:

* Run Express.js
* รับ Request จาก Frontend
* Validate Input
* เรียก Python AI Service
* ติดต่อ PostgreSQL
* จัดการ Session
* จัดการ Business Logic
* ส่งผลลัพธ์กลับ Frontend

Node.js ไม่ควรรับผิดชอบ NLP ที่ซับซ้อน

---

# 9. Express.js

Express.js เป็น Main REST API Framework

ตัวอย่าง API Structure:

```text
/api/session
/api/resume
/api/portfolio
/api/analyze
/api/analysis/:session_id
/api/career/:result_id
/api/skill-gap/:result_id
/api/feedback
```

Actual routes สามารถปรับได้ตาม Implementation แต่ต้องไม่ขัดกับ `PROJECT_SPEC.md`

---

# 10. Backend Architecture

Express Backend ใช้ Layered Architecture

```text
Request
   ↓
Route
   ↓
Controller
   ↓
Service
   ↓
Repository
   ↓
PostgreSQL
```

ตัวอย่าง:

```text
POST /api/analyze
        ↓
AnalyzeController
        ↓
AnalysisService
        ↓
PythonAIService
        ↓
Repository
        ↓
PostgreSQL
```

---

# 11. Backend Layers

## 11.1 Route

กำหนด Endpoint

```text
POST /api/analyze
GET /api/analysis/:session_id
```

ไม่ควรใส่ Business Logic ขนาดใหญ่ใน Route

---

## 11.2 Controller

หน้าที่:

* รับ Request
* ตรวจสอบ Input เบื้องต้น
* เรียก Service
* ส่ง HTTP Response

---

## 11.3 Service

เป็น Business Logic Layer

ตัวอย่าง:

```text
AnalysisService
CareerMatchingService
SkillGapService
PortfolioService
ResumeService
FeedbackService
```

---

## 11.4 Repository

รับผิดชอบ Database Access

ตัวอย่าง:

```text
SessionRepository
ResumeRepository
PortfolioRepository
SkillRepository
OccupationRepository
JobPostingRepository
CareerResultRepository
SkillGapRepository
FeedbackRepository
```

Repository ต้องใช้ Parameterized Query หรือ ORM/Query Builder ที่ป้องกัน SQL Injection

---

# 12. Python AI/NLP Service

Python เป็น AI/NLP Service แยกจาก Express

หน้าที่หลัก:

```text
Resume Parsing
Portfolio Text Processing
Skill Extraction
Skill Normalization
Evidence Analysis
Semantic Similarity
Embedding
Career Matching
Skill Gap Calculation
Evaluation
```

Python ไม่ควรเป็น Main Web Backend

Web framework ของ Python Service คือ FastAPI + Uvicorn ดู `docs/decisions/0004-ai-service.md`

---

# 13. Python Service Communication

Express และ Python ติดต่อกันผ่าน Internal HTTP API หรือ Service Interface ที่กำหนดอย่างชัดเจน

ตัวอย่าง:

```text
Express
   │
   │ POST /internal/analyze
   ▼
Python AI Service
   │
   │ JSON Result
   ▼
Express
```

ตัวอย่าง Input:

```json
{
  "session_id": "uuid",
  "resume_text": "Resume extracted text...",
  "portfolio_projects": []
}
```

ตัวอย่าง Output:

```json
{
  "skills": [
    {
      "name": "React",
      "confidence": 0.92,
      "evidence": [
        {
          "source_type": "RESUME_PROJECT",
          "evidence_text": "Developed web application using React"
        }
      ]
    }
  ]
}
```

Endpoint และโครงสร้าง Request/Response ต้องตรงกับ `API.md` §35-37 และสอดคล้องกับ `AI_MATCHING_SPEC.md`

---

# 14. Python AI/NLP Design Principle

AI Service ต้องแยกเป็น Module

ตัวอย่าง:

```text
services/ai/
├── app/
│   ├── main.py
│   ├── api/
│   ├── services/
│   ├── pipelines/
│   ├── extractors/
│   ├── normalizers/
│   ├── matching/
│   ├── models/
│   └── schemas/
│
├── tests/
├── requirements.txt
└── README.md
```

โครงสร้างนี้เป็นชุดเดียวกับ §42 และ `FOLDER_STRUCTURE.md` §14

ไม่ควรสร้าง Python ไฟล์เดียวที่มี Logic ทั้งหมด

---

# 15. PostgreSQL

PostgreSQL เป็น Main Database ของระบบ

ใช้สำหรับข้อมูลเชิงโครงสร้าง เช่น

```text
Major
Session
Resume
Portfolio
Project
Skill
Skill Alias
User Skill
Skill Evidence
Career Family
Occupation
Occupation Alias
Occupation Skill
Job Posting
Job Posting Skill
Dataset Version
Career Result
Skill Gap
User Feedback
```

รายละเอียด Database Schema อยู่ใน

`DATABASE.md`

---

# 16. Database Access Rule

Architecture:

```text
Next.js
   ↓
Express
   ↓
Repository
   ↓
PostgreSQL
```

ห้าม:

```text
Next.js
   ↓
PostgreSQL
```

และไม่ควรให้ Python Service เข้าถึง Database โดยตรงเป็นหลัก

Preferred:

```text
Express
   ↓
Python AI Service
   ↓
AI Result
   ↓
Express
   ↓
PostgreSQL
```

เหตุผลคือให้ Backend เป็นศูนย์กลางในการควบคุม Application Data Flow

---

# 17. Database Migration

Database Schema ต้องใช้ Migration

โครงสร้าง:

```text
database/
├── migrations/
├── seed/
├── schema/
└── README.md
```

Migration ต้องสามารถ:

```text
Create Database
↓
Run Migration
↓
Create Tables
↓
Create Indexes
↓
Seed Development Data
```

ห้ามแก้ Production Schema ด้วยการแก้ Database โดยตรงโดยไม่มี Migration

วิธีจัดการ Migration คือ SQL Migration Files พร้อมตาราง `schema_migrations` ดู `docs/decisions/0003-database-tooling.md`

---

# 18. ORM / Database Library

การเลือก PostgreSQL Client, Query Builder หรือ ORM สามารถกำหนดในช่วง Implementation โดยต้องพิจารณา:

* TypeScript compatibility
* PostgreSQL support
* Migration support
* Transaction support
* Query performance
* Developer maintainability

ไม่ควรเพิ่ม ORM เพียงเพื่อความทันสมัยหากไม่จำเป็น

เมื่อเลือกแล้วต้องบันทึก Technology Decision ใน Repository Documentation

ตัดสินใจแล้ว: ใช้ node-postgres (`pg`) เขียน SQL ใน Repository Layer และไม่ใช้ ORM ดู `docs/decisions/0003-database-tooling.md`

---

# 19. REST API

Frontend และ Backend ใช้ REST API

รูปแบบ Response ควรสม่ำเสมอ

ตัวอย่าง Success:

```json
{
  "success": true,
  "data": {}
}
```

ตัวอย่าง Error:

```json
{
  "success": false,
  "error": {
    "code": "INVALID_INPUT",
    "message": "Invalid input"
  }
}
```

Error Message ที่แสดง User ต้องไม่เปิดเผย:

* Database credentials
* API Keys
* Internal paths
* Stack traces
* System prompts
* Sensitive processing details

---

# 20. API Responsibility

## Frontend

รับผิดชอบ:

```text
UI
Form
Upload
Validation ที่เหมาะสมกับ UX
API Request
API Response Display
```

## Express

รับผิดชอบ:

```text
Authentication
ไม่จำเป็นสำหรับระบบนี้

Session
Validation
Business Logic
Orchestration
Database
API Security
```

## Python

รับผิดชอบ:

```text
AI
NLP
Parsing
Extraction
Normalization
Matching
Evaluation
```

---

# 21. Session Architecture

ระบบไม่มี Login

ใช้ Temporary Session

```text
User
 ↓
Create Session
 ↓
UUID session_id
 ↓
Upload Resume
 ↓
Submit Portfolio
 ↓
Analysis
 ↓
Results
 ↓
Feedback
 ↓
Session Expiration / Deletion
```

Session ใช้ UUID ตาม `DATABASE.md`

ไม่สร้าง Permanent User Account เพียงเพื่อใช้ระบบนี้

---

# 22. File Processing

Resume รองรับ:

```text
PDF
DOC
DOCX
```

Flow:

```text
Upload
 ↓
Validate File
 ↓
Temporary Storage
 ↓
Extract Text
 ↓
AI/NLP Processing
 ↓
Create Evidence
 ↓
Analysis
 ↓
Delete According to Retention Policy
```

ห้ามเก็บ Resume ถาวรโดยไม่มีเหตุผลและนโยบายที่ชัดเจน

---

# 23. Portfolio Processing

Portfolio เป็น URL

รองรับ URL ประเภทต่าง ๆ เช่น

```text
Personal Website
GitHub
GitLab
Behance
itch.io
YouTube
Online Portfolio
```

Flow:

```text
URL
 ↓
Validate
 ↓
Fetch / Access
 ↓
Extract Available Content
 ↓
Analyze Projects
 ↓
Extract Evidence
 ↓
Normalize Skills
```

หาก Portfolio:

```text
Private
Blocked
Login Required
Invalid
Unsupported
Inaccessible
```

ต้องแจ้งสถานะอย่างเหมาะสม

ห้ามตีความว่า

> Portfolio เข้าไม่ได้ = User ไม่มี Skill

---

# 24. Data Flow

Full Analysis Flow:

```text
1. User selects Major
        ↓
2. Create Session
        ↓
3. Upload Resume
        ↓
4. Submit Portfolio URL
        ↓
5. Consent
        ↓
6. Validate Input
        ↓
7. Resume Parsing
        ↓
8. Portfolio Analysis
        ↓
9. Skill Extraction
        ↓
10. Skill Normalization
        ↓
11. Evidence Analysis
        ↓
12. Candidate Skill Profile
        ↓
13. Occupation Knowledge
        +
    Labour Market Data
        ↓
14. Career Matching
        ↓
15. Career Ranking
        ↓
16. Explainable Recommendation
        ↓
17. Skill Gap Analysis
        ↓
18. Development Guidance
        ↓
19. User Feedback / SUS
        ↓
20. Session Expiration / Deletion
```

---

# 25. Career Matching Responsibility

Final Career Score ต้องคำนวณใน Backend/AI Layer

ไม่คำนวณ Final Score ใน React

```text
Candidate Skill Profile
        +
Occupation Skill Profile
        +
Labour Market Signal
        +
Evidence
        ↓
Matching Engine
        ↓
Career Score
        ↓
Ranking
```

ห้ามใช้ Major เป็น Hard Filter

ตัวอย่างที่ห้าม:

```text
Major = Web
→ แสดงเฉพาะ Web Developer
```

ระบบต้องสามารถค้นพบ Career Cross-Major ได้

---

# 26. Career Score Terminology

ใช้คำ:

```text
Career Match Score
Career Compatibility Score
Career Matching Score
```

ห้ามใช้:

```text
Employment Probability
Chance of Getting Job
Probability of Employment
```

เพราะระบบไม่ได้สร้างแบบจำลองเพื่อทำนายโอกาสได้งานโดยตรง

---

# 27. Explainability

ทุก Career Recommendation ควรสามารถอธิบายย้อนกลับได้

ตัวอย่าง:

```text
Career
 ↓
Required Skills
 ↓
Matched Skills
 ↓
User Skill
 ↓
Evidence
 ↓
Resume / Portfolio
```

และ

```text
Career
 ↓
Occupation Skill Profile
 ↓
Demand
 ↓
Job Posting
 ↓
Labour Market Evidence
```

ระบบต้องไม่แสดงเพียง Score อย่างเดียว

---

# 28. Skill Gap Architecture

```text
Occupation Required Skills
          -
User Evidenced Skills
          ↓
Skill Gap
          ↓
Priority
          ↓
Development Guidance
```

สถานะ:

```text
MATCHED
PARTIAL
EVIDENCE_NOT_FOUND
```

ห้ามใช้ข้อความ:

> คุณไม่มี Skill X

หากไม่มีหลักฐาน

ให้ใช้:

> ยังไม่พบหลักฐานของ Skill X

---

# 29. Development Guidance

Guidance Flow:

```text
Skill Gap
 ↓
Learn
 ↓
Practice
 ↓
Build
 ↓
Document
```

ตัวอย่าง:

```text
Skill: TypeScript

Learn:
พื้นฐาน TypeScript

Practice:
นำ TypeScript มาใช้กับ React

Build:
สร้าง Web Application

Document:
เพิ่ม Project ลง Portfolio
```

Guidance ไม่ใช่การรับประกันว่าจะได้งาน

---

# 30. Labour Market Data

Labour Market Dataset ต้องมี Traceability

```text
Job Posting
 ↓
Skill Extraction
 ↓
Skill Normalization
 ↓
Skill Frequency
 ↓
Occupation Skill Profile
 ↓
Career Matching
```

ข้อมูลต้องมี:

```text
source
source_url
date_collected
dataset_version
```

ห้ามสร้าง Demand Score จากตัวเลขที่ผู้พัฒนาสมมติขึ้นเองโดยไม่มีหลักฐาน

รายละเอียดอยู่ใน `DATASET_SPEC.md`

---

# 31. Occupation Data

Occupation Framework ใช้:

```text
ESCO / O*NET
        +
Thai Labour Market
        ↓
Candidate Occupations
        ↓
Normalization
        ↓
Final Occupation Framework
```

ไม่ควรสร้างรายการอาชีพทั้งหมดจากความคิดเห็นของผู้พัฒนาเพียงอย่างเดียว

Expert Validation สามารถใช้เพิ่มเติมได้

---

# 32. Version Strategy

ไม่ควรเขียน Version ของ Framework แบบตายตัวในเอกสาร หากยังไม่ได้ตรวจสอบ Compatibility ณ เวลาพัฒนา

ให้ใช้หลัก:

> Use the latest stable version compatible with the project at implementation time.

แยก Runtime Version ออกจาก Dependency Version เสมอ (ดู `ENVIRONMENT_SETUP.md` §7, §9):

```text
Runtime Version (Node.js, Python)  -> ตรึงแยกต่างหาก (.nvmrc, Dockerfile base image)
Dependency Version (npm, pip)      -> package-lock.json (npm; Package Manager เดียวคือ npm ตาม ADR 0001)
                                       requirements.txt แบบ == ทุกบรรทัด (pip; ไม่ใช้ pnpm/yarn/poetry)
```

Version จริงที่เลือกใช้ (ทั้ง Runtime และ Dependency หลัก) ต้องบันทึกไว้ใน `docs/decisions/` พร้อมเหตุผล ไม่ใช่แค่ในไฟล์ config และควรบันทึก Development Environment ใน README

---

# 33. Environment Variables

ห้าม Hard-code Secret

ตัวอย่าง:

```text
DATABASE_URL=
AI_SERVICE_URL=
NEXT_PUBLIC_API_BASE_URL=
BACKEND_PORT=
NODE_ENV=
```

หากมี External API:

```text
EXTERNAL_API_KEY=
```

ต้องเก็บใน `.env`

ห้าม Commit `.env` ที่มี Secret ขึ้น GitHub

---

# 34. Environment Files

แนะนำ:

```text
.env
.env.example
```

`.env.example` ต้องมีเฉพาะชื่อ Variable และตัวอย่างที่ไม่ใช่ Secret จริง

ตัวอย่าง:

```env
DATABASE_URL=postgresql://career_user:password@postgres:5432/career_system
AI_SERVICE_URL=http://ai-service:8000
NEXT_PUBLIC_API_BASE_URL=http://localhost:4000/api
BACKEND_PORT=4000
NODE_ENV=development
```

ห้ามใส่ Production Credentials

---

# 35. Docker

ทุก Service หลักควรสามารถทำงานใน Docker Environment ได้

ตัวอย่าง:

```text
docker-compose.yml

services:
  frontend
  backend
  ai-service
  postgres
```

Architecture:

```text
Docker Compose
│
├── frontend
│   └── Next.js
│
├── backend
│   └── Express + TypeScript
│
├── ai-service
│   └── Python
│
└── postgres
    └── PostgreSQL
```

---

# 36. Docker Responsibilities

Docker ใช้เพื่อ:

* Development Environment
* Service Isolation
* Dependency Consistency
* Local Database
* AI Service
* Reproducible Environment

Docker ไม่ควรกลายเป็นความซับซ้อนที่ไม่จำเป็นสำหรับ Thesis Prototype

---

# 37. Git

ใช้ Git สำหรับ Source Control

Branch ที่แนะนำ:

```text
main
develop
feature/*
fix/*
```

ตัวอย่าง:

```text
feature/resume-parser
feature/career-matching
feature/skill-gap
feature/career-result-ui
fix/portfolio-parser
```

---

# 38. Git Commit Convention

แนะนำ Conventional Commit Style:

```text
feat:
fix:
refactor:
docs:
test:
chore:
```

ตัวอย่าง:

```text
feat: add resume upload flow
feat: implement skill normalization
feat: add career matching service
fix: handle inaccessible portfolio
test: add skill extraction tests
docs: update API specification
```

---

# 39. GitHub Repository

Repository ควรมีโครงสร้าง:

```text
Career-Prediction-System/
│
├── apps/
│   ├── web/
│   └── api/
├── services/
│   └── ai/
├── database/
├── datasets/
├── docs/
├── scripts/
├── tests/
├── .env.example
├── docker-compose.yml
├── CLAUDE.md
├── README.md
├── .gitattributes
└── .gitignore
```

---

# 40. Frontend Structure

ตัวอย่าง:

```text
apps/web/
├── app/
│   ├── page.tsx
│   ├── analysis/
│   ├── results/
│   │   ├── career/
│   │   └── skill-gap/
│   └── feedback/
│
├── components/
│   ├── ui/
│   ├── career/
│   ├── skill/
│   ├── evidence/
│   └── analysis/
│
├── lib/
│   ├── api/
│   ├── validation/
│   └── utils/
│
├── types/
├── hooks/
└── public/
```

โครงสร้างจริงสามารถปรับตาม Next.js architecture ที่เลือก

---

# 41. Backend Structure

```text
apps/api/
├── src/
│   ├── routes/
│   ├── controllers/
│   ├── services/
│   ├── repositories/
│   ├── clients/
│   ├── middlewares/
│   ├── validators/
│   ├── types/
│   ├── config/
│   └── app.ts
│
├── tests/
├── package.json
└── tsconfig.json
```

---

# 42. AI Service Structure

```text
services/ai/
├── app/
│   ├── main.py
│   ├── api/
│   ├── services/
│   ├── pipelines/
│   ├── extractors/
│   ├── normalizers/
│   ├── matching/
│   ├── models/
│   └── schemas/
│
├── tests/
├── requirements.txt
└── README.md
```

หน้าที่ของแต่ละโฟลเดอร์ดู `FOLDER_STRUCTURE.md` §14-15 (`config/`, `utils/`, `evaluation/` เพิ่มเมื่อมีโค้ดที่ต้องใช้)

---

# 43. Testing Strategy

ระบบต้องทดสอบอย่างน้อย 4 ระดับ

## 43.1 Unit Test

ทดสอบ Function/Module

ตัวอย่าง:

```text
Skill normalization
Alias mapping
Score calculation
Priority calculation
Input validation
```

---

## 43.2 Integration Test

ทดสอบการทำงานระหว่าง Service

ตัวอย่าง:

```text
Express → PostgreSQL
Express → Python
API → Database
```

---

## 43.3 End-to-End Test

ทดสอบ User Flow

```text
Select Major
 ↓
Upload Resume
 ↓
Submit Portfolio
 ↓
Consent
 ↓
Analyze
 ↓
Career Results
 ↓
Skill Gap
 ↓
Feedback
```

---

## 43.4 AI Evaluation

ทดสอบ:

### Skill Extraction

```text
Precision
Recall
F1-score
```

### Career Recommendation

```text
Top-1 Accuracy
Top-3 Hit Rate
Precision@K
```

ต้องมี Ground Truth ที่เหมาะสม

### Usability

```text
SUS
User Satisfaction
```

---

# 44. Error Handling

ระบบต้องรองรับ:

```text
Invalid Resume
Unsupported File
Corrupted File
Portfolio Invalid URL
Portfolio Inaccessible
Portfolio Blocked
Portfolio Login Required
AI Processing Error
Database Error
Timeout
Empty Extraction Result
No Strong Career Match
```

กรณีไม่มีข้อมูลเพียงพอ ต้องแสดงข้อความที่อธิบายสถานการณ์แทนการสร้างผลลัพธ์ที่ไม่มีหลักฐาน

---

# 45. Security

ต้องมีมาตรการอย่างน้อย:

```text
Input Validation
File Type Validation
File Size Validation
URL Validation
Parameterized Query
SQL Injection Protection
XSS Protection
CORS Configuration
Rate Limiting
Secret Management
Error Sanitization
Temporary File Handling
```

Resume และ Portfolio อาจมีข้อมูลส่วนบุคคล จึงต้องเก็บข้อมูลเท่าที่จำเป็น

---

# 46. Privacy Architecture

```text
User
 ↓
Upload
 ↓
Consent
 ↓
Temporary Processing
 ↓
Analysis
 ↓
Result
 ↓
Retention Period
 ↓
Delete
```

ไม่มี Login จึงไม่ควรสร้าง Permanent User Profile โดยไม่จำเป็น

---

# 47. Accessibility

Frontend ควรคำนึงถึง:

```text
Keyboard Navigation
Semantic HTML
Form Labels
Focus State
Readable Text
Color Contrast
Alt Text
Error Message
Loading State
Screen Reader Compatibility
```

---

# 48. Responsive Design

ระบบต้องรองรับอย่างน้อย:

```text
Desktop
Tablet
Mobile
```

UI ต้องไม่พึ่งพาเฉพาะ Desktop

---

# 49. Performance

หลักการ:

* ไม่โหลดข้อมูลทั้งหมดโดยไม่จำเป็น
* จำกัด File Upload Size
* จำกัดจำนวน Portfolio URL
* ใช้ Pagination เมื่อ Dataset ใหญ่
* Cache ข้อมูล Knowledge ที่ไม่เปลี่ยนบ่อย
* แยก AI Processing ออกจาก Request ที่ไม่จำเป็น
* ใช้ Background Processing หาก Analysis ใช้เวลานาน

---

# 50. AI Processing Strategy

หาก Resume/Portfolio Analysis ใช้เวลานาน:

```text
POST /api/analyze
        ↓
Create Processing Job
        ↓
Python AI Service
        ↓
Update Processing Status
        ↓
Frontend Poll / Retrieve Status
        ↓
Completed
        ↓
Display Result
```

Frontend ต้องแสดง Processing Status เช่น:

```text
กำลังตรวจสอบข้อมูล
กำลังอ่าน Resume
กำลังวิเคราะห์ Portfolio
กำลังตรวจจับ Skills
กำลังสร้าง Skill Profile
กำลังวิเคราะห์อาชีพ
กำลังวิเคราะห์ Skill Gap
กำลังสร้างคำแนะนำ
```

---

# 51. Configuration

ค่าที่สามารถเปลี่ยนได้โดยไม่แก้ Business Logic ควรแยกเป็น Configuration

ตัวอย่าง:

```text
MAX_RESUME_SIZE
MAX_PORTFOLIO_URLS
SESSION_EXPIRATION
TOP_K_CAREERS
AI_TIMEOUT
SUPPORTED_FILE_TYPES
```

Career Matching Weights ต้องไม่ hard-code โดยไม่มีเหตุผล

ควรจัดเก็บเป็น Configuration ที่สามารถ version ได้

---

# 52. Algorithm Version

ทุกผลลัพธ์ Career Recommendation ควรบันทึก:

```text
algorithm_version
dataset_version
```

ตัวอย่าง:

```text
algorithm_version = "v1"
dataset_version = "2026-01"
```

ค่าจริงขึ้นอยู่กับ Implementation

เหตุผล:

เพื่อให้สามารถตอบได้ว่า

> ผลลัพธ์นี้ถูกสร้างจาก Algorithm และ Dataset รุ่นใด

---

# 53. Dataset Versioning

ข้อมูล Labour Market และ Occupation Knowledge ต้องมี Version

ตัวอย่าง:

```text
dataset_version
source
collection_period
created_at
description
```

หาก Dataset เปลี่ยน ผลลัพธ์ในอนาคตอาจเปลี่ยนตาม

จึงต้องสามารถ Trace ได้ว่า Career Result ใช้ Dataset Version ใด

---

# 54. AI Model Versioning

หากใช้ Model หรือ Embedding Model ต้องบันทึก:

```text
model_name
model_version
embedding_model
configuration
```

หาก Model เปลี่ยน ต้องสามารถระบุได้ว่าผลลัพธ์สร้างจาก Model ใด

---

# 55. Development Environment

Recommended Development Flow:

```text
Developer
 ↓
Git
 ↓
GitHub
 ↓
Docker Compose
 ↓
Next.js
Express
Python
PostgreSQL
```

การเริ่ม Project ใหม่ควรทำให้ Developer คนอื่นสามารถ Clone แล้ว Setup ได้ตาม README

---

# 56. Local Development

ตัวอย่าง:

```text
Frontend
http://localhost:3000

Backend
http://localhost:4000

AI Service
http://localhost:8000

PostgreSQL
localhost:5432
```

Port จริงสามารถปรับตาม Implementation

---

# 57. API Documentation

Backend ต้องมี API Documentation

ควรบันทึก:

```text
Endpoint
Method
Request
Response
Validation
Error
Example
```

สามารถใช้ OpenAPI/Swagger หรือ Markdown API Documentation

ไม่ควรปล่อย API Contract ให้ขึ้นอยู่กับความเข้าใจของ Developer เพียงอย่างเดียว

---

# 58. Type Contract

ข้อมูลระหว่าง Frontend และ Backend ต้องมี Type ที่สอดคล้องกัน

ตัวอย่าง:

```text
CareerResult
{
  resultId
  occupation
  score
  rank
  matchedSkills
  evidence
  marketDemand
  explanation
}
```

Frontend ไม่ควรตีความชื่อ Field เองโดยไม่มี API Contract

---

# 59. No Duplicate Backend

ห้ามสร้าง Architecture แบบ:

```text
Next.js API
+
Express API
```

แล้วให้ทั้งสองทำหน้าที่เป็น Main Backend พร้อมกัน

ระบบนี้กำหนด:

```text
Next.js = Frontend

Express = Main Backend API

Python = AI/NLP Service

PostgreSQL = Database
```

อย่างชัดเจน

---

# 60. Technology Not Used as Main Stack

เทคโนโลยีต่อไปนี้ไม่ใช่ Main Stack ของ Thesis:

```text
PHP
MariaDB
MySQL
Yii2
Vue
Vite
MongoDB
```

ไม่ได้หมายความว่าเทคโนโลยีเหล่านี้ไม่ดี แต่ไม่ควรนำกลับมาใช้เป็น Architecture หลัก เพราะ Stack ของ Project ถูกกำหนดไว้แล้ว

---

# 61. Why PostgreSQL

PostgreSQL เหมาะกับระบบนี้เนื่องจากมีข้อมูลเชิงสัมพันธ์จำนวนมาก:

```text
Major
 ↓
Session
 ↓
Resume / Portfolio
 ↓
Skill
 ↓
Occupation
 ↓
Occupation Skill
 ↓
Job Posting
```

และจำเป็นต้องใช้:

* Foreign Keys
* Constraints
* Transactions
* Indexes
* Structured Query
* Dataset Versioning

---

# 62. Why Python

Python เหมาะสำหรับ AI/NLP เนื่องจากมี Ecosystem สำหรับ:

```text
NLP
Machine Learning
Text Processing
Embeddings
Data Processing
Evaluation
```

จึงแยก AI Layer ออกจาก Web Backend ได้อย่างชัดเจน

---

# 63. Why TypeScript

TypeScript เหมาะกับ Frontend และ Backend เพราะช่วยให้:

```text
Frontend Type
        ↕
API Contract
        ↕
Backend Type
```

มีความสอดคล้องกันมากขึ้น

---

# 64. Why Docker

Docker ช่วยลดปัญหา:

```text
Works on my machine
```

โดยกำหนด Environment สำหรับ:

```text
Node.js
Python
PostgreSQL
```

ให้ใกล้เคียงกันระหว่าง Developer Environment

---

# 65. Semester 1 Architecture

Semester 1 ใช้ **Creative Media Technology – Web Full Stack เป็น Pilot**

Scope:

```text
Web Full Stack
 ↓
Resume
 ↓
Portfolio
 ↓
Skill Extraction
 ↓
Career Matching
 ↓
Skill Gap
```

ควรสร้าง Architecture ให้สามารถขยายต่อได้

ไม่ควรสร้าง Database หรือ Code ที่ผูกติดกับ Web Full Stack จนขยายสาขาอื่นไม่ได้

---

# 66. Semester 2 Architecture

Semester 2 ขยายเป็นทั้งคณะ

```text
Faculty
│
├── Film & Radio Television
├── Advertising & Public Relations
├── Digital Printing & Packaging
└── Creative Media Technology
      ├── Web Full Stack
      └── Game Development
```

Backend และ AI Engine ต้องใช้ Architecture เดิม

สิ่งที่เพิ่มคือ:

```text
Occupation Data
Skill Data
Job Market Data
Major Data
```

ไม่ควรสร้าง Matching Engine ใหม่แยกตามสาขา

---

# 67. Scalability Principle

ระบบต้องออกแบบให้เพิ่ม:

```text
Major
Career Family
Occupation
Skill
Job Source
AI Model
```

ได้โดยไม่ต้อง Rewrite Core System

ตัวอย่าง:

```text
New Occupation
→ Add Dataset

New Skill
→ Add Skill Dictionary

New Major
→ Add Major Data
```

ไม่ควร:

```text
if major == "Web":
   ...
elif major == "Game":
   ...
```

เต็มไปทั่วระบบ

---

# 68. Observability

ระบบควรเก็บ Log ที่จำเป็นสำหรับ Debugging

เช่น:

```text
Request ID
Session ID
Processing Status
Processing Duration
Error Code
Service
Algorithm Version
Dataset Version
```

ห้าม Log:

```text
Password
API Key
Secret
Unnecessary Personal Data
Full Sensitive Resume Content
```

---

# 69. Logging Strategy

แบ่ง Log ตามระดับ:

```text
INFO
WARN
ERROR
```

ตัวอย่าง:

```text
INFO:
Analysis started

WARN:
Portfolio inaccessible

ERROR:
AI service timeout
```

Production Log ไม่ควรเปิดเผย Stack Trace ให้ User

---

# 70. API Security Between Services

Express → Python ต้องเป็น Internal Service Communication

ควรตรวจสอบ:

```text
Request Validation
Timeout
Payload Size
Service Authentication หากจำเป็น
Error Handling
```

Python ไม่ควรเปิด Endpoint ที่รับคำขอจาก Internet โดยไม่จำเป็น

---

# 71. Data Validation

Validation ต้องทำอย่างน้อยสองระดับ:

```text
Frontend Validation
        +
Backend Validation
```

Frontend Validation มีไว้เพื่อ UX

Backend Validation เป็น Security Boundary และเป็น Validation ที่เชื่อถือได้

---

# 72. File Security

Resume Upload ต้องตรวจสอบ:

```text
Extension
MIME Type
File Size
File Integrity
Filename
```

ไม่ควรใช้ชื่อไฟล์จาก User เป็น Path โดยตรง

ควรสร้าง Internal Storage Reference

---

# 73. Portfolio Security

Portfolio URL ต้อง:

* Validate URL
* จำกัด Protocol
* ป้องกัน SSRF
* จำกัด Redirect
* จำกัด Request Timeout
* จำกัด Response Size
* ไม่เรียก Internal Network
* ไม่เข้าถึง localhost/private IP

---

# 74. AI Safety / Reliability

AI ต้องไม่สร้างข้อมูลหลักฐานขึ้นเอง

ตัวอย่างที่ห้าม:

```text
Resume ไม่กล่าวถึง React
→ AI สรุปว่า User มี React
```

หรือ:

```text
Portfolio เข้าไม่ได้
→ AI สรุปว่า User ไม่มี Skill
```

AI ต้องยึด Evidence

---

# 75. No Hallucinated Evidence

Career Recommendation ต้องมี Evidence ที่ตรวจสอบย้อนกลับได้

หากไม่มี Evidence:

```text
Evidence Not Found
```

ไม่ควรสร้าง Project หรือ Experience ที่ไม่มีอยู่ใน Input

---

# 76. Fallback Strategy

หาก AI Model ไม่สามารถทำงานได้:

```text
AI Failure
 ↓
Fallback Processing
 ↓
Rule / Dictionary Based Extraction
 ↓
Continue if sufficient
```

หากข้อมูลไม่เพียงพอ:

```text
Insufficient Evidence
```

แทนการสร้างผลลัพธ์ที่ไม่มีหลักฐาน

---

# 77. Development Priority

ลำดับการพัฒนา:

```text
1. Database
2. Dataset
3. Skill Taxonomy
4. Occupation Framework
5. Labour Market Data
6. Resume Parser
7. Portfolio Analyzer
8. Skill Extraction
9. Candidate Skill Profile
10. Matching Engine
11. Skill Gap
12. Explainability
13. Backend API
14. Frontend UI
15. Evaluation
16. Deployment
```

อย่างไรก็ตามสามารถพัฒนา Frontend Prototype คู่ขนานได้ เพื่อทดสอบ UX ก่อน AI Engine เสร็จ

---

# 78. Recommended Implementation Order

Stage ด้านล่างเป็นกลุ่มงานเชิงแนวคิด ไม่ใช่เลข Phase ที่ใช้พัฒนา เลข Phase ที่ใช้จริงอยู่ใน `IMPLEMENTATION_PLAN.md` §3 และ `CLAUDE.md` §8

| Stage | Phase ที่ตรงกัน |
| --- | --- |
| 1 Foundation | 0-1 |
| 2 Data | 2-3 |
| 3 Analysis | 4-6 |
| 4 Recommendation | 7-8 |
| 5 UI | 10 (Phase 9 Backend API พัฒนาควบคู่) |
| 6 Evaluation | 11-12 (Deployment คือ Phase 13) |

## Stage 1 — Foundation

```text
GitHub Repository
Docker
PostgreSQL
Database Migration
Express
Next.js
Python Service
Environment Configuration
```

## Stage 2 — Data

```text
Skill Taxonomy
Skill Alias
Occupation
Occupation Alias
Career Family
Job Posting
Occupation Skill
Dataset Version
```

## Stage 3 — Analysis

```text
Resume Parser
Portfolio Analyzer
Skill Extraction
Skill Normalization
Evidence
Candidate Profile
```

## Stage 4 — Recommendation

```text
Matching
Ranking
Explanation
Skill Gap
Guidance
```

## Stage 5 — UI

```text
Input
Upload
Processing
Results
Career Detail
Skill Gap
Guidance
Feedback
```

## Stage 6 — Evaluation

```text
Skill Extraction Evaluation
Career Recommendation Evaluation
SUS
User Satisfaction
```

---

# 79. Development Principle

ห้ามเริ่มจากการสร้าง AI Model ก่อน

ลำดับที่ถูกต้อง:

```text
Data
 ↓
Schema
 ↓
Taxonomy
 ↓
Occupation
 ↓
Labour Market
 ↓
Evidence
 ↓
Matching
 ↓
AI Enhancement
```

เพราะ AI ที่ดีไม่สามารถแก้ Dataset ที่ไม่มีโครงสร้างได้

---

# 80. Thesis Reproducibility

ระบบต้องสามารถอธิบายได้ว่า:

```text
Input
 ↓
Processing
 ↓
Extraction
 ↓
Normalization
 ↓
Matching
 ↓
Ranking
 ↓
Skill Gap
 ↓
Result
```

และระบุ:

```text
Dataset Version
Algorithm Version
Model Version
```

เพื่อใช้ประกอบการเขียน Chapter 3 และการทดลอง

---

# 81. Technical Documentation

Repository ควรมี:

```text
README.md
ARCHITECTURE.md
API.md
DATABASE.md
DATASET_SPEC.md
AI_MATCHING_SPEC.md
UI_UX_SPEC.md
TECH_STACK.md
IMPLEMENTATION_PLAN.md
```

Documentation ต้องสอดคล้องกัน

หากเปลี่ยน Architecture ต้องตรวจสอบเอกสารที่เกี่ยวข้องด้วย

---

# 82. Definition of Done — Technical

Feature จะถือว่าเสร็จเมื่อ:

* Code ทำงานได้
* TypeScript Compile ผ่าน
* Tests ที่เกี่ยวข้องผ่าน
* API Contract ถูกต้อง
* Database Migration ถูกต้อง
* Error Handling มี
* Security Validation มี
* ไม่มี Secret ใน Source Code
* Documentation ถูกอัปเดต
* Git Commit มีความหมาย
* สามารถ Run ผ่าน Development Environment ได้

---

# 83. Claude Implementation Rules

Claude ต้องปฏิบัติตามกฎต่อไปนี้:

### Rule 1

ใช้ Technology Stack ตามเอกสารนี้

```text
Next.js
React
TypeScript
Tailwind CSS
Node.js
Express.js
Python
PostgreSQL
Docker
Git
GitHub
```

### Rule 2

ห้ามเปลี่ยน Database ไปเป็น:

```text
MySQL
MariaDB
MongoDB
```

โดยไม่ได้รับอนุมัติ

### Rule 3

ห้ามนำ PHP กลับมาเป็น Backend หลัก

### Rule 4

Next.js เป็น Frontend

### Rule 5

Express เป็น Main Backend API

### Rule 6

Python เป็น AI/NLP Service

### Rule 7

Python ไม่ควรกลายเป็น Main Web Backend

### Rule 8

Frontend ห้ามเข้าถึง PostgreSQL โดยตรง

### Rule 9

ห้ามคำนวณ Final Career Score ใน Frontend

### Rule 10

Major ห้ามเป็น Hard Filter

### Rule 11

ห้ามใช้ Employment Probability

### Rule 12

ห้ามสร้าง Labour Market Demand จากตัวเลขสมมติ

### Rule 13

ห้ามสร้าง Evidence ที่ไม่มีใน Resume หรือ Portfolio

### Rule 14

ไม่พบ Skill ต้องใช้:

```text
Evidence Not Found
```

ไม่ใช่:

```text
User does not have this skill
```

### Rule 15

Career Recommendation ต้อง Explainable

### Rule 16

ต้องรองรับ Dataset Version

### Rule 17

ต้องรองรับ Algorithm Version

### Rule 18

Database Schema ต้องใช้ Migration

### Rule 19

Secret ต้องอยู่ใน Environment Variables

### Rule 20

ห้าม Commit Secret ขึ้น GitHub

### Rule 21

ห้ามเพิ่ม Technology ใหม่เพียงเพราะเป็น Technology ที่ได้รับความนิยม

### Rule 22

หากต้องการเปลี่ยน Architecture ต้องอธิบายเหตุผลและตรวจสอบเอกสารที่เกี่ยวข้องก่อน

### Rule 23

หาก Technology Version ไม่ได้ระบุไว้ ให้เลือก Version ที่ Stable และ Compatible ณ เวลาพัฒนา แล้วบันทึก Version จริงไว้ใน Dependency Lockfile

### Rule 24

ทุก Feature ต้องสามารถทดสอบได้

### Rule 25

ทุกผลลัพธ์สำคัญต้อง Trace กลับไปยังข้อมูลต้นทางได้

---

# 84. Final Technical Architecture

Architecture ที่ Lock:

```text
                         USER
                           │
                           ▼
              ┌────────────────────────┐
              │        NEXT.JS         │
              │ React + TypeScript     │
              │ Tailwind CSS            │
              │                        │
              │ Frontend / UI          │
              └───────────┬────────────┘
                          │
                       REST/JSON
                          │
                          ▼
              ┌────────────────────────┐
              │      EXPRESS.JS        │
              │ Node.js + TypeScript   │
              │                        │
              │ Main Backend API       │
              │ Business Logic         │
              │ Validation             │
              │ Orchestration          │
              └───────┬────────┬───────┘
                      │        │
                      │        │ HTTP/JSON
                      │        ▼
                      │ ┌──────────────────┐
                      │ │  PYTHON SERVICE  │
                      │ │                  │
                      │ │ Resume Parsing   │
                      │ │ NLP              │
                      │ │ Skill Extraction │
                      │ │ Normalization    │
                      │ │ Evidence         │
                      │ │ Embedding        │
                      │ │ Matching         │
                      │ │ Evaluation       │
                      │ └──────────────────┘
                      │
                      ▼
              ┌────────────────────────┐
              │      POSTGRESQL        │
              │                        │
              │ Application Data       │
              │ Knowledge Data         │
              │ Labour Market Data     │
              │ Results                │
              └────────────────────────┘

                   DOCKER COMPOSE
                          │
             ┌────────────┼────────────┐
             │            │            │
             ▼            ▼            ▼
          Frontend     Backend      AI Service
                                         │
                                         │
                                    PostgreSQL
```

---

# 85. Technology Status

```text
Project Concept: LOCKED
Core Workflow: LOCKED

Frontend:
Next.js + React + TypeScript + Tailwind CSS: LOCKED

Backend:
Node.js + Express.js + TypeScript: LOCKED

AI/NLP:
Python: LOCKED

Database:
PostgreSQL: LOCKED

Container:
Docker + Docker Compose: LOCKED

Version Control:
Git + GitHub: LOCKED

No Login:
LOCKED

Major as Context:
LOCKED

Cross-Major Matching:
LOCKED

Resume + Portfolio:
LOCKED

Evidence-Based Analysis:
LOCKED

Labour Market Orientation:
LOCKED

Explainable Recommendation:
LOCKED

Skill Gap:
LOCKED

Development Guidance:
LOCKED

Evaluation:
LOCKED
```

---

# 86. Related Documents

```text
PROJECT_SPEC.md
    ↓
DATABASE.md
    ↓
DATASET_SPEC.md
    ↓
AI_MATCHING_SPEC.md
    ↓
UI_UX_SPEC.md
    ↓
TECH_STACK.md
    ↓
IMPLEMENTATION_PLAN.md
```

เอกสารทั้งหมดต้องสอดคล้องกัน

หากเกิดความขัดแย้ง ให้ตรวจสอบ:

```text
PROJECT_SPEC.md
        ↓
DATABASE.md
        ↓
DATASET_SPEC.md
        ↓
AI_MATCHING_SPEC.md
        ↓
UI_UX_SPEC.md
        ↓
TECH_STACK.md
```

และแก้ไขเอกสารที่เกี่ยวข้องก่อนเริ่ม Implementation

---

# 87. Final Principle

Technology เป็นเครื่องมือ ไม่ใช่เป้าหมายของระบบ

ระบบต้องให้ความสำคัญกับ:

```text
Reliable Data
      +
Evidence
      +
Labour Market
      +
Explainable Matching
      +
Skill Gap
      +
Usability
```

มากกว่าการเพิ่ม Technology ที่ไม่จำเป็น

**Final Architecture:**

```text
Next.js
   +
Express.js
   +
Python AI/NLP
   +
PostgreSQL
   +
Docker
   +
Git/GitHub
```

ถือเป็น Technology Stack หลักของ Thesis Project และเป็นพื้นฐานสำหรับการพัฒนา Semester 1 และการขยายระบบใน Semester 2