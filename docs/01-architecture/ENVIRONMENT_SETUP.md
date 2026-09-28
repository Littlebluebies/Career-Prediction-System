# ENVIRONMENT_SETUP.md

# Career Prediction and Skill Gap Analysis System

## Development Environment Setup Specification

**Project:** Career Prediction and Skill Gap Analysis System for Mass Communication Technology Students
**Frontend:** Next.js + React + TypeScript + Tailwind CSS
**Backend:** Node.js + Express.js + TypeScript
**AI/NLP:** Python
**Database:** PostgreSQL
**Container:** Docker + Docker Compose
**Version Control:** Git + GitHub

---

# 1. Purpose

เอกสารนี้กำหนดวิธีเตรียม Development Environment สำหรับระบบ

เป้าหมายคือทำให้ Developer หรือ Claude สามารถ:

```text
เครื่องใหม่
   ↓
ติดตั้ง Tools
   ↓
Clone Project
   ↓
ตั้งค่า Environment
   ↓
Start Docker
   ↓
Run Database
   ↓
Run Backend
   ↓
Run AI Service
   ↓
Run Frontend
   ↓
เปิดระบบได้
```

โดยทุก Environment ต้องใช้ Architecture เดียวกัน

---

# 2. Required Technology

ระบบใช้ Technology ต่อไปนี้

| Technology     | Responsibility            |
| -------------- | ------------------------- |
| Next.js        | Frontend Framework        |
| React          | UI                        |
| TypeScript     | Type Safety               |
| Tailwind CSS   | Styling                   |
| Node.js        | Backend Runtime           |
| Express.js     | REST API                  |
| Python         | AI/NLP                    |
| PostgreSQL     | Main Database             |
| Docker         | Containerization          |
| Docker Compose | Multi-service Environment |
| Git            | Version Control           |
| GitHub         | Repository                |

---

# 3. Technologies Not Used as Main Stack

ห้ามเปลี่ยนไปใช้ Technology เหล่านี้เป็น Main Stack:

```text
PHP
MariaDB
MySQL
MongoDB
Yii2
Vue
Vite
```

ไม่ได้หมายความว่า Technology เหล่านี้ใช้ไม่ได้ตลอดไปในทุกกรณี แต่สำหรับ Project นี้ต้องยึด Stack ที่กำหนดไว้

---

# 4. Architecture

```text
                         USER
                           │
                           ▼
                ┌────────────────────┐
                │      Next.js       │
                │ React + TypeScript │
                │    Tailwind CSS    │
                └─────────┬──────────┘
                          │
                       REST API
                          │
                          ▼
                ┌────────────────────┐
                │      Express       │
                │ Node.js + TypeScript│
                └──────┬───────┬─────┘
                       │       │
                       │       │ HTTP / JSON
                       │       ▼
                       │ ┌────────────────┐
                       │ │   AI Service   │
                       │ │     Python     │
                       │ └────────────────┘
                       │
                       ▼
                ┌────────────────────┐
                │     PostgreSQL     │
                └────────────────────┘
```

---

# 5. Development Modes

ระบบรองรับ 2 รูปแบบ

## Mode A — Docker Development

แนะนำสำหรับการทำงานที่ต้องการ Environment ใกล้เคียงกัน

```text
Docker Compose
├── frontend
├── backend
├── ai-service
└── postgres
```

---

## Mode B — Local Development

สามารถ Run Application บนเครื่องโดยตรงได้

```text
Next.js
Node.js + Express
Python
```

และให้ PostgreSQL ทำงานผ่าน Docker

ตัวอย่าง:

```text
Next.js
   ↓
localhost:4000
   ↓
Express
   ↓
localhost:5432
   ↓
PostgreSQL
```

---

# 6. Prerequisites

ก่อนเริ่ม Project ต้องติดตั้ง:

```text
Git
Node.js
npm
Python
Docker
Docker Compose
```

ไม่จำเป็นต้องติดตั้ง PostgreSQL Server บนเครื่อง หากใช้ PostgreSQL ผ่าน Docker

---

# 7. Node.js

Node.js ใช้สำหรับ:

```text
Next.js
Express.js
Backend Tools
Package Management
```

ควรใช้ Node.js รุ่น LTS ที่ยังได้รับการ Support ณ เวลาพัฒนา

ห้ามกำหนด Version เก่าเพียงเพื่อให้ตรงกับตัวอย่างเอกสาร

