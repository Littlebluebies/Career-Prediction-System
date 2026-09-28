# API.md

# Career Prediction and Skill Gap Analysis System

## API Specification

**Project:** Career Prediction and Skill Gap Analysis System for Mass Communication Technology Students
**ภาษา:** Thai / English
**Backend:** Node.js + Express.js + TypeScript
**Frontend:** Next.js + React + TypeScript
**AI/NLP Service:** Python
**Database:** PostgreSQL
**Architecture:** REST API
**Authentication:** ไม่มี Login สำหรับผู้ใช้งานทั่วไป

---

# 1. Purpose

เอกสารนี้กำหนดโครงสร้าง API สำหรับระบบ Career Prediction and Skill Gap Analysis System

API ทำหน้าที่เป็นตัวกลางระหว่าง

```text
Next.js Frontend
        ↓
Express.js REST API
        ↓
Service Layer
        ↓
PostgreSQL
        ↕
Python AI/NLP Service
```

API ต้องรับผิดชอบเรื่อง:

* การสร้าง Analysis Session
* การเลือก Major
* การรับ Resume
* การรับ Portfolio URL
* การตรวจสอบ Privacy Consent
* การเริ่มกระบวนการวิเคราะห์
* การเรียก AI/NLP Service
* การบันทึก Candidate Skill Profile
* การคำนวณ Career Matching
* การจัดอันดับ Career
* การสร้าง Explainable Recommendation
* การวิเคราะห์ Skill Gap
* การสร้าง Development Guidance
* การส่งผลลัพธ์ให้ Frontend
* การรับ User Feedback / SUS

---

# 2. API Principles

API ต้องปฏิบัติตามหลักการต่อไปนี้

1. ใช้ REST API
2. ใช้ JSON เป็นรูปแบบข้อมูลหลัก
3. ใช้ HTTP Status Code ให้เหมาะสม
4. ใช้ PostgreSQL เป็นฐานข้อมูลหลัก
5. Frontend ห้ามเชื่อม PostgreSQL โดยตรง
6. Frontend ห้ามเรียก Python Service โดยตรง
7. Express เป็น Main Backend API
8. Python เป็น AI/NLP Processing Service
9. API ต้องรองรับ Session แบบไม่มี Login
10. ต้องตรวจสอบ Input ทุกครั้ง
11. ต้องป้องกัน SQL Injection
12. ต้องไม่ส่ง API Key ให้ Frontend
13. ต้องไม่ส่ง Database Credentials ให้ Frontend
14. ต้องไม่ส่ง System Prompt ให้ Frontend
15. ต้องมี Error Response ที่เป็นมาตรฐาน
16. ต้องสามารถ Trace ผลลัพธ์กลับไปยัง Evidence ได้
17. Career Score ต้องเป็น Match / Compatibility Score
18. ห้ามใช้คำว่า Employment Probability
19. Major เป็น Context ไม่ใช่ Hard Filter
20. ห้ามสร้าง Labour Market Demand จากค่าที่ผู้พัฒนาคิดขึ้นเอง

---

# 3. Base URL

Development:

```text
http://localhost:4000/api
```

Production:

```text
/api
```

Frontend ต้องเรียก API ผ่าน Configuration เช่น

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:4000/api
```

ห้าม Hard-code URL กระจายอยู่ทั่ว Frontend

---

# 4. API Versioning

API ควรเตรียมโครงสร้างรองรับ Versioning

ตัวอย่าง:

```text
/api/v1/session
/api/v1/resume
/api/v1/portfolio
/api/v1/analyze
```

ในระยะ MVP สามารถใช้:

```text
/api
```

ได้ก่อน

แต่ Code Structure ต้องไม่ทำให้การเพิ่ม `/v2` ในอนาคตทำได้ยาก

---

# 5. Session Architecture

ระบบไม่มี Login

ผู้ใช้จะได้รับ `session_id` สำหรับการวิเคราะห์หนึ่งครั้ง

Flow:

```text
User
 ↓
Create Session
 ↓
session_id
 ↓
Upload Resume
 ↓
Submit Portfolio
 ↓
Consent
 ↓
Analyze
 ↓
Results
 ↓
Feedback
 ↓
Session Expire / Delete
```

Session ID ต้องเป็น UUID

ตัวอย่าง:

```text
550e8400-e29b-41d4-a716-446655440000
```

ไม่ควรใช้ข้อมูลส่วนตัวของผู้ใช้เป็น Session ID

---

# 6. Standard Response Format

API Success Response:

```json
{
  "success": true,
  "data": {},
  "message": "Operation completed successfully"
}
```

API Error Response:

```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable error message",
    "details": null
  }
}
```

---

# 7. Standard HTTP Status Codes

ใช้ Status Code ดังนี้

| Status | Meaning                                        |
| ------ | ---------------------------------------------- |
| 200    | Success                                        |
| 201    | Resource Created                               |
| 202    | Processing Accepted                            |
| 400    | Bad Request                                    |
| 401    | Unauthorized — ใช้เฉพาะกรณี API ภายในที่จำเป็น |
| 403    | Forbidden                                      |
| 404    | Resource Not Found                             |
| 409    | Conflict                                       |
| 413    | File Too Large                                 |
| 415    | Unsupported Media Type                         |
| 422    | Validation Error                               |
| 429    | Too Many Requests                              |
| 500    | Internal Server Error                          |
| 502    | External / AI Service Error                    |
| 503    | Service Unavailable                            |

ผู้ใช้ทั่วไปไม่ต้อง Login ดังนั้น API หลักของ User Flow ไม่ควรสร้าง Authentication Flow ขึ้นมาโดยไม่จำเป็น

---

# 8. Endpoint Overview

API หลักของระบบ:

```text
POST   /session
GET    /session/:sessionId

