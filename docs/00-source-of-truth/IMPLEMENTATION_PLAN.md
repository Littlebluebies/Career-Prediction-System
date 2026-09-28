# IMPLEMENTATION_PLAN.md

# Career Prediction and Skill Gap Analysis System

## Implementation Plan & Development Roadmap

> **Document Status:** LOCKED
> **Purpose:** กำหนดลำดับและวิธีการพัฒนาระบบจริงตั้งแต่เริ่มต้นจนถึงการประเมินผล
> **Related Documents:** `PROJECT_SPEC.md`, `DATABASE.md`, `DATASET_SPEC.md`, `AI_MATCHING_SPEC.md`, `UI_UX_SPEC.md`, `TECH_STACK.md`

---

# 1. Implementation Objective

เอกสารนี้กำหนดแผนการพัฒนาระบบ

> **ระบบทำนายอาชีพสำหรับนักศึกษาคณะเทคโนโลยีสื่อสารมวลชนโดยอิงการวิเคราะห์ทักษะและความต้องการของตลาดแรงงาน**

โดยเปลี่ยน Specification ของระบบให้เป็นลำดับการพัฒนาที่สามารถนำไปปฏิบัติจริงได้

ระบบต้องสามารถทำงานตั้งแต่:

```text id="w5p3ap"
User Input
 ↓
Resume + Portfolio
 ↓
Skill Extraction
 ↓
Evidence Analysis
 ↓
Candidate Skill Profile
 ↓
Labour Market Analysis
 ↓
Career Matching
 ↓
Career Recommendation
 ↓
Skill Gap
 ↓
Development Guidance
 ↓
User Feedback
```

---

# 2. Development Philosophy

หลักการพัฒนา:

> **Data First → Architecture → Core Processing → Matching → UI → Evaluation**

ห้ามเริ่มต้นด้วยการสร้าง AI Model ที่ซับซ้อนทันที

ลำดับที่ถูกต้องคือ:

```text id="l0d6zj"
Database
 ↓
Dataset
 ↓
Skill Taxonomy
 ↓
Occupation Framework
 ↓
Labour Market Data
 ↓
Resume / Portfolio Processing
 ↓
Skill Extraction
 ↓
Candidate Profile
 ↓
Matching
 ↓
Skill Gap
 ↓
Explanation
 ↓
API
 ↓
Frontend
 ↓
Evaluation
```

---

# 3. Overall Development Phases

ระบบแบ่งเป็น 14 Phases (Phase 0-13)

```text id="z5xk8y"
Phase 0  Project Setup
Phase 1  Database
Phase 2  Reference Data (Knowledge Dataset)
Phase 3  Labour Market Dataset
Phase 4  Resume Processing
Phase 5  Portfolio Processing
Phase 6  Skill & Evidence Pipeline
Phase 7  Career Matching
Phase 8  Skill Gap & Guidance
Phase 9  Backend API
Phase 10 Frontend
Phase 11 Integration & Testing
Phase 12 Evaluation
Phase 13 Deployment
```

เลข Phase นี้ตรงกับ `CLAUDE.md` §8 ดู `docs/decisions/0002-phase-numbering-and-semester-1-scope.md`

---

# 4. Phase 0 — Project Setup

## Objective

สร้าง Development Environment ก่อนเริ่มพัฒนาระบบ

## Tasks

### 0.1 Create Repository

สร้าง GitHub Repository

```text id="h9x4tb"
Career-Prediction-System
```

### 0.2 Create Project Structure

```text id="l3c1i9"
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
│
├── .env.example
├── .gitattributes
├── .gitignore
├── CLAUDE.md
├── docker-compose.yml
└── README.md
```

### 0.3 Initialize Git

```text id="9oj5zv"
main
develop
```

สร้าง feature branch สำหรับงานแต่ละส่วน

### 0.4 Docker

สร้าง Services:

```text id="h8ym1g"
frontend
backend
ai-service
postgres
```

Dockerfile ของแต่ละ Service อยู่ในโฟลเดอร์ของ Service นั้น (`apps/web`, `apps/api`, `services/ai`)

### 0.5 Environment

สร้าง:

```text id="5o1pmm"
.env
.env.example
```

ห้าม Commit `.env`

---

## Acceptance Criteria