**Runtime Version** (ตัว Node.js เอง) กับ **Dependency Version** (npm package แต่ละตัว) เป็นคนละเรื่อง ต้องตรึงแยกกัน:

```text
Runtime Version (Node.js)  -> .nvmrc + package.json "engines.node" + Dockerfile base image tag
Dependency Version (npm)   -> package.json (ช่วง) + package-lock.json (Exact, Commit เข้า Repo)
```

Runtime Version ที่เลือกจริงต้องบันทึกเหตุผลไว้ใน `docs/decisions/` ด้วย ไม่ใช่แค่ในไฟล์ข้างบน

---

# 8. Package Manager

สามารถใช้ npm เป็น Default Package Manager

ตัวอย่าง:

```bash
npm install
```

และ:

```bash
npm run dev
```

หาก Project เปลี่ยนไปใช้ pnpm หรือ yarn ต้องกำหนดให้เป็นมาตรฐานเดียวกันทั้ง Repository

ห้ามใช้ Package Manager หลายชนิดปะปนกันโดยไม่มีเหตุผล

---

# 9. Python

Python ใช้สำหรับ:

```text
Resume Parsing
Portfolio Processing
NLP
Skill Extraction
Skill Normalization
Semantic Similarity
Embedding
AI Evaluation
```

ควรใช้ Python Version ที่ Compatible กับ Library ที่เลือกใช้จริง

**Runtime Version** (ตัว Python Interpreter) กับ **Dependency Version** (แต่ละ Library ใน `requirements.txt`) เป็นคนละเรื่อง ต้องตรึงแยกกัน:

```text
Runtime Version (Python)  -> Dockerfile base image tag (ตรึงถึงระดับ Minor เช่น 3.13)
Dependency Version (pip)  -> services/ai/requirements.txt (ตรึง Exact ด้วย == ทุกบรรทัด ห้ามเว้นเวอร์ชัน)
```

Runtime Version ที่เลือกจริงต้องบันทึกเหตุผลไว้ใน `docs/decisions/` ด้วย ไม่ใช่แค่ใน Dockerfile

---

# 10. Python Virtual Environment

หาก Run Python แบบ Local ให้สร้าง Virtual Environment

ตัวอย่าง:

```bash
python -m venv .venv
```

Activate บน Windows:

```bash
.venv\Scripts\activate
```

บน macOS/Linux:

```bash
source .venv/bin/activate
```

จากนั้น:

```bash
pip install -r requirements.txt
```

---

# 11. Python Dependency

Dependency ต้องอยู่ใน:

```text
services/ai/requirements.txt
```

ห้ามติดตั้ง Library สำคัญในเครื่องโดยไม่บันทึกลง Dependency File

ทุกบรรทัดใน `requirements.txt` ต้องตรึง Version แบบ Exact ด้วย `==` (เช่น `fastapi==0.115.0`) ห้ามเว้นเวอร์ชันหรือใช้ `>=` เพียงอย่างเดียว เพราะ Python ไม่มี Lockfile มาตรฐานเหมือน npm ไฟล์นี้จึงทำหน้าที่แทน Lockfile

เมื่อเพิ่ม Library:

```text
requirements.txt
```

ต้องถูก Update

---

# 12. PostgreSQL

PostgreSQL เป็น Main Database

Development แนะนำให้ใช้ Docker

ตัวอย่าง Concept:

```text
PostgreSQL Container
        ↓
Port 5432
        ↓
career_system Database
```

Database ต้องสอดคล้องกับ `DATABASE.md`

---

# 13. PostgreSQL Database

Database Name ตัวอย่าง:

```text
career_system
```

Schema:

```text
career_system
```

หรือ Schema ที่กำหนดใน `DATABASE.md`

ต้องยึด `DATABASE.md` เป็น Source of Truth หากมีการเปลี่ยนชื่อภายหลัง

---

# 14. PostgreSQL Connection

ตัวอย่าง:

```env
DATABASE_URL=postgresql://career_user:password@postgres:5432/career_system
```

สำหรับ Docker

Local Development อาจเป็น:

```env
DATABASE_URL=postgresql://career_user:password@localhost:5432/career_system
```

ห้าม Commit Password จริงลง Git

---

# 15. Environment Variables

Root:

```text
.env.example
```

ควรมีตัวอย่าง:

```env
NODE_ENV=development

DATABASE_URL=postgresql://career_user:password@postgres:5432/career_system

AI_SERVICE_URL=http://ai-service:8000

NEXT_PUBLIC_API_BASE_URL=http://localhost:4000/api

SESSION_TTL_MINUTES=60

MAX_RESUME_SIZE_MB=10

ALGORITHM_VERSION=career-matching-v1

DATASET_VERSION=development
```

ค่าเหล่านี้เป็นตัวอย่าง

ค่าจริงต้องถูกกำหนดใน Environment

---

# 16. Environment Variable Rules

แบ่งเป็น:

## Public

Frontend สามารถเข้าถึงได้ เช่น:

```text
NEXT_PUBLIC_API_BASE_URL
```

## Private

ห้ามส่งไป Frontend:

```text
DATABASE_URL
AI_SERVICE_URL
API_KEYS
SECRET_KEYS
```

หลักการ:

```text
NEXT_PUBLIC_*
```

เท่านั้นที่ควรถือว่าเป็นข้อมูลที่ Frontend อาจเข้าถึงได้

---

# 17. `.env` Files

Local:

```text
.env
```

Frontend อาจใช้:

```text
apps/web/.env.local
```

Backend:

```text
apps/api/.env
```

AI:

```text
services/ai/.env
```

แต่ต้องจัดการไม่ให้ถูก Commit

---

# 18. `.gitignore`

ต้อง Ignore:

```text
.env
.env.local
.env.*.local

node_modules/
.next/
dist/
build/

.venv/
__pycache__/
*.pyc

uploads/
storage/
temporary/
logs/

*.log
```

และข้อมูล Resume / Portfolio ของผู้ใช้ทั้งหมด

---

# 19. Project Clone

เมื่อ Repository ถูกสร้างบน GitHub:

```bash
git clone <repository-url>
```

จากนั้น:

```bash
cd Career-Prediction-System
```

ห้ามสมมติชื่อ Repository จริงหากยังไม่ได้สร้าง

---

# 20. Install Frontend

เข้า:

```bash
cd apps/web
```

ติดตั้ง:

```bash
npm install
```

จากนั้นกลับ Root:

```bash
cd ../..
```

---

# 21. Install Backend

เข้า:

```bash
cd apps/api
```

ติดตั้ง:

```bash
npm install
```

จากนั้น:

```bash
cd ../..
```

---

# 22. Install AI Service

เข้า:

```bash
cd services/ai
```

สร้าง Virtual Environment:

```bash
python -m venv .venv
```

Activate:

```bash
.venv\Scripts\activate
```

ติดตั้ง:

```bash
pip install -r requirements.txt
```

---

# 23. Docker Compose

Root:

```text
docker-compose.yml
```

ต้องรองรับ:

```text
frontend
backend
ai-service
postgres
```

Concept:

```yaml
services:
  frontend:
    ...

  backend:
    ...

  ai-service:
    ...

  postgres:
    ...
```

Build context ของแต่ละ Service:

```text
frontend    -> ./apps/web
backend     -> ./apps/api
ai-service  -> ./services/ai
```

รายละเอียดจริงต้องสอดคล้องกับ Docker Configuration ที่สร้างใน Implementation

---

# 24. Service Ports

แนะนำ Development Ports:

```text
Frontend:
3000

Backend:
4000

AI Service:
8000

PostgreSQL:
5432
```

ดังนั้น:

```text
http://localhost:3000
```

คือ Frontend

```text
http://localhost:4000
```

คือ Backend

```text
http://localhost:8000
```

คือ AI Service

```text
localhost:5432
```

คือ PostgreSQL

---

# 25. Port Rules

หาก Port ถูกใช้งานอยู่:

```text
อย่าเปลี่ยน Port แบบสุ่มในแต่ละเครื่อง
```

ให้แก้ผ่าน Environment Configuration

ตัวอย่าง:

```env
FRONTEND_PORT=3000
BACKEND_PORT=4000
AI_SERVICE_PORT=8000
POSTGRES_PORT=5432
```

แต่ค่าที่ใช้งานจริงต้องสอดคล้องกับ Docker Compose

---

# 26. Docker Network

ให้ Docker Compose สร้าง Internal Network

Concept:

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

ภายใน Docker ห้ามใช้:

```text
localhost
```

เพื่ออ้างถึง Container อื่น

ให้ใช้ Service Name เช่น:

```text
postgres
ai-service
backend
```