POST   /resume
GET    /resume/:sessionId

POST   /portfolio
GET    /portfolio/:sessionId

POST   /consent

POST   /analyze
GET    /analysis/:sessionId

GET    /career/:resultId
GET    /skill-gap/:resultId

POST   /feedback
```

---

# 9. Create Session

## Endpoint

```http
POST /session
```

## Purpose

สร้าง Session สำหรับการวิเคราะห์ Career

ผู้ใช้ยังไม่จำเป็นต้อง Login

## Request

```json
{
  "major_id": 4
}
```

`major_id` เป็น Context ของผู้ใช้

Major ต้องไม่ถูกนำไปใช้เป็น Hard Filter ของ Career

## Response

```json
{
  "success": true,
  "data": {
    "session_id": "550e8400-e29b-41d4-a716-446655440000",
    "major": {
      "major_id": 4,
      "branch_name": "สาขาวิชาครีเอทีฟมีเดียเทคโนโลยี",
      "major_name": "Web Full Stack"
    },
    "status": "ACTIVE",
    "expires_at": "2026-09-20T12:00:00Z"
  },
  "message": "Session created successfully"
}
```

---

# 10. Get Session

## Endpoint

```http
GET /session/:sessionId
```

## Purpose

ตรวจสอบสถานะ Session

## Response

```json
{
  "success": true,
  "data": {
    "session_id": "550e8400-e29b-41d4-a716-446655440000",
    "status": "ACTIVE",
    "consent_given": true,
    "has_resume": true,
    "portfolio_count": 2
  }
}
```

---

# 11. Upload Resume

## Endpoint

```http
POST /resume
```

## Content-Type

```text
multipart/form-data
```

## Fields

```text
session_id
file
```

## Supported Formats

```text
PDF
DOC
DOCX
```

## Validation

Backend ต้องตรวจสอบ:

* File extension
* MIME type
* File size
* File readability
* File corruption
* Session validity

## Example Response

```json
{
  "success": true,
  "data": {
    "resume_id": 101,
    "session_id": "550e8400-e29b-41d4-a716-446655440000",
    "file_name": "resume.pdf",
    "processing_status": "PENDING"
  },
  "message": "Resume uploaded successfully"
}
```

---

# 12. Resume Processing Status

Resume สามารถมีสถานะ:

```text
PENDING
PROCESSING
COMPLETED
FAILED
```

ตรงกับ `resume.processing_status` ใน `DATABASE.md` §12 Resume ที่ถูกลบจะถูกลบทั้งแถว ไม่มีสถานะ DELETED

Flow:

```text
Upload
 ↓
Validation
 ↓
Store Temporarily
 ↓
Text Extraction
 ↓
Skill Extraction
 ↓
Evidence Extraction
 ↓
Save Result
```

---

# 13. Portfolio Submission

## Endpoint

```http
POST /portfolio
```

## Content-Type

```text
application/json
```

## Request

```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "urls": [
    "https://github.com/example",
    "https://example.com/portfolio"
  ]
}
```

ระบบควรรองรับ URL ประเภท:

```text
Personal Website
GitHub
GitLab
Behance
itch.io
YouTube
Online Portfolio
```

รวมถึง URL ประเภทอื่นที่ระบบสามารถวิเคราะห์ได้ในอนาคต

---

# 14. Portfolio URL Validation

Backend ต้องตรวจสอบ:

* URL Format
* Protocol
* Domain
* Accessibility
* Redirect
* Login Requirement
* Blocked Content
* Unsupported Source

สถานะ:

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

หาก Portfolio เข้าไม่ได้:

```text
ห้ามสรุปว่า User ไม่มี Skill
```

ต้องใช้หลัก:

```text
Evidence Not Available
```

หรือ

```text
Evidence Not Found
```

แทน

---

# 15. Privacy Consent

## Endpoint

```http
POST /consent
```

## Request

```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "consent": true
}
```

หาก User ไม่ยินยอม:

```json
{
  "success": false,
  "error": {
    "code": "CONSENT_REQUIRED",
    "message": "User consent is required before analysis."
  }
}
```

ระบบต้องไม่เริ่ม Analysis หากยังไม่มี Consent

---

# 16. Start Analysis

## Endpoint

```http
POST /analyze
```

## Request

```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

## Validation ก่อน Analysis

Backend ต้องตรวจสอบ:

```text
Session valid?
      ↓
Consent given?
      ↓
Resume available?
      ↓
Resume processed?
      ↓
Portfolio status valid?
      ↓
Start Analysis
```

---

# 17. Analysis Processing

เมื่อเรียก `/analyze`

Express ต้องทำหน้าที่ Orchestrator

```text
Express API
    ↓
Validate Session
    ↓
Validate Input
    ↓
Resume Processing
    ↓
Portfolio Processing
    ↓
Call Python AI Service
    ↓
Receive AI Result
    ↓
Save Candidate Skill Profile
    ↓
Career Matching
    ↓
Skill Gap
    ↓
Explanation
    ↓
Save Results
```

---

# 18. Analysis Status

Session หรือ Analysis สามารถมีสถานะ:

```text
VALIDATING
PARSING_RESUME
ANALYZING_PORTFOLIO
EXTRACTING_SKILLS
NORMALIZING_SKILLS
BUILDING_PROFILE
MATCHING_CAREERS
RANKING_RESULTS
ANALYZING_GAPS
GENERATING_GUIDANCE
COMPLETED
ERROR
```