* Repository ทำงานได้
* Docker Compose Start ได้
* PostgreSQL Start ได้
* Frontend Start ได้
* Backend Start ได้
* Python Service Start ได้
* ทุก Service ติดต่อกันได้ใน Development Environment

---

# 5. Phase 1 — Database

## Objective

สร้าง PostgreSQL Database ตาม `DATABASE.md`

---

## 5.1 Database Schema

สร้าง Schema:

```sql
career_system
```

---

## 5.2 Core Tables

สร้าง:

```text id="5jv9b1"
major
user_session
resume
portfolio
portfolio_project

skill
skill_alias
user_skill
skill_evidence

career_family
occupation
occupation_alias
occupation_skill

job_posting
job_posting_skill

dataset_version

career_result
skill_gap
user_feedback
```

---

## 5.3 Migration

Migration ต้องรองรับ:

```text id="1g1i3v"
Create
Rollback
Update
Version
```

---

## 5.4 Seed Data

สร้าง Seed สำหรับ Development

อย่างน้อย:

```text id="q4t2ar"
4 Faculty Branches
Career Families
Sample Skills
Sample Occupations
Sample Aliases
```

Seed Data ต้องแยกจาก Production Dataset

---

## Acceptance Criteria

สามารถ:

```text id="3h8j2y"
docker compose up
 ↓
migration
 ↓
database ready
 ↓
seed
```

และตรวจสอบ Foreign Keys / Constraints / Indexes ได้

---

# 6. Phase 2 — Knowledge Dataset

## Objective

สร้าง Knowledge Base ของระบบ

ประกอบด้วย:

```text id="z3g3e8"
Skill Taxonomy
Skill Alias
Career Family
Occupation
Occupation Alias
Occupation Skill
```

---

# 7. Skill Taxonomy

สร้าง Canonical Skill Dictionary

ตัวอย่าง:

```text id="f9xv3r"
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
Photoshop
Illustrator

UI Design
UX Design
Typography
Layout

Storytelling
Creative Thinking
Video Production
Communication
```

แต่รายการจริงต้องผ่าน Dataset Process

---

# 8. Skill Alias

ตัวอย่าง:

```text id="9xgk0h"
React.js
ReactJS
React JS
→ React
```

และ:

```text id="v5qz4u"
Adobe Photoshop
Photoshop
PS
→ Adobe Photoshop
```

---

# 9. Occupation Framework

สร้าง Candidate Occupation จาก:

```text id="q3m2ps"
ESCO / O*NET
+
Thai Labour Market
```

จากนั้น Normalize

---

# 10. Career Families

Initial Framework:

```text id="k8j6h4"
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

รายการสุดท้ายสามารถเปลี่ยนตามข้อมูลจริง

---

# 11. Occupation Alias

ตัวอย่าง:

```text id="wz7s5g"
Frontend Developer
Front-end Developer
Frontend Engineer
Junior Frontend Developer
```

ต้อง Map ไปยัง Canonical Occupation ที่เหมาะสม

---

# 12. Phase 3 — Labour Market Dataset

## Objective

สร้าง Dataset จาก Job Posting จริง

---

# 13. Data Collection

เก็บ:

```text id="d7c1bs"
Job Title
Company
Description
Requirements
Experience
Location
Source
Source URL
Date Collected
```

---

# 14. Job Posting Processing

Pipeline:

```text id="8g1r6m"
Raw Job Posting
 ↓
Cleaning
 ↓
Deduplication
 ↓
Job Title Normalization
 ↓
Skill Extraction
 ↓
Skill Normalization
 ↓
Occupation Mapping
 ↓
Database
```

---

# 15. Skill Demand

คำนวณจากข้อมูลที่เก็บจริง

ตัวอย่างแนวคิด:

```text id="j9w2jv"
Skill Frequency
        ↓
Demand Signal
```

ห้ามกำหนด:

```text
React = 80%
```

โดยไม่มีข้อมูลรองรับ

---

# 16. Occupation-Skill Profile

สร้าง:

```text id="l1v6h8"
Occupation
+
Skill
+
Importance
+
Demand
```

ตัวเลขต้องมี Source หรือ Methodology รองรับ

---

# 17. Dataset Version

ทุก Dataset ต้องมี Version

ตัวอย่าง:

```text id="m5z2fr"
dataset_version = 2026_xx
```

Version จริงขึ้นอยู่กับรอบการเก็บข้อมูล

---

# 18. Phase 4 — Resume Processing

## Objective

สร้างระบบอ่าน Resume

---

# 19. Resume Input

รองรับ:

```text id="p2x4b7"
PDF
DOC
DOCX
```

---

# 20. Resume Pipeline

```text id="3m0qtx"
Upload
 ↓