---

# 27. Important Docker Rule

ภายใน Container:

```text
localhost
```

หมายถึง Container ตัวนั้นเอง

ดังนั้น:

Backend → PostgreSQL:

```text
postgres:5432
```

ไม่ใช่:

```text
localhost:5432
```

Backend → Python:

```text
ai-service:8000
```

ไม่ใช่:

```text
localhost:8000
```

---

# 28. Start Database

เริ่ม PostgreSQL:

```bash
docker compose up -d postgres
```

ตรวจสอบ:

```bash
docker compose ps
```

ควรเห็น PostgreSQL ทำงานอยู่

---

# 29. Run Database Migration

หลัง Database พร้อม:

```text
database/migrations/
```

ต้องถูก Execute ตามลำดับ

ตัวอย่าง:

```text
001_create_schema.sql
002_create_major.sql
003_create_user_session.sql
...
```

Migration ต้องทำงานตามลำดับ

---

# 30. Seed Database

หลัง Migration:

```text
seed/
```

สามารถใส่ข้อมูล Development เช่น:

```text
Major
Career Family
Skill
Occupation
Alias
```

Seed ต้องแยกจาก Production Labour Market Dataset

---

# 31. Database Initialization

Flow:

```text
Start PostgreSQL
       ↓
Run Migration
       ↓
Create Tables
       ↓
Create Indexes
       ↓
Seed Development Data
       ↓
Database Ready
```

---

# 32. Run Backend

Local:

```bash
cd apps/api
npm run dev
```

Backend:

```text
http://localhost:4000
```

ควรมี Health Check เช่น:

```http
GET /health
```

Response:

```json
{
  "success": true,
  "data": {
    "status": "ok"
  }
}
```

---

# 33. Run AI Service

Local:

```bash
cd services/ai
```

Activate Virtual Environment:

```bash
.venv\Scripts\activate
```

จากนั้น Start Service (FastAPI + Uvicorn ดู `docs/decisions/0004-ai-service.md`)

ตัวอย่าง:

```bash
python -m app.main
```

หรือ Command ที่ถูกกำหนดใน Project จริง

AI Service:

```text
http://localhost:8000
```

ต้องมี Health Check:

```http
GET /health
```

---

# 34. Run Frontend

Local:

```bash
cd apps/web
npm run dev
```

เปิด:

```text
http://localhost:3000
```

Frontend ต้องสามารถเรียก:

```text
http://localhost:4000/api
```

---

# 35. Full Local Startup

Development แบบ Local:

Terminal 1:

```bash
docker compose up -d postgres
```

Terminal 2:

```bash
cd apps/api
npm run dev
```

Terminal 3:

```bash
cd services/ai
.venv\Scripts\activate
python -m app.main
```

Terminal 4:

```bash
cd apps/web
npm run dev
```

จากนั้น:

```text
Browser
   ↓
localhost:3000
   ↓
Frontend
   ↓
localhost:4000
   ↓
Backend
   ├── localhost:5432 → PostgreSQL
   └── localhost:8000 → AI Service
```

---

# 36. Full Docker Startup

เมื่อ Docker Configuration พร้อม:

```bash
docker compose up --build
```

หรือ Background:

```bash
docker compose up -d --build
```

ตรวจสอบ:

```bash
docker compose ps
```

---

# 37. Stop Services

หยุด:

```bash
docker compose down
```

หากต้องการลบ Database Volume ด้วย ต้องใช้คำสั่งที่ระบุไว้ใน Project Documentation เท่านั้น

ไม่ควรลบ Volume โดยไม่ตั้งใจ เพราะอาจทำให้ Development Data หาย

---

# 38. Reset Development Database

ต้องมี Script:

```text
scripts/database/reset.sh
```

หรือคำสั่งที่เทียบเท่าสำหรับ Windows

การ Reset ต้อง:

```text
Stop
 ↓
Remove Development Database
 ↓
Create Database
 ↓
Migration
 ↓
Seed
```

ต้องมี Warning ก่อนลบข้อมูล

---

# 39. Health Check

ทุก Service สำคัญควรมี Health Check

Frontend:

```text
Application reachable
```

Backend:

```http
GET /health
```

AI:

```http
GET /health
```

Database:

```text
PostgreSQL connection check
```

---

# 40. System Health

Backend สามารถตรวจ:

```text
Backend
 ↓
PostgreSQL
 ↓
AI Service
```