---

# 19. Start Analysis Response

เนื่องจาก Analysis อาจใช้เวลานาน API ควรสามารถตอบแบบ asynchronous ได้

## Response

```http
202 Accepted
```

```json
{
  "success": true,
  "data": {
    "session_id": "550e8400-e29b-41d4-a716-446655440000",
    "status": "PROCESSING"
  },
  "message": "Analysis started successfully"
}
```

Frontend สามารถเรียก:

```http
GET /analysis/:sessionId
```

เพื่อดูสถานะ

---

# 20. Get Analysis

## Endpoint

```http
GET /analysis/:sessionId
```

## Response During Processing

```json
{
  "success": true,
  "data": {
    "session_id": "550e8400-e29b-41d4-a716-446655440000",
    "status": "EXTRACTING_SKILLS",
    "progress": 40
  }
}
```

หมายเหตุ:

ค่า `progress` เป็นค่าที่ใช้สำหรับ UI เท่านั้น

ไม่ควรทำให้ User เข้าใจว่าเป็น Model Accuracy

---

# 21. Completed Analysis Response

เมื่อวิเคราะห์เสร็จ:

```json
{
  "success": true,
  "data": {
    "session_id": "550e8400-e29b-41d4-a716-446655440000",
    "status": "COMPLETED",

    "candidate_profile": {
      "skills": [
        {
          "skill_id": 1,
          "name": "HTML",
          "category": "TECHNICAL",
          "confidence": 0.95,
          "source": "BOTH"
        },
        {
          "skill_id": 2,
          "name": "React",
          "category": "TECHNICAL",
          "confidence": 0.88,
          "source": "PORTFOLIO"
        }
      ]
    },

    "career_results": [
      {
        "result_id": 501,
        "occupation": {
          "occupation_id": 10,
          "name": "Front-end Developer"
        },
        "score": 0.82,
        "rank": 1,
        "matched_skills": [
          "HTML",
          "CSS",
          "JavaScript",
          "React"
        ],
        "evidence": [
          {
            "skill": "React",
            "source": "Portfolio",
            "project": "Personal Website"
          }
        ],
        "market_signal": {
          "level": "HIGH"
        },
        "explanation": "..."
      }
    ]
  }
}
```

---

# 22. Candidate Skill Profile

Candidate Skill Profile ต้องประกอบด้วยอย่างน้อย:

```text
Skill
Category
Confidence
Source
Evidence
```

ตัวอย่าง:

```json
{
  "skill": "React",
  "category": "TECHNICAL",
  "confidence": 0.88,
  "source": "BOTH"
}
```

Source:

```text
RESUME
PORTFOLIO
BOTH
```

---

# 23. Evidence API

Evidence ต้องสามารถตรวจสอบย้อนกลับได้

โครงสร้าง:

```text
Career Result
      ↓
Matched Skill
      ↓
User Skill
      ↓
Evidence
      ↓
Resume / Portfolio
```

ตัวอย่าง:

```json
{
  "skill": "React",
  "evidence": [
    {
      "source_type": "PORTFOLIO_TECHNOLOGY",
      "source_reference": "portfolio_project_12",
      "description": "Built a responsive web application using React."
    }
  ]
}
```

---

# 24. Career Results

## Endpoint

```http
GET /career/:resultId
```

## Response

```json
{
  "success": true,
  "data": {
    "result_id": 501,
    "occupation": {
      "occupation_id": 10,
      "name": "Front-end Developer",
      "career_family": "Web Development"
    },
    "score": 0.82,
    "rank": 1,
    "matched_skills": [
      "HTML",
      "CSS",
      "JavaScript",
      "React"
    ],
    "market_skills": [
      "TypeScript",
      "Testing",
      "Accessibility"
    ],
    "explanation": "...",
    "evidence": []
  }
}
```

---

# 25. Career Score Rules

Score ต้องหมายถึง:

```text
Career Match Score
```

หรือ

```text
Career Compatibility Score
```

ห้ามแสดงเป็น:

```text
Employment Probability
Job Probability
Chance of Getting Hired
```

ตัวอย่าง:

```text
82% Career Match
```

สามารถใช้ได้หากระบบกำหนด Score Scale เป็น 0–100

แต่ตัวเลขและสูตรจริงต้องถูกกำหนดจาก methodology และ evaluation

ห้ามกำหนด Weight แบบสุ่มเพื่อให้ผลลัพธ์ดูดี

---

# 26. Career Ranking

ระบบต้องรองรับ Top-K

ค่าเริ่มต้น:

```text
Top 3–5 Careers
```

ตัวอย่าง:

```json
{
  "career_results": [
    {
      "rank": 1,
      "occupation": "Front-end Developer",
      "score": 0.82
    },
    {
      "rank": 2,
      "occupation": "UI/UX Designer",
      "score": 0.77
    },
    {
      "rank": 3,
      "occupation": "Web Developer",
      "score": 0.74
    }
  ]
}
```

หากผลลัพธ์มีคะแนนใกล้เคียงกัน ระบบไม่ควรอ้างว่าความแตกต่างนั้นมีนัยสำคัญ หากยังไม่ได้ผ่านการประเมินทางสถิติหรือ methodology ที่เหมาะสม

---

# 27. Cross-Major Matching

Major ของ User เป็นเพียง Context

ตัวอย่าง:

```text
Major:
Creative Media Technology — Web Full Stack
```

แต่ผลลัพธ์สามารถเป็น:

```text
Front-end Developer
UI/UX Designer
Digital Content Creator
Graphic Designer
```

หาก Skill และ Evidence สนับสนุน