Validation
 ↓
Temporary Storage
 ↓
Text Extraction
 ↓
Text Cleaning
 ↓
Section Detection
 ↓
Skill Extraction
 ↓
Evidence Extraction
```

---

# 21. Resume Sections

พยายามตรวจจับ:

```text id="t7w2ks"
Education
Experience
Projects
Skills
Certificates
Activities
```

ไม่จำเป็นต้องดึงข้อมูลส่วนบุคคลที่ไม่เกี่ยวข้อง

---

# 22. Resume Output

ตัวอย่าง:

```json id="k2r5hf"
{
  "skills": [
    {
      "skill": "React",
      "confidence": 0.91,
      "source": "RESUME"
    }
  ]
}
```

และ Evidence:

```json id="2n5d1a"
{
  "skill": "React",
  "evidence_type": "RESUME_PROJECT",
  "evidence_text": "Developed a web application using React"
}
```

---

# 23. Phase 5 — Portfolio Processing

## Objective

วิเคราะห์ Portfolio URL

---

# 24. Portfolio Flow

```text id="p9c3mv"
URL
 ↓
Validation
 ↓
Access
 ↓
Content Extraction
 ↓
Project Detection
 ↓
Technology Detection
 ↓
Skill Extraction
 ↓
Evidence
```

---

# 25. Portfolio Status

รองรับ:

```text id="v1v6mw"
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

# 26. Portfolio Evidence

ตัวอย่าง:

```text id="5v3z8f"
Project:
E-Commerce Website

Technology:
React
Node.js
PostgreSQL

Evidence:
GitHub Project
```

Skill ต้องเชื่อมกับ Evidence

---

# 27. Portfolio Safety

ต้องป้องกัน:

```text id="9g8z2n"
SSRF
Private IP Access
Localhost Access
Large Response
Infinite Redirect
Timeout
```

---

# 28. Phase 6 — Skill & Evidence Pipeline

## Objective

รวมข้อมูลจาก Resume และ Portfolio

---

# 29. Extraction Pipeline

```text id="q9m4zs"
Raw Text
 ↓
Text Cleaning
 ↓
Skill Detection
 ↓
Skill Extraction
 ↓
Skill Normalization
 ↓
Confidence
 ↓
Evidence
```

---

# 30. Skill Normalization

ตัวอย่าง:

```text id="e1n7sm"
React.js
ReactJS
React JS
        ↓
React
```

---

# 31. Candidate Skill Profile

รวม:

```text id="3h7s8n"
Resume Skills
+
Portfolio Skills
+
Evidence
+
Confidence
```

เป็น:

```text id="k6f2qj"
Candidate Skill Profile
```

---

# 32. Evidence Model

ตัวอย่าง:

| Skill     | Resume | Portfolio | Evidence        |
| --------- | -----: | --------: | --------------- |
| HTML      |      ✓ |         ✓ | Website Project |
| React     |      ✓ |         ✓ | GitHub Project  |
| Figma     |      ✕ |         ✓ | UI Prototype    |
| Photoshop |      ✕ |         ✓ | Graphic Project |

---

# 33. Evidence Rule

หลักสำคัญ:

```text id="d8g1e5"
Skill
 ↓
Evidence
 ↓
Source
```

ไม่ใช่:

```text id="7j9n2r"
Skill
 ↓
AI Guess
```

---

# 34. Phase 7 — Career Matching

## Objective

สร้าง Career Matching Engine

---

# 35. Matching Input

```text id="5v9d2k"
Candidate Skill Profile
+
Occupation Skill Profile
+
Labour Market Signal
+
Evidence Confidence
```

---

# 36. Matching Pipeline

```text id="7h1x4q"
Candidate Profile
 ↓
Compare Occupations
 ↓
Skill Matching
 ↓
Evidence Strength
 ↓
Market Relevance
 ↓
Career Score
 ↓
Ranking
```

---

# 37. Cross-Major Matching

Major ใช้เป็น Context เท่านั้น