ตัวอย่าง:

```json
{
  "success": true,
  "data": {
    "backend": "ok",
    "database": "ok",
    "ai_service": "ok"
  }
}
```

ห้ามเปิดข้อมูล Sensitive ผ่าน Health Check

---

# 41. Git Initialization

หาก Repository ยังไม่มี Git:

```bash
git init
```

จากนั้น:

```bash
git add .
```

และ:

```bash
git commit -m "chore: initialize project structure"
```

---

# 42. Git Remote

หลังสร้าง GitHub Repository:

```bash
git remote add origin <repository-url>
```

จากนั้น:

```bash
git push -u origin main
```

ห้ามใส่ URL จริงใน Documentation หาก Repository ยังไม่ได้สร้าง

---

# 43. Branch Strategy

แนะนำ:

```text
main
develop
feature/*
fix/*
docs/*
```

ตัวอย่าง:

```text
feature/session-api
feature/resume-parser
feature/career-matching
fix/resume-upload
docs/api-spec
```

---

# 44. Commit Convention

แนะนำ Conventional Commits

ตัวอย่าง:

```text
feat: add session API
feat: add resume upload
feat: implement skill extraction
fix: handle invalid portfolio URL
docs: update API specification
refactor: improve career matching service
test: add skill normalization tests
chore: update Docker configuration
```

---

# 45. Development Workflow

ทุก Feature:

```text
Create Branch
      ↓
Implement
      ↓
Run Tests
      ↓
Check Lint
      ↓
Check TypeScript
      ↓
Commit
      ↓
Push
      ↓
Review
      ↓
Merge
```

---

# 46. Code Quality Checks

Frontend และ Backend ต้องมี:

```text
TypeScript Check
Lint
Unit Tests
Build
```

Python ต้องมี:

```text
Syntax Check
Unit Tests
Dependency Check
```

---

# 47. Frontend Build

ตรวจสอบ:

```bash
npm run build
```

ต้องผ่านก่อน Deploy

---

# 48. Backend Build

TypeScript Backend ต้องสามารถ Build ได้

ตัวอย่าง:

```bash
npm run build
```

และ:

```bash
npm start
```

ต้องสามารถ Start Production Build ได้

---

# 49. AI Service Check

AI Service ต้องสามารถ:

```text
Start
 ↓
Health Check
 ↓
Receive JSON
 ↓
Process
 ↓
Return JSON
```

โดยไม่ต้องเข้าถึง Frontend โดยตรง

---

# 50. Database Check

ต้องตรวจสอบ:

```text
Connection
Migration
Indexes
Foreign Keys
Constraints
Seed
```

ให้ตรงกับ `DATABASE.md`

---

# 51. Development Environment Checklist

ก่อนเริ่ม Development:

* [ ] Git ติดตั้งแล้ว
* [ ] Node.js ติดตั้งแล้ว
* [ ] npm ใช้งานได้
* [ ] Python ติดตั้งแล้ว
* [ ] Docker ติดตั้งแล้ว
* [ ] Docker Compose ใช้งานได้
* [ ] Repository Clone แล้ว
* [ ] `.env` ถูกสร้าง
* [ ] Frontend dependencies ติดตั้งแล้ว
* [ ] Backend dependencies ติดตั้งแล้ว
* [ ] Python dependencies ติดตั้งแล้ว
* [ ] PostgreSQL ทำงาน
* [ ] Migration ผ่าน
* [ ] Seed ผ่าน
* [ ] Backend Health Check ผ่าน
* [ ] AI Health Check ผ่าน
* [ ] Frontend เปิดได้

---

# 52. First Setup Verification

เมื่อ Setup เสร็จ ต้องทดสอบ:

```text
Browser
   ↓
Next.js
   ↓
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

หากสอง Flow นี้ทำงานได้ ถือว่า Base Environment พร้อม

---

# 53. First Vertical Slice Environment Test

หลัง Environment พร้อม ให้ทดสอบ:

```text
Select Major
      ↓
POST /session
      ↓
PostgreSQL
      ↓
session_id
      ↓
Frontend
```

จากนั้น:

```text
Upload Resume
      ↓
Express
      ↓
Temporary Storage
      ↓
Python
      ↓
Extract Text
      ↓
Extract Basic Skills
      ↓
PostgreSQL
      ↓