Backend ห้ามเขียน Logic:

```text
if major == "Web Full Stack":
    only return Web careers
```

ห้ามใช้ Major เป็น Hard Filter

---

# 28. Skill Gap API

## Endpoint

```http
GET /skill-gap/:resultId
```

## Response

```json
{
  "success": true,
  "data": {
    "result_id": 501,
    "occupation": "Front-end Developer",
    "skill_gap": [
      {
        "skill": "TypeScript",
        "status": "EVIDENCE_NOT_FOUND",
        "priority": "HIGH",
        "reason": "Frequently required in the collected job postings.",
        "guidance": {
          "learn": "Study TypeScript fundamentals.",
          "practice": "Convert an existing React project to TypeScript.",
          "build": "Create a small React + TypeScript application."
        }
      },
      {
        "skill": "Testing",
        "status": "PARTIAL",
        "priority": "MEDIUM",
        "reason": "Testing-related requirements appear in relevant job postings."
      }
    ]
  }
}
```

---

# 29. Skill Gap Status

ใช้สถานะ:

```text
MATCHED
PARTIAL
EVIDENCE_NOT_FOUND
```

ความหมาย:

### MATCHED

พบหลักฐานที่สอดคล้องกับ Skill ที่ต้องการ

### PARTIAL

พบหลักฐานบางส่วน แต่ยังไม่เพียงพอสำหรับ Skill Requirement ทั้งหมด

### EVIDENCE_NOT_FOUND

ยังไม่พบหลักฐานจากข้อมูลที่ระบบวิเคราะห์

ห้ามแสดงว่า:

```text
User ไม่มี Skill นี้
```

เพียงเพราะระบบไม่พบหลักฐาน

---

# 30. Skill Gap Priority

Priority:

```text
HIGH
MEDIUM
LOW
```

Priority ต้องพิจารณาจาก:

```text
Skill Importance
+
Labour Market Demand
+
Candidate Skill Status
```

ไม่ควรกำหนด Priority จากความคิดเห็นของ Developer เพียงอย่างเดียว

---

# 31. Development Guidance

Guidance ใช้โครงสร้าง:

```text
Learn
 ↓
Practice
 ↓
Build
 ↓
Document
```

ตัวอย่าง:

```json
{
  "skill": "TypeScript",
  "guidance": {
    "learn": "Learn TypeScript fundamentals.",
    "practice": "Apply types and interfaces in React components.",
    "build": "Create a React + TypeScript project.",
    "document": "Add the project to the portfolio with a clear description."
  }
}
```

Guidance เป็นคำแนะนำด้านการพัฒนาทักษะ

ไม่ใช่การรับประกันการได้งาน

---

# 32. Feedback API

## Endpoint

```http
POST /feedback
```

## Request

```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "sus_score": 82,
  "satisfaction": 85,
  "comment": "ระบบใช้งานง่ายและเข้าใจผลลัพธ์ได้"
}
```

`satisfaction` เป็นคะแนน 0-100 ตาม `DATABASE.md` §28 (Frontend แปลงจากสเกล 1-5 ใน `UI_UX_SPEC.md` §43 โดยคูณ 20)

---

# 33. SUS

ระบบควรรองรับ System Usability Scale (SUS)

ต้องใช้โครงสร้างมาตรฐานของ SUS

ห้ามแก้ wording ของคำถามมาตรฐานโดยไม่มีเหตุผลทางระเบียบวิธีวิจัย

Backend รับ:

```text
SUS responses
```

และสามารถคำนวณ:

```text
SUS Score
```

เป็นคะแนน 0–100

---

# 34. Internal Python AI Service

Python Service ไม่ใช่ Public API สำหรับ Frontend

Architecture:

```text
Next.js
   ↓
Express
   ↓
Python AI Service
```

Frontend ห้ามเรียก:

```text
Python directly
```

---

# 35. Python Service Endpoint

Internal Endpoint:

```http
POST /internal/analyze
```

Endpoint นี้สามารถอยู่ใน Docker Network ภายใน

ไม่ควรเปิด Public โดยไม่จำเป็น

Python Service มี `GET /health` สำหรับ Health Check

---

# 36. Python Analysis Request

Express ส่งข้อมูลที่จำเป็นไปยัง Python

ตัวอย่าง:

```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "resume_text": "...",
  "portfolio_projects": [
    {
      "project_id": 12,
      "title": "Personal Website",
      "description": "Built a responsive website using React.",
      "technologies": [
        "React",
        "HTML",
        "CSS"
      ]
    }
  ]
}
```

ไม่ควรส่งข้อมูลส่วนบุคคลที่ไม่จำเป็นต่อการวิเคราะห์

---

# 37. Python Analysis Response

ตัวอย่าง:

```json
{
  "skills": [
    {
      "name": "React",
      "confidence": 0.88,
      "evidence": [
        {
          "source_type": "PORTFOLIO_TECHNOLOGY",
          "project_id": 12,
          "evidence_text": "Built a responsive website using React."
        }
      ]
    }
  ]
}
```

`source_type` ต้องเป็นหนึ่งใน 8 ค่าของ `skill_evidence.source_type` (`DATABASE.md` §18, `AI_MATCHING_SPEC.md` §13) Evidence จาก Resume ไม่มี `project_id` ให้ใช้ `source_reference` (เช่น ชื่อ Section ใน Resume)

Express จะเป็นผู้รับผลลัพธ์และนำไปดำเนินการต่อ

---

# 38. AI Service Responsibilities

Python รับผิดชอบ:

```text
Text Cleaning
Resume Parsing
Portfolio Text Processing
Skill Extraction
Skill Normalization
Semantic Similarity
Embedding
NLP Processing
AI Evaluation
```

Python ไม่ควรรับผิดชอบ:

```text
Frontend
Main REST API
Session Management
User Interface
Business Authorization
Main Database Transaction Logic
```

---

# 39. Express Responsibilities

Express รับผิดชอบ:

```text
HTTP Request
Input Validation
Session Management
Business Logic
Database Transaction
Calling Python Service
Career Matching Orchestration
Result Persistence
Error Handling
API Response
```

---

# 40. Next.js Responsibilities

Next.js รับผิดชอบ:

```text
UI
Form
Upload UI
Portfolio URL UI
Progress UI
Result UI
Skill Gap UI
Feedback UI
```

Frontend ไม่ควร:

```text
Connect PostgreSQL
Calculate final Career Score
Call Python directly
Store API Secret
Store Database Password
```

---

# 41. API → Database Mapping

| API                  | Main Table                 |
| -------------------- | -------------------------- |
| POST /session        | user_session               |
| POST /resume         | resume                     |
| POST /portfolio      | portfolio                  |
| Portfolio processing | portfolio_project          |
| Skill extraction     | skill / user_skill         |
| Evidence             | skill_evidence             |
| Career framework     | occupation / career_family |
| Career matching      | career_result              |
| Skill gap            | skill_gap                  |
| Feedback             | user_feedback              |

---

# 42. Database Transaction

Operation ที่เกี่ยวข้องหลาย Table ต้องพิจารณา Transaction

ตัวอย่าง:

```text
Create Analysis Result
      ↓
career_result
      ↓
skill_gap
      ↓
user_skill
      ↓
skill_evidence
```

หากขั้นตอนสำคัญล้มเหลว ต้องสามารถ Rollback ได้ตามความเหมาะสม

---

# 43. Validation

Backend ต้อง Validate ทุก Input

ตัวอย่าง Session:

```text
session_id must be UUID
```

Major:

```text
major_id must exist
```

Portfolio:

```text
must be valid URL
```

Feedback:

```text
sus_score must be valid range
satisfaction must be valid range
```

ห้ามเชื่อข้อมูลจาก Frontend โดยตรง

---

# 44. Error Codes

กำหนด Error Code กลาง เช่น:

```text
INVALID_REQUEST
INVALID_SESSION
SESSION_EXPIRED
CONSENT_REQUIRED
RESUME_REQUIRED
RESUME_INVALID
RESUME_TOO_LARGE
RESUME_PARSE_FAILED
PORTFOLIO_INVALID
PORTFOLIO_INACCESSIBLE
PORTFOLIO_BLOCKED
PORTFOLIO_LOGIN_REQUIRED
PORTFOLIO_UNSUPPORTED
ANALYSIS_ALREADY_RUNNING
ANALYSIS_FAILED
AI_SERVICE_UNAVAILABLE
AI_SERVICE_TIMEOUT
DATABASE_ERROR
CAREER_RESULT_NOT_FOUND
SKILL_GAP_NOT_FOUND
INVALID_FEEDBACK
RATE_LIMIT_EXCEEDED
INTERNAL_ERROR
```

Error Code ต้องคงที่เพื่อให้ Frontend สามารถจัดการได้

---

# 45. Example Error

```json
{
  "success": false,
  "error": {
    "code": "PORTFOLIO_INACCESSIBLE",
    "message": "The portfolio could not be accessed.",
    "details": {
      "url": "https://example.com"
    }
  }
}
```

Frontend สามารถแสดง:

```text
ไม่สามารถเข้าถึง Portfolio นี้ได้
ระบบจะไม่ถือว่าคุณไม่มี Skill จากกรณีนี้
```

---

# 46. Rate Limiting

API ควรมี Rate Limiting โดยเฉพาะ:

```text
POST /session
POST /resume
POST /portfolio
POST /analyze
POST /feedback
```

เพื่อป้องกัน:

```text
Abuse
Spam
Resource Exhaustion
Repeated AI Processing
```

---

# 47. File Upload Security

Resume Upload ต้อง:

* จำกัด File Size
* ตรวจสอบ MIME Type
* ตรวจสอบ Extension
* เปลี่ยนชื่อไฟล์ที่จัดเก็บ
* ห้ามใช้ Original Filename เป็น Storage Path โดยตรง
* Scan/Validate ไฟล์ตามความเหมาะสม
* ไม่ execute uploaded file
* เก็บไฟล์ใน Temporary Storage
* ลบตาม Retention Policy

---

# 48. Privacy

API ต้องปฏิบัติตามหลัก Data Minimization

เก็บเฉพาะข้อมูลที่จำเป็นต่อ:

```text
Resume Analysis
Portfolio Analysis
Career Matching
Skill Gap Analysis
Evaluation
```

ไม่ควรเก็บ:

```text
Password
API Key
System Prompt
ข้อมูลส่วนบุคคลที่ไม่จำเป็น
```

---

# 49. Session Expiration

Session ต้องมี:

```text
created_at
expires_at
status
```

เมื่อหมดอายุ:

```text
ACTIVE
 ↓
EXPIRED
```

Temporary User Data สามารถถูกลบตาม Retention Policy

---

# 50. Delete / Cleanup

เมื่อ Session หมดอายุหรือผู้ใช้ร้องขอให้ลบ:

```text
user_session
   ↓
resume
portfolio
portfolio_project
user_skill
skill_evidence
career_result
skill_gap
```

ข้อมูล Temporary ต้องถูกจัดการตาม Retention Policy

Knowledge Data เช่น:

```text
skill
occupation
career_family
job_posting
```