ตัวอย่าง:

```text id="c6v9hz"
Creative Media
+
React
+
Figma
+
UI Evidence
```

สามารถได้รับ:

```text
UI/UX Designer
```

แม้ Career จะไม่ใช่อาชีพที่ตรงกับชื่อ Major โดยตรง

---

# 38. No Hard Filter

ห้าม:

```text id="d1p7v5"
IF Major = Web
THEN only Web Careers
```

ต้อง:

```text id="f4x8z0"
Major
 ↓
Context Signal
 ↓
All Relevant Occupations
 ↓
Ranking
```

---

# 39. Ranking

ระบบแสดง:

```text id="s7n2w5"
Top 3–5 Careers
```

แต่ K ควรเป็น Configuration

เช่น:

```text
TOP_K_CAREERS
```

---

# 40. Explainability

Career Result ต้องแสดง:

```text id="x7v4qk"
Career
Match Score
Matched Skills
Evidence
Market Skills
Explanation
```

---

# 41. Example Explanation

ตัวอย่างโครงสร้าง:

```text id="k9r3bx"
แนะนำอาชีพ Front-end Developer

เหตุผล:
• ตรวจพบ HTML และ CSS
• ตรวจพบ JavaScript และ React
• มีหลักฐานจาก Web Project
• Skills เหล่านี้ปรากฏในข้อมูลประกาศงานที่ใช้วิเคราะห์

Skill ที่ควรพัฒนา:
• TypeScript
• Testing
• Accessibility
```

ข้อความจริงต้องสร้างจาก Evidence และ Dataset

---

# 42. Phase 8 — Skill Gap & Guidance

## Objective

ระบุ Skill Gap และแนะนำแนวทางพัฒนา

---

# 43. Skill Gap Pipeline

```text id="r8y1z2"
Occupation Required Skills
        -
Candidate Evidenced Skills
        ↓
Skill Gap
        ↓
Priority
```

---

# 44. Skill Gap Status

```text id="s2f5na"
MATCHED
PARTIAL
EVIDENCE_NOT_FOUND
```

---

# 45. Priority

```text id="g6x8r3"
HIGH
MEDIUM
LOW
```

Priority ต้องอ้างอิงจาก:

```text id="a9v2s5"
Skill Importance
+
Labour Market Demand
+
Matching Context
```

ไม่กำหนดแบบสุ่ม

---

# 46. Guidance

รูปแบบ:

```text id="n5k8w1"
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
TypeScript

Learn:
TypeScript Fundamentals

Practice:
ใช้ TypeScript กับ React

Build:
สร้าง Web Application

Document:
เพิ่ม Project ลง Portfolio
```

---

# 47. Phase 9 — Backend API

## Objective

เชื่อม Database, AI และ Frontend

---

# 48. API Modules

```text id="r5p3y7"
Session
Resume
Portfolio
Analysis
Career
Skill Gap
Feedback
```

---

# 49. Core API

## Create Session

```http
POST /api/session
```

Input:

```json id="8s1k5p"
{
  "major_id": 1
}
```

---

## Upload Resume

```http
POST /api/resume
```

---

## Submit Portfolio

```http
POST /api/portfolio
```

---

## Start Analysis

```http
POST /api/analyze
```

---

## Get Analysis

```http
GET /api/analysis/:session_id
```

---

## Get Career

```http
GET /api/career/:result_id
```

---

## Get Skill Gap

```http
GET /api/skill-gap/:result_id
```

---

## Submit Feedback

```http
POST /api/feedback
```

Actual API Contract ต้องจัดทำใน `API.md`

---

# 50. API Processing Flow

```text id="f7c9s2"
Frontend
 ↓
POST /api/analyze
 ↓
Express
 ↓
Validate
 ↓
Load Session
 ↓
Load Resume
 ↓
Load Portfolio
 ↓
Python AI Service
 ↓
Matching
 ↓
Skill Gap
 ↓
Save Result
 ↓
Return Status
```

---

# 51. Phase 10 — Frontend

## Objective

สร้าง User Experience ตาม `UI_UX_SPEC.md`

---

# 52. Frontend Pages