Candidate Skill Profile
```

นี่คือ Vertical Slice แรกของระบบ

---

# 54. Troubleshooting

## PostgreSQL Connection Failed

ตรวจสอบ:

```text
Docker Container
Port
DATABASE_URL
Username
Password
Database Name
```

---

## Backend Cannot Reach AI

ตรวจสอบ:

```text
AI_SERVICE_URL
Docker Network
AI Container
AI Port
Health Check
```

---

## Frontend Cannot Reach Backend

ตรวจสอบ:

```text
NEXT_PUBLIC_API_BASE_URL
Backend Port
CORS
Backend Health Check
```

---

## Python Dependency Error

ตรวจสอบ:

```text
Python Version
Virtual Environment
requirements.txt
Library Compatibility
```

---

## Docker Container Stops

ตรวจสอบ:

```bash
docker compose logs
```

และ:

```bash
docker compose ps
```

ห้ามแก้ปัญหาด้วยการลบ Configuration โดยไม่ตรวจสอบ Root Cause

---

# 55. Security Rules

ห้าม:

```text
Commit .env
Commit API Key
Commit Database Password
Commit User Resume
Commit Private Portfolio Data
Commit Production Credentials
```

ห้ามเขียน:

```text
DATABASE_URL
```

แบบ Hard-coded ใน Source Code

ห้ามเขียน:

```text
API_KEY = "..."
```

ใน Source Code

---

# 56. Privacy Rules

Resume และ Portfolio ของ User ต้องถือเป็น User Data

ดังนั้น:

```text
Temporary
 ↓
Process
 ↓
Result
 ↓
Retention
 ↓
Delete
```

ข้อมูล User ไม่ควรถูกใช้เป็น Demo Dataset โดยอัตโนมัติ

หากต้องนำไปใช้เป็น Evaluation Dataset ต้องมีขั้นตอนด้าน Privacy และการอนุญาตที่เหมาะสม

---

# 57. Production Environment

Production ต้องแยกจาก Development

```text
Development
≠
Production
```

Production ต้องมี:

```text
Production Database
Production Secrets
Production Environment Variables
Production Storage
Production Logs
```

ห้ามใช้ Development Credentials ใน Production

---

# 58. Production Deployment Principle

Architecture:

```text
Internet
   ↓
Frontend
   ↓
Backend API
   ├── PostgreSQL
   └── AI Service
```

PostgreSQL และ AI Service ไม่ควรเปิด Public โดยไม่จำเป็น

---

# 59. Environment Separation

อย่างน้อย:

```text
development
testing
production
```

Configuration ต้องแยกกัน

ตัวอย่าง:

```text
.env.development
.env.test
.env.production
```

แต่ Secret จริงต้องใช้ Secret Management ของ Environment/Platform ที่ Deploy

---

# 60. Testing Environment

Test ต้องไม่ใช้ Production Database

ควรมี:

```text
Test Database
Test Dataset
Test Storage
```

เพื่อป้องกันข้อมูลจริงเสียหาย

---

# 61. Data Version

Dataset ต้องมี Version

ตัวอย่าง:

```text
DATASET_VERSION=2026-01
```

Algorithm ต้องมี Version:

```text
ALGORITHM_VERSION=career-matching-v1
```

ทุก Career Analysis ต้องสามารถ Trace ได้ว่าใช้ Version ใด

---

# 62. Documentation Source of Truth

Environment Setup ต้องสอดคล้องกับ:

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
```

หากมีความขัดแย้ง:

```text
Architecture
→ TECH_STACK.md

Database
→ DATABASE.md

API
→ API.md

AI/NLP
→ AI_MATCHING_SPEC.md

Dataset
→ DATASET_SPEC.md

UI/UX
→ UI_UX_SPEC.md

Development Process
→ IMPLEMENTATION_PLAN.md

Folder Structure
→ FOLDER_STRUCTURE.md
```

จากนั้นต้องแก้เอกสารที่เกี่ยวข้องให้กลับมาสอดคล้องกัน

---

# 63. Claude Setup Instructions

เมื่อให้ Claude เริ่ม Project:

## Step 1

