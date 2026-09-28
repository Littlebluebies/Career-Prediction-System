# DATABASE.md

# Career Prediction and Skill Gap Analysis System

## PostgreSQL Database Specification

---

# 1. Document Purpose

เอกสารนี้กำหนด Database Architecture และ PostgreSQL Schema สำหรับระบบ:

**Career Prediction and Skill Gap Analysis System for Mass Communication Technology Students Based on Skill Evidence and Labour Market Demand**

Database ต้องรองรับกระบวนการ:

```text id="u5m5n9"
User Session
    ↓
Resume + Portfolio
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
    ↓
Labour Market Data
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

Database เป็นส่วนสำคัญของระบบ แต่ไม่ควรเป็นตัวประมวลผล AI โดยตรง

---

# 2. Locked Technology

Database ของระบบนี้ใช้:

```text id="6f2a1q"
PostgreSQL
```

และ Backend เชื่อมต่อผ่าน:

```text id="1b8g2h"
Node.js
+
Express.js
+
TypeScript
```

Python AI/NLP Service สามารถเข้าถึงข้อมูลที่จำเป็นผ่าน Backend API หรือ Database Access Layer ตาม Architecture ที่กำหนด

---

# 3. Database Principles

Database ต้องปฏิบัติตามหลักการ:

1. Relational Database
2. Normalized Data
3. Referential Integrity
4. Foreign Key Constraints
5. Unique Constraints
6. Transaction Safety
7. Traceability
8. Dataset Versioning
9. Temporary User Data
10. Privacy by Design
11. No Permanent User Account
12. No Password Storage
13. No Hard-coded Career Result
14. No Arbitrary Labour Market Demand
15. Support for Data Evaluation

---

# 4. PostgreSQL Configuration

แนะนำ:

```text
Database:
PostgreSQL

Encoding:
UTF-8

Timezone:
UTC
```

Application Layer สามารถแปลงเวลาเป็นเวลาไทย:

```text
Asia/Bangkok
```

เมื่อแสดงผลแก่ผู้ใช้

การเก็บเวลาใน Database ควรใช้:

```sql
TIMESTAMPTZ
```

แทนการเก็บเวลาแบบไม่มี Timezone

---

# 5. PostgreSQL Data Types

เลือกใช้ PostgreSQL Types ให้เหมาะกับข้อมูล

### Primary Key

ใช้:

```sql
BIGINT GENERATED ALWAYS AS IDENTITY
```

แทนการพึ่งพา `AUTO_INCREMENT`

ตัวอย่าง:

```sql
id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY
```

### UUID

สำหรับ Temporary Session:

```sql
session_id UUID PRIMARY KEY
```

### Boolean

ใช้:

```sql
BOOLEAN
```

### Timestamp

ใช้:

```sql
TIMESTAMPTZ
```

### Text

ข้อมูลข้อความที่มีความยาวไม่แน่นอนใช้:

```sql
TEXT
```

ไม่จำเป็นต้องกำหนด VARCHAR ทุกกรณี

---

# 6. High-Level Database Architecture

แบ่งข้อมูลออกเป็น 4 กลุ่ม:

```text id="pjb6bi"
┌───────────────────────────────┐
│ 1. Temporary User Data        │
│                               │
│ Session                       │
│ Resume                        │
│ Portfolio                     │
│ Evidence                      │
└───────────────────────────────┘

┌───────────────────────────────┐
│ 2. Knowledge Data             │
│                               │
│ Major                         │
│ Skill                         │
│ Skill Alias                   │
│ Career Family                 │
│ Occupation                    │
│ Occupation Alias              │
│ Occupation Skill              │
└───────────────────────────────┘

┌───────────────────────────────┐
│ 3. Labour Market Data         │
│                               │
│ Job Posting                   │
│ Job Posting Skill             │
│ Dataset Version               │
└───────────────────────────────┘

┌───────────────────────────────┐
│ 4. Analysis Result            │
│                               │
│ Career Result                 │
│ Skill Gap                     │
│ User Feedback                 │
└───────────────────────────────┘
```

---

# 7. Entity Overview

Core Tables:

```text id="r8oz2e"
01. major
02. user_session
03. resume
04. portfolio
05. portfolio_project

06. skill
07. skill_alias
08. user_skill
09. skill_evidence

10. career_family
11. occupation
12. occupation_alias
13. occupation_skill

14. job_posting
15. job_posting_skill
16. dataset_version

17. career_result
18. skill_gap
19. user_feedback
```

รวม:

```text id="d8j5n5"
19 Core Tables
```

---

# 8. Entity Relationship Overview

```text id="e9q5w4"
MAJOR
  │
  ▼
USER_SESSION
  │
  ├──────────────► RESUME
  │
  ├──────────────► PORTFOLIO
  │                     │
  │                     ▼
  │              PORTFOLIO_PROJECT
  │                     │
  │                     ▼
  │                  EVIDENCE
  │
  ▼
USER_SKILL
  │
  ▼
SKILL
  │
  ├──────────────► SKILL_ALIAS
  │
  └──────────────► SKILL_EVIDENCE


CAREER_FAMILY
  │
  ▼
OCCUPATION
  │
  ├──────────────► OCCUPATION_ALIAS
  │
  └──────────────► OCCUPATION_SKILL
                         │
                         ▼
                       SKILL


JOB_POSTING
  │
  └──────────────► JOB_POSTING_SKILL
                         │
                         ▼
                       SKILL


USER_SESSION
  │
  ▼
CAREER_RESULT
  │
  ├──────────────► SKILL_GAP
  │
  └──────────────► OCCUPATION