```text id="3x7h8m"
Home
 ↓
Analysis Input
 ↓
Major Selection
 ↓
Resume Upload
 ↓
Portfolio Input
 ↓
Privacy Consent
 ↓
Processing
 ↓
Analysis Overview
 ↓
Career Results
 ↓
Career Detail
 ↓
Skill Gap
 ↓
Development Guidance
 ↓
Feedback / SUS
 ↓
Completion
```

---

# 53. Frontend Components

สร้าง Reusable Components:

```text id="q8v5x2"
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
Modal
Alert
Toast
LoadingState
EmptyState
```

---

# 54. Analysis Page

ต้องรับ:

```text id="h5q7z3"
Major
Resume
Portfolio
Consent
```

ก่อนเริ่ม Analysis

---

# 55. Processing Page

แสดง:

```text id="j6m8p1"
Validating
Parsing Resume
Analyzing Portfolio
Extracting Skills
Normalizing Skills
Building Profile
Matching Careers
Ranking Results
Analyzing Gaps
Generating Guidance
```

---

# 56. Career Results Page

แต่ละ Career Card แสดง:

```text id="q1r8s4"
Rank
Occupation
Career Family
Match Score
Matched Skills
Evidence
Market Signal
Why Recommended
```

---

# 57. Career Detail

แสดง:

```text id="y6x3c9"
Why this career
Matched Skills
Evidence
Market Demand
Required Skills
Skill Gap
Development Guidance
```

---

# 58. Skill Gap Page

แสดง:

```text id="k7s2v5"
Skill
Status
Priority
Reason
Market Relevance
How to Develop
```

---

# 59. Feedback Page

เก็บ:

```text id="p8x1m4"
SUS
Satisfaction
Optional Comment
```

SUS ต้องใช้โครงสร้างมาตรฐาน

---

# 60. Phase 11 — Integration & Testing

## Objective

รวมทุก Service และทดสอบ End-to-End

---

# 61. Integration

```text id="c9v3x7"
Next.js
    ↕
Express
    ↕
Python
    ↕
PostgreSQL
```

ต้องทดสอบทั้ง Success และ Error Flow

---

# 62. Unit Tests

อย่างน้อย:

```text id="g2m7k9"
Skill normalization
Alias mapping
Input validation
Score calculation
Ranking
Skill gap
Priority
```

---

# 63. Integration Tests

ทดสอบ:

```text id="v8s4n2"
Backend → Database
Backend → Python
Python → Backend
```

---

# 64. End-to-End Tests

Test Scenario:

```text id="n7q5m3"
Select Major
 ↓
Create Session
 ↓
Upload Resume
 ↓
Submit Portfolio
 ↓
Consent
 ↓
Analyze
 ↓
View Career Results
 ↓
View Career Detail
 ↓
View Skill Gap
 ↓
Submit Feedback
```

---

# 65. Error Test Cases

ต้องทดสอบ:

```text id="t5k8p2"
Invalid File
Large File
Corrupted File
Invalid URL
Private Portfolio
Blocked Portfolio
Login Required
AI Timeout
Database Error
No Skills Found
Insufficient Evidence
No Strong Match
```

---

# 66. Phase 12 — Evaluation

## Objective

ประเมินประสิทธิภาพระบบตาม Research Methodology

---

# 67. Skill Extraction Evaluation

Metrics:

```text id="a8n3c6"
Precision
Recall
F1-score
```

เปรียบเทียบ:

```text
Expected Skill
vs
Detected Skill
```

---

# 68. Career Recommendation Evaluation

Metrics:

```text id="z4x7k1"
Top-1 Accuracy
Top-3 Hit Rate
Precision@K
```

ต้องกำหนด Ground Truth อย่างเหมาะสม

---

# 69. Usability Evaluation

ใช้:

```text id="w3m9s5"
System Usability Scale (SUS)
```

และ:

```text
User Satisfaction
```

---

# 70. Optional Expert Validation

สามารถใช้ผู้เชี่ยวชาญตรวจสอบ:

```text id="v5q8n2"
Occupation
Skill Requirements
Occupation-Skill Relationship
Recommendation Reason
```

ผู้เชี่ยวชาญเป็นผู้ตรวจสอบความเหมาะสม ไม่ใช่ผู้กำหนด Dataset ทั้งหมดจากความคิดเห็นส่วนตัว

---

# 71. Evaluation Dataset

สร้าง:

```text id="p4k7x9"
Resume
Expected Skills
Expected Career
System Result
```

เพื่อใช้ประเมิน