อ่าน:

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
```

## Step 2

ตรวจสอบ Environment

```text
Node.js
Python
Docker
Git
```

## Step 3

สร้าง Root Project

## Step 4

สร้าง Folder Structure

## Step 5

สร้าง Docker Compose

## Step 6

สร้าง PostgreSQL

## Step 7

สร้าง Migration

## Step 8

สร้าง Backend Skeleton

## Step 9

สร้าง Python Skeleton

## Step 10

สร้าง Frontend Skeleton

## Step 11

สร้าง Health Check

## Step 12

ทดสอบ Service Communication

---

# 64. Claude Must Not Do

Claude ห้าม:

```text
สร้าง PHP Backend
```

ห้าม:

```text
สร้าง MariaDB
```

ห้าม:

```text
เปลี่ยน PostgreSQL เป็น MongoDB
```

ห้าม:

```text
สร้าง Next.js API เป็น Main Backend แทน Express
```

ห้าม:

```text
ให้ Frontend ติดต่อ PostgreSQL โดยตรง
```

ห้าม:

```text
ให้ Frontend ติดต่อ Python โดยตรง
```

ห้าม:

```text
สร้าง Backend สองชุดที่ทำหน้าที่ซ้ำกัน
```

ห้าม:

```text
Hard-code Secret
```

ห้าม:

```text
Hard-code Labour Market Demand
```

---

# 65. First Development Milestone

Milestone แรกยังไม่ใช่ Career Prediction

ต้องทำให้:

```text
Project Starts
      ↓
Docker Works
      ↓
PostgreSQL Works
      ↓
Backend Works
      ↓
Python Works
      ↓
Frontend Works
      ↓
Frontend ↔ Backend
      ↓
Backend ↔ PostgreSQL
      ↓
Backend ↔ Python
```

ครบก่อน

---

# 66. Definition of Done

Environment Setup ถือว่าสมบูรณ์เมื่อ:

* [ ] Project Clone ได้
* [ ] Frontend Install ได้
* [ ] Backend Install ได้
* [ ] Python Environment พร้อม
* [ ] Docker Compose ทำงาน
* [ ] PostgreSQL ทำงาน
* [ ] Migration ทำงาน
* [ ] Seed ทำงาน
* [ ] Backend Start ได้
* [ ] Python Start ได้
* [ ] Frontend Start ได้
* [ ] Backend Health Check ผ่าน
* [ ] AI Health Check ผ่าน
* [ ] Frontend เรียก Backend ได้
* [ ] Backend เชื่อม PostgreSQL ได้
* [ ] Backend เชื่อม Python ได้
* [ ] Environment Variables ถูกต้อง
* [ ] Secrets ไม่อยู่ใน Git
* [ ] User Data ไม่อยู่ใน Git
* [ ] Test Environment แยกจาก Production
* [ ] First Vertical Slice สามารถเริ่มพัฒนาได้

---

# 67. Final Development Command Concept

Local Development:

```bash
# Terminal 1
docker compose up -d postgres

# Terminal 2
cd apps/api
npm install
npm run dev

# Terminal 3
cd services/ai
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m app.main

# Terminal 4
cd apps/web
npm install
npm run dev
```

Docker Development:

```bash
docker compose up --build
```

ตรวจสอบ:

```bash
docker compose ps
```

---

# 68. Final Environment Architecture

```text
┌─────────────────────────────────────────────────────┐
│                  Development PC                     │
│                                                     │
│  ┌────────────┐                                     │
│  │  Browser   │                                     │
│  └─────┬──────┘                                     │
│        │                                             │
│        ▼                                             │
│  ┌────────────┐                                     │
│  │  Next.js   │ :3000                              │
│  └─────┬──────┘                                     │
│        │ REST API                                   │
│        ▼                                             │
│  ┌────────────┐                                     │
│  │  Express   │ :4000                              │
│  └──┬──────┬──┘                                     │
│     │      │                                        │
│     │      ▼                                        │
│     │  ┌────────────┐                               │
│     │  │ Python AI  │ :8000                         │
│     │  └────────────┘                               │
│     │                                               │
│     ▼                                               │
│  ┌────────────┐                                     │
│  │ PostgreSQL │ :5432                              │
│  └────────────┘                                     │
│                                                     │
│                 Docker Compose                      │
└─────────────────────────────────────────────────────┘
```

---

# 69. Document Status

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

API Architecture:
Next.js → Express
Express → PostgreSQL
Express → Python

Folder Structure:
LOCKED

Environment Setup:
LOCKED

Semester 1:
Creative Media Technology → Web Full Stack Pilot

Semester 2:
Whole Faculty Expansion
```

---

# END OF ENVIRONMENT_SETUP.md