USER_SESSION
  │
  ▼
USER_FEEDBACK
```

---

# 9. Schema Namespace

แนะนำให้ใช้ PostgreSQL Schema:

```sql
CREATE SCHEMA IF NOT EXISTS career_system;
```

และกำหนด:

```sql
SET search_path TO career_system, public;
```

เหตุผล:

* แยก Database Objects ของระบบ
* ลดชื่อ Table Collision
* จัดการระบบง่ายขึ้น
* เหมาะกับการ Deploy ผ่าน Docker

หาก Project เล็กมาก สามารถใช้ `public` Schema ได้ แต่ต้องใช้แนวทางเดียวกันทั้งระบบ

---

# 10. MAJOR

เก็บสาขาวิชาของ Faculty

```sql
CREATE TABLE major (
    major_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    branch_name TEXT NOT NULL,
    major_name TEXT NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT uq_major
        UNIQUE (branch_name, major_name)
);
```

ตัวอย่างข้อมูล:

```text
สาขาวิชาเทคโนโลยีการผลิตภาพยนตร์และวิทยุโทรทัศน์
สาขาวิชาเทคโนโลยีการโฆษณาและประชาสัมพันธ์
สาขาวิชาเทคโนโลยีการพิมพ์ดิจิทัลและบรรจุภัณฑ์
สาขาวิชาครีเอทีฟมีเดียเทคโนโลยี
```

สำหรับ Creative Media Technology สามารถเก็บ Track/Focus เพิ่มภายหลังได้หากจำเป็น

เช่น:

```text
Web Full Stack
Game Development
```

Major เป็น **Context เท่านั้น**

ห้ามสร้าง Foreign Key หรือ Mapping ที่บังคับว่า:

```text
Major → Occupation
```

---

# 11. USER_SESSION

ระบบไม่มี Login

ดังนั้นใช้ Temporary Session

```sql
CREATE TABLE user_session (
    session_id UUID PRIMARY KEY,
    major_id BIGINT REFERENCES major(major_id)
        ON DELETE SET NULL,

    consent_given BOOLEAN NOT NULL DEFAULT FALSE,
    consent_given_at TIMESTAMPTZ,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    expires_at TIMESTAMPTZ NOT NULL,

    status TEXT NOT NULL DEFAULT 'ACTIVE',

    CONSTRAINT chk_session_status
        CHECK (
            status IN (
                'ACTIVE',
                'PROCESSING',
                'COMPLETED',
                'EXPIRED',
                'DELETED',
                'ERROR'
            )
        )
);
```

Index:

```sql
CREATE INDEX idx_user_session_major
ON user_session(major_id);

CREATE INDEX idx_user_session_expires
ON user_session(expires_at);

CREATE INDEX idx_user_session_status
ON user_session(status);
```

---

# 12. RESUME

เก็บข้อมูล Resume ที่ผู้ใช้ Upload

```sql
CREATE TABLE resume (
    resume_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    session_id UUID NOT NULL
        REFERENCES user_session(session_id)
        ON DELETE CASCADE,

    file_name TEXT NOT NULL,
    file_type TEXT NOT NULL,
    file_size_bytes BIGINT,

    storage_reference TEXT NOT NULL,

    extracted_text TEXT,

    processing_status TEXT NOT NULL DEFAULT 'PENDING',

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_resume_status
        CHECK (
            processing_status IN (
                'PENDING',
                'PROCESSING',
                'COMPLETED',
                'FAILED'
            )
        )
);
```

ไม่ควรเก็บ Binary File ขนาดใหญ่ใน Table หากไม่มีเหตุผลจำเป็น

แนะนำ:

```text
File Storage
     ↓
storage_reference
     ↓