---

# 72. Phase 13 — Deployment

หลังจาก Development และ Evaluation เสร็จ

```text id="q5v8n1"
GitHub
 ↓
Build
 ↓
Docker Image
 ↓
Deployment Environment
 ↓
PostgreSQL
 ↓
Backend
 ↓
AI Service
 ↓
Frontend
```

---

# 73. Deployment Checklist

ก่อน Deploy:

```text id="r7k2m5"
Environment Variables
Database Migration
Production Database
CORS
File Upload Limits
Security
Logging
Error Handling
Backup
Retention Policy
```

---

# 74. Development Milestones

แบ่ง Milestone สำคัญดังนี้:

## M1 — Infrastructure Ready

```text id="m1a2b3"
GitHub
Docker
PostgreSQL
Next.js
Express
Python
```

---

## M2 — Database Ready

```text id="m2c3d4"
Schema
Migration
Seed
```

---

## M3 — Dataset Ready

```text id="m3e4f5"
Skills
Occupations
Job Postings
Occupation-Skill
```

---

## M4 — Analysis Ready

```text id="m4g5h6"
Resume
Portfolio
Skill Extraction
Evidence
```

---

## M5 — Recommendation Ready

```text id="m5i6j7"
Matching
Ranking
Explanation
```

---

## M6 — Skill Gap Ready

```text id="m6k7l8"
Gap
Priority
Guidance
```

---

## M7 — UI Ready

```text id="m7m8n9"
Complete User Flow
```

---

## M8 — Evaluation Ready

```text id="m8o9p0"
Metrics
Ground Truth
SUS
```

---

# 75. Semester 1 Implementation

## Scope

Pilot:

> Creative Media Technology — Web Full Stack

---

## Semester 1 Minimum Viable System

ต้องสามารถ:

```text id="s1v1x2"
Select Major
 ↓
Upload Resume
 ↓
Submit Portfolio
 ↓
Extract Skills
 ↓
Build Candidate Profile
 ↓
Match Web-related + Cross-Major Occupations
 ↓
Show Top Careers
 ↓
Explain Recommendation
 ↓
Skill Gap
 ↓
Guidance
```

ลำดับการสร้าง: เริ่มจาก Vertical Slice (Major → Session → Resume → Candidate Skill Profile) ตาม `FOLDER_STRUCTURE.md` §52 และ `CLAUDE.md` §15 แล้วต่อยอดจนครบ MVP นี้

---

# 76. Semester 1 Priority Occupations

เริ่มจาก Occupations ที่เกี่ยวข้องกับ Web Full Stack และใกล้เคียง เช่น:

```text id="s1o1p2"
Front-end Developer
Back-end Developer
Full-stack Developer
Web Developer
Web Application Developer
UI/UX Designer
UX Engineer
Product Designer
```

รายการจริงต้องผ่าน Occupation Framework และ Dataset Process

---

# 77. Semester 2 Expansion

ขยายจาก Pilot ไปทั้งคณะ:

```text id="s2x1y2"
Film & Radio Television
Advertising & Public Relations
Digital Printing & Packaging
Creative Media Technology
```

รวม:

```text id="s2x3y4"
Web Full Stack
Game Development
```

---

# 78. Semester 2 Expansion Strategy

ไม่สร้างระบบใหม่

ใช้:

```text id="s2a5b6"
Same Frontend
Same Backend
Same AI Engine
Same Database Architecture
```

เพิ่ม:

```text id="s2c7d8"
Major Data
Occupation Data
Skill Data
Job Market Data
```

---

# 79. Priority Order

หากเวลาไม่พอ ให้รักษา Feature ตามลำดับ:

```text id="p1q2r3"
1. Resume Processing
2. Portfolio Processing
3. Skill Extraction
4. Skill Normalization
5. Evidence
6. Candidate Profile
7. Career Matching
8. Explainability
9. Skill Gap
10. Guidance
11. UI
12. Advanced AI
```

Advanced AI ไม่ควรมาก่อน Core System

---

# 80. MVP Definition

MVP ต้องสามารถ:

```text id="mvp001"
Input
 ↓
Resume
 +
Portfolio
 ↓
Skill Profile
 ↓
Career Matching
 ↓
Top 3–5 Careers
 ↓
Explanation
 ↓
Skill Gap
```