ไม่ควรถูกลบเพียงเพราะ User Session หมดอายุ

---

# 51. Labour Market Traceability

Career Result ต้องสามารถ Trace กลับไปยังข้อมูลตลาดแรงงานได้

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

API ควรสามารถส่งข้อมูล Market Signal ที่อธิบายได้

ตัวอย่าง:

```json
{
  "market_signal": {
    "level": "HIGH",
    "source": "labour_market_dataset",
    "dataset_version": "2026-01"
  }
}
```

ค่า `HIGH` ต้องมาจาก methodology ที่กำหนดไว้จริง

ไม่ใช่ค่าที่ Developer กำหนดตามความรู้สึก

---

# 52. Dataset Version

ทุก Career Analysis ควรบันทึก:

```text
dataset_version_id
algorithm_version
```

เพื่อให้สามารถตอบได้ว่า:

```text
ผลลัพธ์นี้ใช้ Dataset รุ่นใด?
Algorithm รุ่นใด?
```

---

# 53. Algorithm Version

ตัวอย่าง:

```text
algorithm_version:
career-matching-v1.0
```

เมื่อ Matching Algorithm เปลี่ยน:

```text
v1.0
↓
v1.1
↓
v2.0
```

ต้องสามารถแยกผลลัพธ์แต่ละ Version ได้

---

# 54. Explainability API

Career Result ต้องตอบได้ว่า:

```text
Why was this career recommended?
```

ข้อมูลที่ควรส่ง:

```text
Career
Match Score
Matched Skills
Evidence
Market Skills
Skill Gap
Reason
```

ตัวอย่าง:

```json
{
  "explanation": {
    "summary": "This career aligns with several skills evidenced in the user's resume and portfolio.",
    "matched_skills": [
      "HTML",
      "CSS",
      "JavaScript",
      "React"
    ],
    "evidence_count": 4,
    "market_relevance": "Skills related to React and JavaScript appear frequently in the analyzed job postings."
  }
}
```

ข้อความ Explanation ต้องไม่อ้างสิ่งที่ไม่มี Evidence รองรับ

---

# 55. API Security

ต้องปฏิบัติตามหลัก:

```text
Input Validation
Parameterized Queries
Rate Limiting
CORS Configuration
Secure Headers
File Validation
Request Size Limits
Timeouts
Error Sanitization
Environment Variables
```

ห้ามส่ง Stack Trace หรือ Internal Database Error ให้ User ใน Production

---

# 56. API Logging

Backend ควร Log:

```text
Request ID
Timestamp
Endpoint
HTTP Method
Status Code
Processing Time
Session ID
Error Code
```

ไม่ควร Log:

```text
Resume Content ทั้งหมด
Private Portfolio Content ทั้งหมด
API Keys
Passwords
Database Credentials
Sensitive Personal Data ที่ไม่จำเป็น
```

---

# 57. Request ID

แต่ละ Request ควรมี:

```text
X-Request-ID
```

ตัวอย่าง:

```text
X-Request-ID: req_01JABC123
```

ใช้สำหรับ Debug และ Trace ระบบ

---

# 58. Timeout

การเรียก Python AI Service ต้องมี Timeout

ตัวอย่าง Concept:

```text
Express
  ↓
Python AI
  ↓
Timeout
  ↓
Retry / Fail Gracefully
```

ห้ามปล่อย Request ค้างไม่สิ้นสุด

ค่า Timeout จริงต้องกำหนดใน Configuration

---

# 59. Retry

Retry เฉพาะ Error ที่เหมาะสม เช่น:

```text
Temporary Network Error
Temporary AI Service Unavailable
```

ไม่ควร Retry:

```text
Invalid Input
Invalid File
Invalid URL
Consent Missing
```

เพื่อไม่ให้เกิด Processing ซ้ำโดยไม่จำเป็น

---

# 60. Idempotency

Operation ที่อาจถูกเรียกซ้ำ เช่น:

```text
POST /analyze
```

ต้องป้องกันการสร้างผลลัพธ์ซ้ำ

ตัวอย่าง:

```text
Session A
 ↓
Analysis Running
 ↓
User clicks Analyze again
```

ระบบต้องตอบ:

```text
ANALYSIS_ALREADY_RUNNING
```

แทนที่จะเริ่ม Process ใหม่หลายครั้ง

---

# 61. API Flow — Complete

```text
1. User selects Major
        ↓
2. POST /session
        ↓
3. session_id
        ↓
4. POST /resume
        ↓
5. POST /portfolio
        ↓
6. POST /consent
        ↓
7. POST /analyze
        ↓
8. Express validates
        ↓
9. Python analyzes
        ↓
10. Skill Extraction
        ↓
11. Skill Normalization
        ↓
12. Evidence Analysis
        ↓
13. Candidate Skill Profile
        ↓
14. Career Matching
        ↓
15. Career Ranking
        ↓
16. Explainability
        ↓
17. Skill Gap
        ↓
18. Development Guidance
        ↓
19. GET /analysis/:sessionId
        ↓
20. User views result
        ↓
21. POST /feedback
        ↓
22. Session cleanup
```

---

# 62. Recommended Frontend State

Frontend ควรมี State อย่างน้อย:

```text
session
major
resume
portfolio
consent
analysisStatus
candidateSkills
careerResults
selectedCareer
skillGap
guidance
feedback
```

Frontend ไม่ควรเก็บข้อมูลเกินความจำเป็น

---

# 63. API Client Structure

Next.js สามารถมีโครงสร้าง:

```text
apps/web/
└── lib/
    └── api/
        ├── client.ts
        ├── session.ts
        ├── resume.ts
        ├── portfolio.ts
        ├── analysis.ts
        ├── career.ts
        ├── skill-gap.ts
        └── feedback.ts
```

ไม่ควรเขียน `fetch()` กระจายอยู่ทุก Component

---

# 64. Express Structure

Backend:

```text
apps/api/src/
├── routes/
│   ├── session.routes.ts
│   ├── resume.routes.ts
│   ├── portfolio.routes.ts
│   ├── analysis.routes.ts
│   ├── career.routes.ts
│   ├── skill-gap.routes.ts
│   └── feedback.routes.ts
│
├── controllers/
├── services/
├── repositories/
├── validators/
├── middlewares/
├── clients/
│   └── python.client.ts
├── config/
└── app.ts
```

---

# 65. Python Structure

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
└── requirements.txt
```

---

# 66. API Testing

ทุก Endpoint สำคัญต้องมี Test

อย่างน้อย:

```text
Create Session
Upload Resume
Submit Portfolio
Consent
Start Analysis
Get Analysis
Get Career Result
Get Skill Gap
Submit Feedback
```

ต้องทดสอบทั้ง:

```text
Success Case
Validation Error
Not Found
Expired Session
Duplicate Request
AI Service Error
Database Error
```

---

# 67. Example End-to-End API Scenario

## Step 1

```http
POST /session
```

```json
{
  "major_id": 4
}
```

ได้รับ:

```text
session_id = abc
```

---

## Step 2

```http
POST /resume
```

```text
session_id = abc
file = resume.pdf
```

---

## Step 3

```http
POST /portfolio
```

```json
{
  "session_id": "abc",
  "urls": [
    "https://github.com/example"
  ]
}
```

---

## Step 4

```http
POST /consent
```

```json
{
  "session_id": "abc",
  "consent": true
}
```

---

## Step 5

```http
POST /analyze
```

```json
{
  "session_id": "abc"
}
```

---

## Step 6

Frontend Polling:

```http
GET /analysis/abc
```

จนกว่า:

```text
status = COMPLETED
```

---

## Step 7

Frontend แสดง:

```text
Candidate Skills
        ↓
Top 3–5 Careers
        ↓
Career Explanation
        ↓
Skill Gap
        ↓
Development Guidance
```

---

## Step 8

User ส่ง Feedback:

```http
POST /feedback
```

---

# 68. MVP API

Semester 1 MVP สามารถเริ่มจาก:

```text
POST /session
POST /resume
POST /portfolio
POST /consent
POST /analyze
GET  /analysis/:sessionId
GET  /career/:resultId
GET  /skill-gap/:resultId
POST /feedback
```

โดยเน้น:

```text
Creative Media Technology
        ↓
Web Full Stack
```

---

# 69. Semester 2 API Expansion

Semester 2 ต้องรองรับทุกสาขา:

```text
Film & Television
Advertising & Public Relations
Digital Printing & Packaging
Creative Media Technology
```

ภายใน Creative Media Technology:

```text
Web Full Stack
Game Development
```

API ไม่ควรต้องสร้างใหม่สำหรับแต่ละ Major

ใช้:

```text
major_id
```

เป็น Context

และใช้ Occupation Framework เป็นฐานกลาง

---

# 70. API Acceptance Criteria

API ถือว่าผ่านเมื่อ:

* [ ] สามารถสร้าง Session ได้
* [ ] Session ใช้ UUID
* [ ] สามารถเลือก Major ได้
* [ ] Major ไม่เป็น Hard Filter
* [ ] Upload Resume ได้
* [ ] ตรวจสอบ Resume ได้
* [ ] Submit Portfolio URL ได้
* [ ] รองรับ Portfolio ที่เข้าถึงไม่ได้
* [ ] มี Privacy Consent
* [ ] ไม่เริ่ม Analysis หากไม่มี Consent
* [ ] เริ่ม Analysis ได้
* [ ] Express สามารถเรียก Python Service ได้
* [ ] Skill Extraction Result ถูกบันทึกได้
* [ ] Evidence สามารถ Trace ได้
* [ ] Career Matching ทำงานได้
* [ ] ได้ Top 3–5 Career
* [ ] มี Match Score
* [ ] มี Explanation
* [ ] มี Labour Market Signal
* [ ] มี Skill Gap
* [ ] มี Development Guidance
* [ ] รองรับ SUS / User Feedback
* [ ] มี Error Handling
* [ ] มี Rate Limiting
* [ ] มี Request Logging
* [ ] มี Timeout
* [ ] ป้องกัน Duplicate Analysis
* [ ] รองรับ Session Expiration
* [ ] มี Data Cleanup
* [ ] มี Dataset Version
* [ ] มี Algorithm Version

---

# 71. Prohibited API Patterns

ห้าม:

```text
Next.js → PostgreSQL
```

ห้าม:

```text
Next.js → Python AI
```

ห้าม:

```text
Python → Frontend
```

ห้าม:

```text
Frontend → Database Credentials
```

ห้าม:

```text
Frontend → AI API Key
```

ห้าม:

```text
Major → Hard Filter Occupation
```

ห้าม:

```text
No Evidence → User Does Not Have Skill
```

ห้าม:

```text
Career Score → Employment Probability
```

ห้าม:

```text
Developer invented market demand
```

ห้าม:

```text
Hard-coded Career Ranking
```

ห้าม:

```text
Duplicate API implementation in Next.js and Express
```

---

# 72. API Development Priority

พัฒนา API ตามลำดับ:

```text
1. POST /session
        ↓
2. POST /resume
        ↓