PostgreSQL
```

แทนการเก็บไฟล์โดยตรงใน Database

Index:

```sql
CREATE INDEX idx_resume_session
ON resume(session_id);
```

---

# 13. PORTFOLIO

```sql
CREATE TABLE portfolio (
    portfolio_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    session_id UUID NOT NULL
        REFERENCES user_session(session_id)
        ON DELETE CASCADE,

    url TEXT NOT NULL,
    platform TEXT,

    status TEXT NOT NULL DEFAULT 'PENDING',

    accessible BOOLEAN,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_portfolio_status
        CHECK (
            status IN (
                'PENDING',
                'ACCESSIBLE',
                'INACCESSIBLE',
                'INVALID',
                'BLOCKED',
                'LOGIN_REQUIRED',
                'UNSUPPORTED',
                'ERROR'
            )
        )
);
```

Index:

```sql
CREATE INDEX idx_portfolio_session
ON portfolio(session_id);
```

---

# 14. PORTFOLIO_PROJECT

```sql
CREATE TABLE portfolio_project (
    project_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    portfolio_id BIGINT NOT NULL
        REFERENCES portfolio(portfolio_id)
        ON DELETE CASCADE,

    title TEXT NOT NULL,
    description TEXT,
    url TEXT,
    technologies TEXT,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

Index:

```sql
CREATE INDEX idx_portfolio_project_portfolio
ON portfolio_project(portfolio_id);
```

---

# 15. SKILL

Canonical Skill Dictionary

```sql
CREATE TABLE skill (
    skill_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    skill_name TEXT NOT NULL UNIQUE,

    category TEXT NOT NULL,

    description TEXT,

    is_active BOOLEAN NOT NULL DEFAULT TRUE,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_skill_category
        CHECK (
            category IN (
                'TECHNICAL',
                'DESIGN',
                'CREATIVE',
                'SOFTWARE_TOOL',
                'COMMUNICATION',
                'BUSINESS',
                'OTHER'
            )
        )
);
```

---

# 16. SKILL_ALIAS

เก็บชื่อเรียกอื่นของ Skill

```sql
CREATE TABLE skill_alias (
    alias_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    skill_id BIGINT NOT NULL
        REFERENCES skill(skill_id)
        ON DELETE CASCADE,

    alias TEXT NOT NULL UNIQUE
);
```

ตัวอย่าง:

```text
React
React.js
ReactJS
```

Mapping:

```text
React.js
ReactJS
    ↓
React
```

---

# 17. USER_SKILL

เก็บ Skill ที่ระบบตรวจพบในผู้ใช้

```sql
CREATE TABLE user_skill (
    user_skill_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    session_id UUID NOT NULL
        REFERENCES user_session(session_id)
        ON DELETE CASCADE,

    skill_id BIGINT NOT NULL
        REFERENCES skill(skill_id)
        ON DELETE RESTRICT,

    confidence NUMERIC(5,4),

    source TEXT NOT NULL,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT uq_user_skill
        UNIQUE (session_id, skill_id),

    CONSTRAINT chk_user_skill_source
        CHECK (
            source IN (
                'RESUME',
                'PORTFOLIO',
                'BOTH'
            )
        ),

    CONSTRAINT chk_user_skill_confidence
        CHECK (
            confidence IS NULL
            OR confidence BETWEEN 0 AND 1
        )
);
```

---

# 18. SKILL_EVIDENCE

เก็บหลักฐานที่สนับสนุน User Skill

```sql
CREATE TABLE skill_evidence (
    evidence_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    user_skill_id BIGINT NOT NULL
        REFERENCES user_skill(user_skill_id)
        ON DELETE CASCADE,

    source_type TEXT NOT NULL,

    source_reference TEXT,

    project_id BIGINT
        REFERENCES portfolio_project(project_id)
        ON DELETE SET NULL,

    evidence_text TEXT,

    confidence NUMERIC(5,4),

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_evidence_source
        CHECK (
            source_type IN (
                'RESUME_SKILL',
                'RESUME_PROJECT',
                'RESUME_EXPERIENCE',
                'RESUME_CERTIFICATE',
                'PORTFOLIO_PROJECT',
                'PORTFOLIO_DESCRIPTION',
                'PORTFOLIO_TECHNOLOGY',
                'PORTFOLIO_ARTIFACT'
            )
        ),

    CONSTRAINT chk_evidence_confidence
        CHECK (
            confidence IS NULL
            OR confidence BETWEEN 0 AND 1
        )
);
```

Index:

```sql
CREATE INDEX idx_skill_evidence_user_skill
ON skill_evidence(user_skill_id);

CREATE INDEX idx_skill_evidence_project
ON skill_evidence(project_id);
```

---

# 19. CAREER_FAMILY

```sql
CREATE TABLE career_family (
    career_family_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    family_code TEXT NOT NULL UNIQUE,

    family_name TEXT NOT NULL,

    description TEXT,

    is_active BOOLEAN NOT NULL DEFAULT TRUE,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

Initial Candidate Career Families:

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

รายการนี้เป็น Initial Framework และสามารถปรับตาม Dataset และ Validation

---

# 20. OCCUPATION

```sql
CREATE TABLE occupation (
    occupation_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    career_family_id BIGINT NOT NULL
        REFERENCES career_family(career_family_id)
        ON DELETE RESTRICT,

    occupation_name TEXT NOT NULL,

    description TEXT,

    source TEXT,

    source_identifier TEXT,

    is_active BOOLEAN NOT NULL DEFAULT TRUE,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT uq_occupation
        UNIQUE (career_family_id, occupation_name)
);
```

---

# 21. OCCUPATION_ALIAS

```sql
CREATE TABLE occupation_alias (
    alias_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    occupation_id BIGINT NOT NULL
        REFERENCES occupation(occupation_id)
        ON DELETE CASCADE,

    alias TEXT NOT NULL UNIQUE
);
```

ตัวอย่าง:

```text
Frontend Developer
Front-end Developer
Frontend Engineer
Junior Frontend Developer
```

สามารถ Map ไปยัง Canonical Occupation เดียวกันตาม Mapping Methodology

---

# 22. OCCUPATION_SKILL

เชื่อม Occupation กับ Skill

```sql
CREATE TABLE occupation_skill (
    occupation_skill_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    occupation_id BIGINT NOT NULL
        REFERENCES occupation(occupation_id)
        ON DELETE CASCADE,

    skill_id BIGINT NOT NULL
        REFERENCES skill(skill_id)
        ON DELETE RESTRICT,

    importance NUMERIC(5,4),

    demand NUMERIC(5,4),

    source TEXT,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT uq_occupation_skill
        UNIQUE (occupation_id, skill_id),

    CONSTRAINT chk_importance
        CHECK (
            importance IS NULL
            OR importance BETWEEN 0 AND 1
        ),

    CONSTRAINT chk_demand
        CHECK (
            demand IS NULL
            OR demand BETWEEN 0 AND 1
        )
);
```

### ความหมาย

`importance`

หมายถึงความสำคัญของ Skill ต่อ Occupation

`demand`

หมายถึง Labour Market Demand ที่คำนวณจากข้อมูล Job Posting

**ทั้งสองค่าต้องมีวิธีการคำนวณที่ตรวจสอบได้**

ห้ามกำหนดค่าโดยไม่มีหลักฐาน

---

# 23. JOB_POSTING

เก็บข้อมูลประกาศงาน

```sql
CREATE TABLE job_posting (
    job_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    job_title TEXT NOT NULL,

    company TEXT,

    description TEXT,

    requirements TEXT,

    experience TEXT,

    location TEXT,

    source TEXT NOT NULL,

    source_url TEXT,

    date_collected TIMESTAMPTZ NOT NULL,

    occupation_id BIGINT
        REFERENCES occupation(occupation_id)
        ON DELETE SET NULL,

    dataset_version_id BIGINT,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

หมายเหตุ:

`source_url` ใช้สำหรับ Traceability ของ Dataset ตามสิทธิ์และข้อกำหนดของแหล่งข้อมูล

---

# 24. JOB_POSTING_SKILL

```sql
CREATE TABLE job_posting_skill (
    job_posting_skill_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    job_id BIGINT NOT NULL
        REFERENCES job_posting(job_id)
        ON DELETE CASCADE,

    skill_id BIGINT NOT NULL
        REFERENCES skill(skill_id)
        ON DELETE RESTRICT,

    confidence NUMERIC(5,4),

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT uq_job_posting_skill
        UNIQUE (job_id, skill_id),

    CONSTRAINT chk_job_skill_confidence
        CHECK (
            confidence IS NULL
            OR confidence BETWEEN 0 AND 1
        )
);
```

---

# 25. DATASET_VERSION

ใช้ Traceability ของ Dataset

```sql
CREATE TABLE dataset_version (
    dataset_version_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    dataset_name TEXT NOT NULL,

    version_name TEXT NOT NULL,

    source_description TEXT,

    collected_at TIMESTAMPTZ,

    processed_at TIMESTAMPTZ,

    record_count INTEGER,

    description TEXT,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT uq_dataset_version
        UNIQUE (dataset_name, version_name)
);
```

หลังจากสร้าง Table นี้แล้ว ให้เพิ่ม Foreign Key:

```sql
ALTER TABLE job_posting
ADD CONSTRAINT fk_job_posting_dataset_version
FOREIGN KEY (dataset_version_id)
REFERENCES dataset_version(dataset_version_id)
ON DELETE SET NULL;
```

---

# 26. CAREER_RESULT

เก็บผลการแนะนำอาชีพ

```sql
CREATE TABLE career_result (
    result_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    session_id UUID NOT NULL
        REFERENCES user_session(session_id)
        ON DELETE CASCADE,

    occupation_id BIGINT NOT NULL
        REFERENCES occupation(occupation_id)
        ON DELETE RESTRICT,

    score NUMERIC(7,4),

    rank_position INTEGER NOT NULL,

    explanation TEXT,

    algorithm_version TEXT,

    dataset_version_id BIGINT
        REFERENCES dataset_version(dataset_version_id)
        ON DELETE SET NULL,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_career_rank
        CHECK (rank_position > 0),

    CONSTRAINT chk_career_score
        CHECK (
            score IS NULL
            OR score >= 0
        ),

    CONSTRAINT uq_session_occupation_result
        UNIQUE (session_id, occupation_id)
);
```

### Important

`score` คือ:

```text
Career Compatibility / Match Score
```

ไม่ใช่:

```text
Employment Probability
```

และไม่ควรเก็บคะแนนที่เกิดจาก Arbitrary Weight โดยไม่มี Methodology

---

# 27. SKILL_GAP

เก็บ Skill Gap ของ Career Result

```sql
CREATE TABLE skill_gap (
    gap_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    result_id BIGINT NOT NULL
        REFERENCES career_result(result_id)
        ON DELETE CASCADE,

    skill_id BIGINT NOT NULL
        REFERENCES skill(skill_id)
        ON DELETE RESTRICT,

    status TEXT NOT NULL,

    priority TEXT,

    reason TEXT,

    guidance TEXT,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT uq_result_skill_gap
        UNIQUE (result_id, skill_id),

    CONSTRAINT chk_skill_gap_status
        CHECK (
            status IN (
                'MATCHED',
                'PARTIAL',
                'EVIDENCE_NOT_FOUND'
            )
        ),

    CONSTRAINT chk_skill_gap_priority
        CHECK (
            priority IS NULL
            OR priority IN (
                'HIGH',
                'MEDIUM',
                'LOW'
            )
        )
);
```

---

# 28. USER_FEEDBACK

```sql
CREATE TABLE user_feedback (
    feedback_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    session_id UUID NOT NULL
        REFERENCES user_session(session_id)
        ON DELETE CASCADE,

    sus_score NUMERIC(5,2),

    satisfaction NUMERIC(5,2),

    comment TEXT,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT chk_sus_score
        CHECK (
            sus_score IS NULL
            OR sus_score BETWEEN 0 AND 100
        ),

    CONSTRAINT chk_satisfaction
        CHECK (
            satisfaction IS NULL
            OR satisfaction BETWEEN 0 AND 100
        )
);
```

---

# 29. Complete Relationship Map

```text id="c7q3wb"
major
 │
 └── user_session
       │
       ├── resume
       │
       ├── portfolio
       │     │
       │     └── portfolio_project
       │
       ├── user_skill
       │     │
       │     ├── skill
       │     │     └── skill_alias
       │     │
       │     └── skill_evidence
       │             └── portfolio_project
       │
       ├── career_result
       │     │
       │     ├── occupation
       │     │     │
       │     │     ├── career_family
       │     │     ├── occupation_alias
       │     │     └── occupation_skill
       │     │             └── skill
       │     │
       │     └── skill_gap
       │             └── skill
       │
       └── user_feedback


job_posting
 │
 ├── job_posting_skill
 │       └── skill
 │
 ├── occupation
 │
 └── dataset_version
```

---

# 30. Traceability — User Evidence

ระบบต้องสามารถ Trace:

```text id="e0l4br"
Career Result
     ↓
Matched Skill
     ↓
User Skill
     ↓
Skill Evidence
     ↓
Resume / Portfolio
```

ตัวอย่าง:

```text id="b2qzq9"
Career:
Front-end Developer

        ↓

Skill:
React

        ↓

User Skill:
React

        ↓

Evidence:
GitHub Project

        ↓

Project:
Student Management System

        ↓

Portfolio:
GitHub URL
```

---

# 31. Traceability — Labour Market

ต้องสามารถ Trace:

```text id="9wz4q8"
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

ทำให้สามารถอธิบายได้ว่า:

```text
Skill X
```

ถูกนำมาใช้ใน Career Recommendation เพราะมีหลักฐานจาก Labour Market Dataset ใด

---

# 32. Major Must Not Hard Filter Career

Database ห้ามสร้างโครงสร้าง:

```text
major
 ↓
allowed_occupation
```

เพื่อบังคับ Career Recommendation

Major มีหน้าที่เป็น:

```text
Context
```

เท่านั้น

ดังนั้น:

```text
Creative Media Technology
```

สามารถได้รับ Recommendation เช่น:

```text
UI/UX Designer
Front-end Developer
Graphic Designer
Content Strategist
```

ตาม Skills และ Evidence ที่ตรวจพบ

---

# 33. Skill Evidence Principle

Database ต้องแยก:

```text
Skill
```

ออกจาก:

```text
Evidence
```

เพราะ:

```text
Skill Exists
```

ไม่เท่ากับ:

```text
Strong Evidence
```

ตัวอย่าง:

```text
Resume:
React

Portfolio:
GitHub Project using React
```

สามารถมี Evidence สองรายการที่สนับสนุน Skill เดียวกัน

---

# 34. Evidence Not Found Principle

หาก Required Skill ไม่ปรากฏในข้อมูล:

ห้ามบันทึกความหมายว่า:

```text
USER DOES NOT HAVE SKILL
```

ให้ใช้:

```text
EVIDENCE_NOT_FOUND
```

เพราะ:

```text
No Evidence
≠
No Skill
```

---

# 35. Temporary User Data

ข้อมูลเหล่านี้เป็น Temporary:

```text
user_session
resume
portfolio
portfolio_project
user_skill
skill_evidence
career_result
skill_gap
user_feedback
```

ต้องมี Retention Policy

ตัวอย่าง:

```text
Session Created
      ↓
Analysis
      ↓
Result Display
      ↓
Retention Period
      ↓
Automatic Cleanup
```

ระยะเวลา Retention ต้องกำหนดก่อน Production

---

# 36. Knowledge Data

ข้อมูลต่อไปนี้สามารถเก็บถาวร:

```text
major
skill
skill_alias
career_family
occupation
occupation_alias
occupation_skill
```

เพราะเป็น Knowledge Base ของระบบ

---

# 37. Labour Market Data

ข้อมูล:

```text
job_posting
job_posting_skill
dataset_version
```

สามารถเก็บตาม Dataset Retention Policy

และควร Version ข้อมูลเพื่อเปรียบเทียบแต่ละช่วงเวลา

---

# 38. Delete Rules

### User Session

เมื่อ Session ถูกลบ:

```text
Resume
Portfolio
Portfolio Project
User Skill
Evidence
Career Result
Skill Gap
Feedback
```

ควรถูกลบตามความสัมพันธ์ `ON DELETE CASCADE`

### Knowledge

ไม่ควรลบ Skill หรือ Occupation ที่ถูก Reference โดยง่าย

ใช้:

```text
is_active = false
```

แทนเมื่อข้อมูลไม่ต้องการใช้ในระบบใหม่

---

# 39. Recommended Indexes

```sql
CREATE INDEX idx_resume_session
ON resume(session_id);

CREATE INDEX idx_portfolio_session
ON portfolio(session_id);

CREATE INDEX idx_portfolio_project_portfolio
ON portfolio_project(portfolio_id);

CREATE INDEX idx_user_skill_session
ON user_skill(session_id);

CREATE INDEX idx_user_skill_skill
ON user_skill(skill_id);

CREATE INDEX idx_skill_evidence_user_skill
ON skill_evidence(user_skill_id);

CREATE INDEX idx_occupation_family
ON occupation(career_family_id);

CREATE INDEX idx_occupation_skill_occupation
ON occupation_skill(occupation_id);

CREATE INDEX idx_occupation_skill_skill
ON occupation_skill(skill_id);

CREATE INDEX idx_job_posting_occupation
ON job_posting(occupation_id);

CREATE INDEX idx_job_posting_date
ON job_posting(date_collected);

CREATE INDEX idx_job_posting_skill_job
ON job_posting_skill(job_id);

CREATE INDEX idx_job_posting_skill_skill
ON job_posting_skill(skill_id);

CREATE INDEX idx_career_result_session
ON career_result(session_id);

CREATE INDEX idx_career_result_rank
ON career_result(session_id, rank_position);

CREATE INDEX idx_skill_gap_result
ON skill_gap(result_id);

CREATE INDEX idx_feedback_session
ON user_feedback(session_id);
```

---

# 40. PostgreSQL Extensions

Extensions ต้องเปิดใช้เฉพาะเมื่อมี Requirement

Possible extensions:

```sql
CREATE EXTENSION IF NOT EXISTS pgcrypto;
```

สำหรับ UUID/cryptographic functions หากจำเป็น

หากภายหลังต้องใช้ Vector Search ใน PostgreSQL:

```text
pgvector
```

สามารถพิจารณาเพิ่มเติม

แต่ **ยังไม่ควรเพิ่ม Extension เพียงเพราะมี AI**

ต้องมี Requirement จาก AI Architecture ก่อน

---

# 41. Embedding Storage

ในระยะแรก:

```text
Python
 ↓
Embedding
 ↓
Matching
```

ไม่จำเป็นต้องเก็บ Embedding ใน PostgreSQL

ถ้าระบบภายหลังต้องรองรับ Semantic Search หรือ Vector Retrieval จำนวนมาก สามารถพิจารณา:

```text
PostgreSQL
+
pgvector
```

และสร้าง Table เช่น:

```text
skill_embedding
occupation_embedding
job_posting_embedding
```

แต่เป็น **Future Extension**

ไม่ใช่ Core Schema ใน Phase แรก

---

# 42. Transaction Rules

Operation ที่เกี่ยวข้องกับหลาย Table ควรใช้ Transaction

ตัวอย่าง:

```text id="2h4qpo"
Create Career Result
      ↓
Create Skill Gap
      ↓
Commit
```

ถ้า Skill Gap Creation ล้มเหลว:

```text
Rollback
```

เพื่อป้องกัน Partial Result

---

# 43. Database Access Layer

Backend:

```text
Next.js
      ↓
Express API
      ↓
Service Layer
      ↓
Repository / Data Access Layer
      ↓
PostgreSQL
```

ไม่ควร:

```text
Controller
   ↓
Raw SQL Everywhere
```

ควรแยก:

```text
Controller
Service
Repository
```

เพื่อให้ Business Logic และ Database Logic ไม่ปะปนกัน

---

# 44. Python Database Access

Python AI Service ไม่ควรแก้ข้อมูล Database โดยตรงโดยไม่มีการกำหนด Contract

Recommended:

```text id="2gj0q9"
Node.js / Express
        ↓
Python AI Service
        ↓
AI Result
        ↓
Node.js
        ↓
PostgreSQL
```

กล่าวคือ:

```text
Python
=
AI / NLP Processing

Node.js
=
Application / Database Orchestration
```

วิธีนี้ช่วยลดปัญหา Database Logic กระจายอยู่สองภาษา

หากมีเหตุผลที่ Python ต้องอ่าน Dataset โดยตรง สามารถอนุญาตเฉพาะ Read Operation ที่กำหนดไว้

---

# 45. Migration Structure

แนะนำ:

```text
database/
│
├── migrations/
│   ├── 001_create_schema.sql
│   ├── 002_create_major.sql
│   ├── ...
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

รายการ Migration ฉบับเต็มและลำดับ Dependency อยู่ที่ `DATABASE_MIGRATION_PLAN.md` §5 (001-021) ใช้ SQL Migration Files ดู `docs/decisions/0003-database-tooling.md`

---

# 46. Seed Data Rules

Seed Data ใช้เพื่อ:

* Development
* Testing
* Demo
* Prototype

ไม่ใช่:

```text
Official Labour Market Evidence
```

ตัวอย่าง:

```text
React
HTML
CSS
JavaScript
```

สามารถใช้เป็น Seed Data เพื่อทดสอบระบบได้

แต่ Demand ของ React เช่น:

```text
0.85
```

ห้ามสร้างขึ้นเพื่อเป็นข้อมูลจริง

---

# 47. Dataset Import

ข้อมูล Labour Market ไม่ควร Insert ด้วย SQL แบบ Manual จำนวนมาก

ควรใช้ Pipeline:

```text
CSV / JSON
      ↓
Validation
      ↓
Cleaning
      ↓
Normalization
      ↓
Database Import
```

ตัวอย่าง:

```text
scripts/dataset/
    import_skills
    import_occupations
    import_job_postings
```

---

# 48. Data Integrity Rules

Database ต้องป้องกัน:

### Duplicate Skill

```text
React
React
```

ต้องไม่สามารถสร้าง Canonical Skill ซ้ำได้

### Duplicate Occupation

Canonical Occupation ต้องมี Unique Constraint

### Duplicate Occupation-Skill

```text
Front-end Developer + React
```

ต้องมีได้เพียงหนึ่ง Relationship

### Duplicate Job-Skill

```text
Job #123 + React
```

ต้องมี Relationship เดียว

---

# 49. Data Quality

Database ไม่ควรเป็นตัวแทนของ Data Quality ทั้งหมด

ต้องมี Application / Dataset Validation เพิ่มเติม

ตรวจสอบ:

```text
Missing
Duplicate
Invalid
Unmapped
Outdated
Incorrect Alias
Incorrect Occupation Mapping
```

---

# 50. Security

Backend ต้องใช้:

```text
Parameterized Queries
```

หรือ ORM/Query Builder ที่ป้องกัน SQL Injection

ห้ามสร้าง Query จาก User Input โดยต่อ String ตรง ๆ

ไม่เก็บ:

```text
API Keys
Passwords
AI System Prompts
```

ใน Database

---

# 51. Resume Privacy

Resume อาจมีข้อมูล:

```text
Name
Email
Phone
Address
Education
Experience
```

ดังนั้นควรเก็บเฉพาะข้อมูลที่จำเป็น

และกำหนด Retention Policy

หากไม่จำเป็นต้องเก็บ:

```text
Permanent Resume
```

ไม่ควรเก็บถาวร

---

# 52. Portfolio Privacy

Portfolio URL สามารถเป็น:

```text
Public
Private
Login Required
Blocked
```

Database ต้องแยกสถานะเหล่านี้

ไม่ควรสรุป:

```text
Private Portfolio
=
No Skill
```

---

# 53. Result Versioning

Career Result ควรสามารถระบุ:

```text
Algorithm Version
Dataset Version
Created At
```

ตัวอย่าง:

```text
Algorithm:
matching-v1.0

Dataset:
labour-market-2026-01

Created:
2026-09-19
```

เพื่อให้สามารถอธิบาย Result ในการประเมิน Thesis

---

# 54. Recommended View — User Skill Summary

สามารถสร้าง View สำหรับอ่านข้อมูลได้:

```sql
CREATE VIEW user_skill_summary AS
SELECT
    us.user_skill_id,
    us.session_id,
    s.skill_id,
    s.skill_name,
    s.category,
    us.confidence,
    us.source
FROM user_skill us
JOIN skill s
    ON s.skill_id = us.skill_id;
```

View เป็น Optional

---

# 55. Recommended View — Career Result Summary

สามารถสร้าง View:

```sql
CREATE VIEW career_result_summary AS
SELECT
    cr.result_id,
    cr.session_id,
    cr.rank_position,
    cr.score,
    o.occupation_id,
    o.occupation_name,
    cf.family_code,
    cf.family_name
FROM career_result cr
JOIN occupation o
    ON o.occupation_id = cr.occupation_id
JOIN career_family cf
    ON cf.career_family_id = o.career_family_id;
```

---

# 56. Backup Strategy

Production Database ต้องมี:

```text
Backup
Restore Test
Retention Policy
```

Development:

```text
Docker Volume
```

Production:

```text
Managed PostgreSQL
หรือ
PostgreSQL Server + Backup
```

ขึ้นอยู่กับ Deployment Architecture ที่กำหนดภายหลัง

---

# 57. Docker PostgreSQL

Development Environment สามารถใช้:

```text
Docker
   ↓
PostgreSQL Container
```

ตัวอย่าง Concept:

```text
services:

  postgres:
    image: postgres
    environment:
      POSTGRES_DB:
      POSTGRES_USER:
      POSTGRES_PASSWORD:
```

ค่าจริงต้องเก็บใน `.env`

ห้าม Hard-code Credentials ใน `docker-compose.yml` สำหรับ Production

---

# 58. Development Database Lifecycle

```text
Developer
   ↓
Docker PostgreSQL
   ↓
Migration
   ↓
Seed
   ↓
Development
   ↓
Test
```

Production:

```text
Production PostgreSQL
   ↓
Migration
   ↓
Production Dataset
```

ห้ามใช้ Development Database เป็น Production Database โดยตรง

---

# 59. Database Testing

ต้องมี Test อย่างน้อย:

### Schema

* Table exists
* Primary Key
* Foreign Key
* Unique Constraint

### Data

* Valid Skill
* Valid Occupation
* Valid Mapping

### Relationship

* Session → Resume
* Session → Portfolio
* User Skill → Evidence
* Occupation → Skill
* Job Posting → Skill
* Career Result → Skill Gap

### Cascade

ทดสอบ:

```text
Delete Session
 ↓
Temporary Data Deleted
```

แต่:

```text
Delete Session
 ↓
Skill Knowledge
```

ต้องยังอยู่

---

# 60. Performance Considerations

ในระยะแรกไม่ต้อง Optimize ก่อนมีข้อมูลจริง

เมื่อ Dataset โตขึ้น ให้พิจารณา:

```text
Indexes
Query Plans
Pagination
Batch Insert
Connection Pooling
Materialized Views
Partitioning
```

โดยเฉพาะ Job Posting Dataset หากมีจำนวนมาก

---

# 61. Database Implementation Order

ลำดับเชิงแนวคิด ลำดับการสร้างจริงและ Dependency ใช้ `DATABASE_MIGRATION_PLAN.md` §5 (001-021):

```text
1. PostgreSQL Environment
        ↓
2. Schema
        ↓
3. Major
        ↓
4. User Session
        ↓
5. Resume
        ↓
6. Portfolio
        ↓
7. Portfolio Project
        ↓
8. Skill
        ↓
9. Skill Alias
        ↓
10. User Skill
        ↓
11. Skill Evidence
        ↓
12. Career Family
        ↓
13. Occupation
        ↓
14. Occupation Alias
        ↓
15. Occupation Skill
        ↓
16. Dataset Version
        ↓
17. Job Posting
        ↓
18. Job Posting Skill
        ↓
19. Career Result
        ↓
20. Skill Gap
        ↓
21. User Feedback
```

---

# 62. Database Acceptance Criteria

Database ถือว่าเสร็จเมื่อ:

* PostgreSQL สามารถ Start ได้
* Migration ทำงานตั้งแต่ต้นจนจบ
* Seed Data ทำงาน
* Foreign Keys ถูกต้อง
* Unique Constraints ทำงาน
* Indexes ถูกสร้าง
* Session สามารถสร้างได้
* Resume สามารถเชื่อม Session
* Portfolio สามารถเชื่อม Session
* Project สามารถเชื่อม Portfolio
* Skill สามารถเชื่อม User
* Evidence สามารถเชื่อม Skill
* Occupation สามารถเชื่อม Career Family
* Occupation สามารถเชื่อม Skill
* Job Posting สามารถเชื่อม Skill
* Career Result สามารถเชื่อม Occupation
* Skill Gap สามารถเชื่อม Career Result
* Feedback สามารถเชื่อม Session
* Traceability ทำงาน
* Cascade Rules ทำงาน
* Database Tests ผ่าน

---

# 63. Database Non-Goals

Database นี้ไม่ได้ทำหน้าที่:

* ทำนายอาชีพด้วยตัวเอง
* สร้าง AI Score ด้วยตัวเอง
* Scrape Website โดยตรง
* วิเคราะห์ Resume โดยตรง
* วิเคราะห์ Portfolio โดยตรง
* Generate Guidance โดยตรง

Database ทำหน้าที่:

```text
Store
Organize
Relate
Version
Trace
Retrieve
```

---

# 64. Final Database Architecture

```text id="x9w8ju"
                         PostgreSQL
                              │
          ┌───────────────────┼────────────────────┐
          │                   │                    │
          ▼                   ▼                    ▼
   Temporary Data       Knowledge Base       Labour Market
          │                   │                    │
          │                   │                    │
    ┌─────┴─────┐      ┌──────┴──────┐      ┌──────┴──────┐
    │           │      │             │      │             │
 Session     Resume   Skill      Occupation  Job Posting  Dataset
    │           │      │             │      │             │
    │        Portfolio│          Skill      │          Version
    │           │      │             │      │
    │         Project  │      Occupation    │
    │           │      │          Skill     │
    │           └──────┼─────────────┘      │
    │                  │                    │
    ▼                  ▼                    ▼
 Candidate         Evidence            Market Demand
 Skill Profile          │                    │
    │                   │                    │
    └───────────────────┼────────────────────┘
                        ▼
                 Career Result
                        │
                        ▼
                   Skill Gap
                        │
                        ▼
                  Development
                   Guidance
                        │
                        ▼
                  User Feedback
```

---

# 65. Final Rules for Claude

เมื่อ Implement Database:

1. ใช้ PostgreSQL เท่านั้นสำหรับ Main Database
2. ห้ามเปลี่ยนกลับไป MySQL/MariaDB
3. ใช้ PostgreSQL-compatible SQL
4. ใช้ `GENERATED ... AS IDENTITY` สำหรับ Numeric IDs
5. ใช้ UUID สำหรับ Temporary Session
6. ใช้ `TIMESTAMPTZ` สำหรับ Timestamp
7. ใช้ Foreign Key ทุก Relationship ที่จำเป็น
8. ใช้ Unique Constraint ป้องกัน Duplicate
9. ใช้ Check Constraint สำหรับ Enumerated Values ที่เหมาะสม
10. ใช้ Transaction เมื่อ Operation ครอบคลุมหลาย Table
11. ห้ามเก็บ Password
12. ห้ามเก็บ API Key
13. ห้ามสร้าง Major → Occupation Hard Filter
14. ห้ามสร้าง Employment Probability
15. ห้ามสร้าง Labour Market Demand จากข้อมูลสมมติ
16. ต้องรักษา Evidence Traceability
17. ต้องรองรับ Dataset Version
18. ต้องรองรับ Algorithm Version ใน Career Result
19. ต้องใช้ Migration สำหรับ Schema Changes
20. ห้ามแก้ Production Database โดยตรง
21. Seed Data ต้องระบุว่าเป็น Development/Test Data
22. User Data ต้องมี Retention / Cleanup Policy
23. Python ไม่ควรเขียน Database Logic กระจายจาก Backend โดยไม่มี Contract
24. Backend เป็นผู้ควบคุม Application-Level Database Operations
25. หากต้องเพิ่ม Table ใหม่ ต้องตรวจสอบก่อนว่าไม่สามารถใช้ Entity เดิมได้
26. หาก Schema ที่ต้องการเปลี่ยนมีผลต่อ AI Matching หรือ UI ต้องปรับ Specification ที่เกี่ยวข้องด้วย

---

# 66. Status

```text
Project Concept: LOCKED
Core Workflow: LOCKED

Technology Stack: LOCKED

Frontend:
Next.js + React + TypeScript + Tailwind CSS

Backend:
Node.js + Express.js + TypeScript

AI / NLP:
Python

Database:
PostgreSQL

Container:
Docker + Docker Compose

Version Control:
Git + GitHub

Database Specification:
LOCKED

Database Engine:
PostgreSQL

MySQL / MariaDB:
NOT USED

MongoDB:
NOT USED AS MAIN DATABASE
```

---

# 67. Related Documents

Database implementation ต้องสอดคล้องกับ:

```text
PROJECT_SPEC.md
DATASET_SPEC.md
AI_MATCHING_SPEC.md
UI_UX_SPEC.md
IMPLEMENTATION_PLAN.md
TECH_STACK.md
```

หากมีความขัดแย้ง:

```text
Project Concept
        ↓
Architecture
        ↓
Database
        ↓
Implementation
```

ห้ามแก้ Core Concept เพื่อแก้ปัญหา Implementation โดยไม่ทบทวน Specification ก่อน

---

# 68. Final Principle

Database ของระบบนี้ไม่ได้มีหน้าที่เพียงเก็บข้อมูล แต่ต้องทำหน้าที่เป็น **Traceable Knowledge and Evidence Store**

ดังนั้นทุกผลลัพธ์สำคัญควรสามารถย้อนกลับได้ว่า:

```text
Career Recommendation
        ↓
เกิดจาก Occupation Skill Profile ใด
        ↓
Skill ใดที่เกี่ยวข้อง
        ↓
Skill นั้นมาจาก Labour Market Evidence ใด
```

และในฝั่งผู้ใช้:

```text
Career Recommendation
        ↓
Matched Skill ใด
        ↓
ตรวจพบจาก Resume หรือ Portfolio
        ↓
Evidence คืออะไร
        ↓
Project / Resume Section ใด
```

หลักการสำคัญคือ:

> **No Evidence → No Unsupported Claim**

และ:

> **No Arbitrary Data → No Arbitrary Recommendation**

Database ต้องสนับสนุนหลักการนี้ตลอดวงจรชีวิตของระบบ