ระบบที่ไม่มี Skill Gap หรือ Evidence ไม่ถือว่าเป็น MVP ที่สมบูรณ์ตาม Project Concept

---

# 81. Feature Priority

## Must Have

```text id="must01"
No Login
Major Selection
Resume Upload
Portfolio URL
Privacy Consent
Resume Parsing
Portfolio Analysis
Skill Extraction
Skill Normalization
Evidence
Candidate Profile
Occupation Framework
Labour Market Data
Career Matching
Ranking
Explainability
Skill Gap
Guidance
SUS
```

## Should Have

```text id="should1"
Career Comparison
Skill Visualization
Processing Progress
Dataset Dashboard
Advanced Evidence View
```

## Could Have

```text id="could01"
Embedding Search
Advanced Semantic Similarity
Additional Portfolio Sources
Advanced Analytics
```

---

# 82. What Must Not Be Done

ห้าม:

```text id="no001"
สร้าง Login โดยไม่จำเป็น
```

ห้าม:

```text id="no002"
ใช้ Major เป็น Hard Filter
```

ห้าม:

```text id="no003"
ทำนาย Employment Probability
```

ห้าม:

```text id="no004"
สร้าง Labour Market Demand แบบสมมติ
```

ห้าม:

```text id="no005"
สร้าง Evidence ที่ไม่มีใน Input
```

ห้าม:

```text id="no006"
บอกว่า User ไม่มี Skill เพียงเพราะไม่พบใน Resume
```

ห้าม:

```text id="no007"
ให้ Frontend คำนวณ Final Career Score
```

ห้าม:

```text id="no008"
ให้ Next.js และ Express เป็น Main Backend พร้อมกัน
```

ห้าม:

```text id="no009"
ให้ Python กลายเป็น Main Web Backend
```

ห้าม:

```text id="no010"
ใช้ MongoDB เป็น Main Database
```

ห้าม:

```text id="no011"
ใช้ MySQL/MariaDB เป็น Main Database
```

---

# 83. Definition of Done — Full System

ระบบถือว่าพัฒนาเสร็จเมื่อ:

### Infrastructure

* Docker ทำงานได้
* Services Start ได้
* Environment Configuration ทำงาน

### Database

* Migration สำเร็จ
* Schema ถูกต้อง
* Constraints ทำงาน
* Dataset Import ได้

### Data

* Skill Taxonomy พร้อม
* Occupation Framework พร้อม
* Labour Market Dataset พร้อม
* Dataset Version พร้อม

### AI/NLP

* Resume Parsing ทำงาน
* Portfolio Processing ทำงาน
* Skill Extraction ทำงาน
* Normalization ทำงาน
* Evidence ทำงาน
* Candidate Profile ทำงาน

### Recommendation

* Matching ทำงาน
* Ranking ทำงาน
* Explainability ทำงาน
* Cross-Major ทำงาน

### Skill Gap

* Gap Analysis ทำงาน
* Priority ทำงาน
* Guidance ทำงาน

### Frontend

* User Flow ครบ
* Responsive
* Error Handling
* Processing State
* Results
* Feedback

### Evaluation

* Skill Extraction Metrics
* Recommendation Metrics
* SUS
* User Satisfaction

### Documentation

* README
* API
* Database
* Dataset
* AI Methodology
* UI/UX
* Technology Stack
* Implementation Plan

---

# 84. Final Development Flow

```text id="final01"
┌───────────────────────┐
│  PROJECT SETUP        │
│ Git + Docker          │
└───────────┬───────────┘
            ↓
┌───────────────────────┐
│  DATABASE             │
│ PostgreSQL            │
└───────────┬───────────┘
            ↓
┌───────────────────────┐
│  KNOWLEDGE DATA       │
│ Skill + Occupation    │
└───────────┬───────────┘
            ↓
┌───────────────────────┐
│  LABOUR MARKET        │
│ Job Posting           │
└───────────┬───────────┘
            ↓
┌───────────────────────┐
│  INPUT PROCESSING     │
│ Resume + Portfolio    │
└───────────┬───────────┘
            ↓
┌───────────────────────┐
│  SKILL + EVIDENCE     │
│ Candidate Profile     │
└───────────┬───────────┘
            ↓
┌───────────────────────┐
│  CAREER MATCHING      │
│ Ranking + Explain     │
└───────────┬───────────┘
            ↓
┌───────────────────────┐
│  SKILL GAP            │
│ Guidance              │
└───────────┬───────────┘
            ↓
┌───────────────────────┐
│  FRONTEND             │
│ Complete UX           │
└───────────┬───────────┘
            ↓
┌───────────────────────┐
│  TESTING              │
│ Unit + Integration    │
│ + E2E                 │
└───────────┬───────────┘
            ↓
┌───────────────────────┐
│  EVALUATION           │
│ F1 + Top-K + SUS      │
└───────────┬───────────┘
            ↓
┌───────────────────────┐
│  DEPLOYMENT           │
└───────────────────────┘
```