3. POST /portfolio
        ↓
4. POST /consent
        ↓
5. POST /analyze
        ↓
6. GET /analysis/:sessionId
        ↓
7. Skill Profile
        ↓
8. Career Matching
        ↓
9. GET /career/:resultId
        ↓
10. GET /skill-gap/:resultId
        ↓
11. Development Guidance
        ↓
12. POST /feedback
```

---

# 73. Claude Implementation Rules

เมื่อ Claude เริ่ม Implement API ต้อง:

1. อ่าน `PROJECT_SPEC.md`
2. อ่าน `DATABASE.md`
3. อ่าน `DATASET_SPEC.md`
4. อ่าน `AI_MATCHING_SPEC.md`
5. อ่าน `UI_UX_SPEC.md`
6. อ่าน `TECH_STACK.md`
7. อ่าน `IMPLEMENTATION_PLAN.md`
8. อ่าน `API.md`

จากนั้นจึงเริ่มเขียน Code

ห้ามสร้าง API โดยอาศัยความเข้าใจจาก `API.md` เพียงไฟล์เดียว หากรายละเอียดด้าน Database, AI หรือ UI ถูกกำหนดไว้ในเอกสารอื่น

---

# 74. Claude Must Follow Architecture

```text
Next.js
   ↓
Express REST API
   ↓
Service Layer
   ↓
Repository Layer
   ↓
PostgreSQL
```

และ:

```text
Express
   ↓
Python AI Service
```

ต้องไม่เปลี่ยน Architecture โดยไม่มีเหตุผลและไม่ควรสร้าง Backend ซ้ำซ้อน

---

# 75. Change Management

หาก API เปลี่ยน ต้องตรวจสอบเอกสาร:

```text
API.md
DATABASE.md
AI_MATCHING_SPEC.md
UI_UX_SPEC.md
IMPLEMENTATION_PLAN.md
TECH_STACK.md
PROJECT_SPEC.md
```

ตัวอย่าง:

หากเพิ่ม Endpoint ใหม่:

```text
API.md
```

ต้องถูกแก้

หาก Endpoint ต้องใช้ Table ใหม่:

```text
DATABASE.md
```

ต้องถูกแก้ด้วย

หากเปลี่ยน AI Processing:

```text
AI_MATCHING_SPEC.md
```

ต้องถูกตรวจสอบ

---

# 76. Final API Architecture

```text
                         USER
                           │
                           ▼
               ┌─────────────────────┐
               │      Next.js        │
               │ React + TypeScript  │
               │     Tailwind CSS    │
               └──────────┬──────────┘
                          │
                       REST API
                          │
                          ▼
               ┌─────────────────────┐
               │   Express Backend   │
               │ Node.js + TypeScript│
               └───────┬───────┬─────┘
                       │       │
                       │       │ HTTP/JSON
                       │       ▼
                       │ ┌─────────────────┐
                       │ │ Python AI/NLP   │
                       │ │     Service     │
                       │ └─────────────────┘
                       │
                       ▼
               ┌─────────────────────┐
               │     PostgreSQL      │
               │    Main Database    │
               └─────────────────────┘
```

---

# 77. Final System Flow

```text
Major Selection
       ↓
Create Session
       ↓
Resume Upload
       ↓
Portfolio URL
       ↓
Privacy Consent
       ↓
Input Validation
       ↓
Resume Analysis
       ↓
Portfolio Analysis
       ↓
Skill Extraction
       ↓
Skill Normalization
       ↓
Evidence Analysis
       ↓
Candidate Skill Profile
       ↓
Occupation Knowledge
       +
Labour Market Data
       ↓
Career Matching
       ↓
Career Ranking
       ↓
Explainable Recommendation
       ↓
Skill Gap Analysis
       ↓
Development Guidance
       ↓
User Satisfaction / SUS
       ↓
Session Cleanup
       ↓
END
```

---

# 78. Definition of Done

API Layer ถือว่าสมบูรณ์เมื่อ:

```text
Frontend สามารถ
      ↓
สร้าง Session
      ↓
ส่ง Resume
      ↓
ส่ง Portfolio
      ↓
ยืนยัน Consent
      ↓
เริ่ม Analysis
      ↓
ติดตาม Processing
      ↓
รับ Candidate Skill Profile
      ↓
รับ Career Results
      ↓
ดู Evidence
      ↓
ดู Skill Gap
      ↓
ดู Development Guidance
      ↓
ส่ง Feedback
```

ได้ครบโดยไม่ต้องเข้าถึง PostgreSQL หรือ Python Service โดยตรง

---

# 79. Document Status

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
Database: PostgreSQL
Backend: Node.js + Express.js + TypeScript
Frontend: Next.js + React + TypeScript + Tailwind CSS
AI/NLP: Python
Container: Docker + Docker Compose
Version Control: Git + GitHub

API Architecture: LOCKED
REST API: LOCKED
Express as Main Backend: LOCKED
Python as AI/NLP Service: LOCKED
No Direct Frontend → Database: LOCKED
No Direct Frontend → Python: LOCKED

Semester 1:
Creative Media Technology → Web Full Stack Pilot

Semester 2:
Whole Faculty Expansion

Detailed Database Specification:
DATABASE.md

Detailed Dataset Specification:
DATASET_SPEC.md

Detailed AI/NLP Specification:
AI_MATCHING_SPEC.md

Detailed UI/UX Specification:
UI_UX_SPEC.md

Detailed Technology Specification:
TECH_STACK.md

Detailed Implementation Plan:
IMPLEMENTATION_PLAN.md

Detailed API Specification:
API.md
```

---

# END OF API.md