---

# 85. Claude Execution Protocol

Claude ต้องพัฒนาระบบตาม Phase ไม่ควรสร้างทุกอย่างในครั้งเดียว

เมื่อเริ่มแต่ละ Phase:

1. อ่าน `PROJECT_SPEC.md`
2. อ่าน `TECH_STACK.md`
3. อ่านเอกสารที่เกี่ยวข้องกับ Phase
4. ตรวจสอบโครงสร้าง Repository ปัจจุบัน
5. ตรวจสอบสิ่งที่พัฒนาไปแล้ว
6. ทำเฉพาะงานของ Phase
7. Test
8. รายงานผล
9. Update Documentation
10. Commit

---

# 86. Claude Task Format

เมื่อสั่ง Claude ให้ทำงาน ควรใช้รูปแบบ:

```text
Read:
- PROJECT_SPEC.md
- TECH_STACK.md
- DATABASE.md
- [relevant specification]

Current Phase:
Phase X

Objective:
[objective]

Tasks:
1. ...
2. ...
3. ...

Constraints:
- Follow locked architecture
- Do not change database technology
- Do not introduce unnecessary dependencies
- Do not remove existing functionality
- Maintain backward compatibility

Acceptance Criteria:
- ...
- ...
- ...

After implementation:
- Run tests
- Report changed files
- Report test results
- Report remaining issues
```

---

# 87. Change Management

หากพบว่าต้องเปลี่ยนสิ่งที่ LOCKED:

```text id="chg001"
Identify Problem
 ↓
Explain Reason
 ↓
Identify Affected Documents
 ↓
Propose Change
 ↓
Update Specifications
 ↓
Implement
```

ห้ามเปลี่ยน Architecture ระหว่าง Coding โดยไม่มีการอัปเดต Specification

---

# 88. Final Project Rule

ระบบนี้ต้องพัฒนาโดยยึดหลัก:

```text id="rule01"
Evidence > Assumption

Real Data > Invented Data

Explainability > Score Only

Skill Fit > Major Name

Development Guidance > Simple Recommendation

Reproducibility > Black Box
```

---

# 89. Final Status

```text id="status01"
PROJECT_SPEC.md
Status: LOCKED

DATABASE.md
Status: LOCKED

DATASET_SPEC.md
Status: LOCKED

AI_MATCHING_SPEC.md
Status: LOCKED

UI_UX_SPEC.md
Status: LOCKED

TECH_STACK.md
Status: LOCKED

IMPLEMENTATION_PLAN.md
Status: LOCKED
```

เอกสารชุดนี้ถือเป็น Foundation ของการพัฒนาระบบ Thesis

---

# 90. Next Development Document

หลังจากเอกสารชุด Specification ครบแล้ว ขั้นตอนถัดไปคือสร้างเอกสาร Implementation-level ที่จำเป็นสำหรับการเริ่ม Coding:

```text id="next01"
API.md
```

จากนั้นจึงเริ่ม:

```text id="next02"
Repository Setup
        ↓
Docker
        ↓
PostgreSQL
        ↓
Migration
        ↓
Seed
        ↓
Backend API
        ↓
AI Service
        ↓
Frontend
```

**Implementation Principle:**

> Build the smallest complete vertical slice first, then expand.

ตัวอย่าง Vertical Slice แรก:

```text id="next03"
Major Selection
 ↓
Create Session
 ↓
Upload Resume
 ↓
Extract Basic Skills
 ↓
Save Skills
 ↓
Return Candidate Skill Profile
```

เมื่อ Vertical Slice นี้ทำงานครบ จึงค่อยต่อ Portfolio → Matching → Skill Gap → UI เต็มรูปแบบ