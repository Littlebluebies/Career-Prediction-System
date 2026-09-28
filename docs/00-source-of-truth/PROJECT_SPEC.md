# PROJECT SPEC.md

# Career Prediction and Skill Gap Analysis System

## ระบบทำนายอาชีพสำหรับนักศึกษาคณะเทคโนโลยีสื่อสารมวลชนโดยอิงการวิเคราะห์ทักษะและความต้องการของตลาดแรงงาน

---

# 1. DOCUMENT PURPOSE

เอกสารนี้เป็น **Master Specification / Single Source of Truth** สำหรับการพัฒนาระบบ Career Prediction and Skill Gap Analysis System

เอกสารนี้ใช้สำหรับ:

* กำหนดแนวคิดหลักของระบบ
* กำหนดขอบเขตระบบ
* กำหนด Workflow
* กำหนด Functional Requirements
* กำหนด AI/NLP Pipeline
* กำหนด Database Concept
* กำหนด Skill และ Occupation Framework
* กำหนด Labour Market Data
* กำหนด Career Matching
* กำหนด Skill Gap Analysis
* กำหนด UI/UX
* กำหนด Testing และ Evaluation
* ใช้เป็นข้อกำหนดหลักสำหรับ AI Coding Assistant เช่น Claude

## IMPORTANT

Claude MUST treat this document as the primary specification.

Claude MUST NOT change the core concept of the system unless explicitly instructed by the project owner.

If an implementation decision is not specified in this document, Claude should:

1. Prefer the simplest maintainable solution.
2. Preserve the core system concept.
3. Avoid introducing unnecessary features.
4. Clearly identify the assumption before implementing.
5. Never silently change the system architecture.

---

# 2. PROJECT OVERVIEW

ระบบนี้เป็น Web Application สำหรับช่วยนักศึกษาคณะเทคโนโลยีสื่อสารมวลชนประเมินแนวทางอาชีพจาก:

1. Resume
2. Portfolio
3. Portfolio Evidence
4. Detected Skills
5. Academic Major
6. Occupation Knowledge
7. Labour Market Demand

ระบบจะวิเคราะห์ข้อมูลดังกล่าวเพื่อ:

* ตรวจจับทักษะของผู้ใช้
* ตรวจสอบหลักฐานของทักษะจาก Resume และ Portfolio
* สร้าง Candidate Skill Profile
* เปรียบเทียบ Candidate Skill Profile กับ Occupation Skill Profile
* พิจารณาความต้องการทักษะจากตลาดแรงงาน
* จัดอันดับอาชีพที่มีความสอดคล้องกับทักษะ
* อธิบายเหตุผลที่อาชีพถูกแนะนำ
* วิเคราะห์ Skill Gap
* แนะนำแนวทางพัฒนาทักษะ

ระบบไม่ได้รับประกันว่าผู้ใช้จะประกอบอาชีพนั้นจริงในอนาคต

คำว่า "Career Prediction" ในระบบนี้หมายถึง:

> การประเมินและจัดลำดับความเหมาะสมของอาชีพจากทักษะ หลักฐานจากผลงาน และความต้องการของตลาดแรงงาน

ไม่ใช่การทำนายอนาคตของบุคคลหรือการรับประกันการได้งาน

---

# 3. PROJECT OBJECTIVES

## Objective 1

พัฒนาระบบสำหรับประเมินและแนะนำอาชีพให้แก่นักศึกษาคณะเทคโนโลยีสื่อสารมวลชน

## Objective 2

วิเคราะห์ทักษะจาก Resume และ Portfolio Evidence ของผู้ใช้

## Objective 3

วิเคราะห์ความสัมพันธ์ระหว่างทักษะของผู้ใช้กับความต้องการทักษะของตลาดแรงงาน

## Objective 4

แนะนำอาชีพที่มีความสอดคล้องกับทักษะของผู้ใช้ พร้อมแสดงเหตุผลประกอบ

## Objective 5

วิเคราะห์ Skill Gap และนำเสนอแนวทางพัฒนาทักษะที่เกี่ยวข้องกับอาชีพเป้าหมาย

## Objective 6

ประเมินประสิทธิภาพของระบบและความพึงพอใจของผู้ใช้งาน

---

# 4. TARGET USERS

Primary users:

* นักศึกษาคณะเทคโนโลยีสื่อสารมวลชน
* นักศึกษาที่กำลังเตรียมฝึกงาน
* นักศึกษาที่กำลังเตรียมสมัครงาน
* นักศึกษาที่ต้องการสำรวจแนวทางอาชีพ

Secondary users:

* อาจารย์
* ผู้ดูแลโครงการ
* ผู้วิจัย

---

# 5. FACULTY SCOPE

ระบบมีเป้าหมายรองรับนักศึกษาทั้งคณะ

## Branch 1

เทคโนโลยีการผลิตภาพยนตร์และวิทยุโทรทัศน์

## Branch 2

เทคโนโลยีการโฆษณาและประชาสัมพันธ์

## Branch 3

เทคโนโลยีการพิมพ์ดิจิทัลและบรรจุภัณฑ์

## Branch 4

ครีเอทีฟมีเดียเทคโนโลยี

Sub-majors:

* Web Full Stack
* Game Development

---

# 6. DEVELOPMENT PHASE

## Semester 1

พัฒนาระบบต้นแบบ (Pilot System)

Initial scope:

> Creative Media Technology — Web Full Stack

เป้าหมายคือทำให้ระบบ Core Engine สามารถทำงานได้จริงก่อน

Core Engine ต้องไม่ถูกออกแบบเฉพาะสำหรับ Web Full Stack

---

## Semester 2

ขยายระบบให้ครอบคลุม:

1. Film & Television
2. Advertising & Public Relations
3. Digital Printing & Packaging
4. Creative Media Technology

   * Web Full Stack
   * Game Development

การเพิ่มสาขาใน Semester 2 ควรเกิดจากการเพิ่ม:

* Occupations
* Skills
* Skill aliases
* Job postings
* Occupation-skill relationships

ไม่ควรต้องเขียน Matching Algorithm ใหม่สำหรับแต่ละสาขา

---

# 7. CORE DESIGN PRINCIPLES

หลักการต่อไปนี้เป็นข้อกำหนดสำคัญของระบบ

## 7.1 No Authentication

ระบบสำหรับผู้ใช้ทั่วไปไม่มี:

* Login
* Register
* Password
* User account

ระบบใช้ temporary session identifier สำหรับเชื่อมโยงข้อมูลระหว่างขั้นตอนการประเมิน

---

## 7.2 Major Is Context, Not Hard Filter

สาขาวิชาเป็นข้อมูลประกอบ ไม่ใช่ตัวกรองอาชีพ

ห้ามออกแบบระบบในลักษณะ:

```text
Web Student
    ↓
Only Web Developer
```

ต้องเป็น:

```text
Student
   ↓
Resume + Portfolio
   ↓
Detected Skills
   ↓
ALL OCCUPATIONS
   ↓
Matching
```

ตัวอย่าง:

นักศึกษา Web Full Stack มี:

* HTML
* CSS
* React
* Figma
* Photoshop
* UI Design

ระบบสามารถแนะนำ:

* Front-end Developer
* Web Designer
* UI/UX Designer
* Digital Designer
* Graphic Designer

โดยไม่จำกัดเฉพาะอาชีพของสาขาที่เรียน

---

## 7.3 Evidence-Based

ระบบไม่ควรพิจารณาเพียงข้อความ Skill ใน Resume

ต้องพยายามตรวจสอบหลักฐานจาก Portfolio

หลักการ:

```text
Portfolio URL
      ↓
Project
      ↓
Description / Technology / Deliverable
      ↓
Evidence
      ↓
Skill
```

---

## 7.4 Evidence Not Found != No Skill

ถ้าไม่พบ Skill ใน Resume หรือ Portfolio:

ห้ามสรุปว่า:

> ผู้ใช้ไม่มี Skill นี้

ควรแสดงว่า:

> ยังไม่พบหลักฐานของ Skill นี้

หรือ:

> Evidence Not Found

เหตุผล:

การไม่มีหลักฐานใน Resume หรือ Portfolio ไม่ได้หมายความว่าบุคคลนั้นไม่มีทักษะดังกล่าว

---

## 7.5 Labour-Market-Oriented

ระบบต้องอ้างอิงความต้องการทักษะจากข้อมูลประกาศงานจริง

ไม่ควรสร้าง Skill Demand จากความคิดเห็นของผู้พัฒนาเพียงอย่างเดียว

---

## 7.6 Explainable Recommendation

ระบบต้องตอบได้ว่า:

> ทำไมอาชีพนี้จึงถูกแนะนำ?

ผลลัพธ์ต้องแสดงอย่างน้อย:

* Matched Skills
* Evidence
* Labour Market Relevance
* Reason

ไม่ควรแสดงเพียง Score

---

## 7.7 Skill Gap

หลังจากแนะนำอาชีพแล้ว ระบบต้องวิเคราะห์ว่า:

> สำหรับอาชีพนี้ ผู้ใช้ยังมี Skill ใดที่ยังไม่พบหลักฐาน?

---

## 7.8 No Employment Guarantee

ระบบต้องไม่กล่าวหรือสื่อว่า:

* ผู้ใช้จะได้งาน
* ผู้ใช้จะประกอบอาชีพนี้แน่นอน
* คะแนนคือโอกาสได้งาน
* ระบบรับประกันการจ้างงาน

---

# 8. SYSTEM MASTER WORKFLOW

```text
START
  ↓
Introduction
  ↓
Select / Enter Academic Major
  ↓
Upload Resume
  ↓
Enter Portfolio URL
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
Career Matching Engine
  ↓
Career Ranking
  ↓
Explainable Career Recommendation
  ↓
Skill Gap Analysis
  ↓
Development Guidance
  ↓
User Satisfaction / SUS
  ↓
END
```

---

# 9. INPUT DATA

## 9.1 Academic Major

ข้อมูล:

```text
major_id
major_name
```

Major เป็น Context เท่านั้น

---

## 9.2 Resume

รองรับในเบื้องต้น:

* PDF
* DOC
* DOCX

ข้อมูลที่ควรวิเคราะห์:

* Education
* Experience
* Projects
* Skills
* Certificates
* Activities

ระบบควรเก็บข้อมูลเท่าที่จำเป็นต่อการวิเคราะห์

---

## 9.3 Portfolio

รองรับ URL เช่น:

* Personal Website
* GitHub
* GitLab
* Behance
* itch.io
* YouTube
* Online Portfolio

ข้อจำกัด:

Portfolio อาจ:

* Public
* Private
* Login Required
* Blocked
* Invalid
* Unsupported

หากเข้าถึง Portfolio ไม่ได้:

ห้ามสรุปว่าไม่มี Skill

---

# 10. RESUME ANALYSIS

Pipeline:

```text
Resume File
   ↓
File Validation
   ↓
Text Extraction
   ↓
Text Cleaning
   ↓
Section Detection
   ↓
Skill Detection
   ↓
Skill Extraction
   ↓
Skill Normalization
```

ตัวอย่าง:

```text
"Experienced with ReactJS and JavaScript"
```

ผลลัพธ์:

```text
React
JavaScript
```

---

# 11. PORTFOLIO ANALYSIS

Pipeline:

```text
Portfolio URL
      ↓
URL Validation
      ↓
Accessibility Check
      ↓
Page Retrieval
      ↓
Content Extraction
      ↓
Project Detection
      ↓
Technology / Tool Detection
      ↓
Skill Extraction
      ↓
Evidence Generation
```

ระบบควรพยายามตรวจสอบ:

* Project title
* Project description
* Technology
* Tools
* Deliverables
* Project type
* Accessible artifact information

---

# 12. SKILL EXTRACTION

Pipeline:

```text
Raw Text
   ↓
Text Cleaning
   ↓
Skill Detection
   ↓
Skill Extraction
   ↓
Normalization
```

Skill สามารถมาจาก:

```text
Resume
Portfolio
Job Posting
Occupation Data
```

---

# 13. SKILL TAXONOMY

Skill ควรแบ่งเป็นหมวดหมู่

## Technical Skill

ตัวอย่าง:

* HTML
* CSS
* JavaScript
* PHP
* Python
* SQL
* React
* Node.js
* TypeScript
* Git

## Design Skill

ตัวอย่าง:

* UI Design
* UX Design
* Typography
* Layout
* Color Theory

## Creative Skill

ตัวอย่าง:

* Storytelling
* Concept Development
* Creative Thinking
* Video Production

## Software / Tool

ตัวอย่าง:

* Figma
* Adobe Photoshop
* Adobe Illustrator
* Adobe Premiere Pro
* Adobe After Effects
* DaVinci Resolve
* Unity
* Unreal Engine

## Communication / Business

ตัวอย่าง:

* Communication
* Presentation
* Project Management
* Marketing
* Public Relations

---

# 14. SKILL NORMALIZATION

ระบบต้องรองรับ Alias

ตัวอย่าง:

```text
React
React.js
ReactJS

→ React
```

```text
Photoshop
Adobe Photoshop
PS

→ Adobe Photoshop
```

```text
Frontend Developer
Front-end Developer
Frontend Engineer

→ Canonical Occupation
```

ควรมี:

```text
SKILL
SKILL_ALIAS
```

และ:

```text
OCCUPATION
OCCUPATION_ALIAS
```

---

# 15. EVIDENCE MODEL

ระบบควรสามารถบอกได้ว่า Skill ถูกตรวจพบจากที่ใด

ตัวอย่าง:

| Skill     | Resume | Portfolio | Evidence        |
| --------- | ------ | --------- | --------------- |
| HTML      | Yes    | Yes       | Project Website |
| React     | Yes    | Yes       | GitHub Project  |
| Figma     | No     | Yes       | UI Prototype    |
| Photoshop | No     | Yes       | Graphic Project |

Evidence อาจมี:

* Source
* Project
* Description
* URL
* Detection method
* Confidence

Confidence หากนำมาใช้ควรมี:

```text
HIGH
MEDIUM
LOW
```

---

# 16. CANDIDATE SKILL PROFILE

หลังจากวิเคราะห์ Resume และ Portfolio ระบบต้องสร้าง Candidate Skill Profile

ตัวอย่าง:

```text
Candidate Skill Profile

Technical
- HTML
- CSS
- JavaScript
- React

Design
- UI Design
- UX Design

Software
- Figma
- Photoshop

Communication
- Presentation
```

แต่ละ Skill ควรมี Evidence ที่เกี่ยวข้อง

ตัวอย่าง:

```text
React
  Source: Resume
  Evidence: GitHub Project
  Confidence: High
```

---

# 17. OCCUPATION FRAMEWORK

ระบบไม่ควรให้ผู้พัฒนาสร้างรายการอาชีพจากความคิดเห็นส่วนตัวทั้งหมด

แนวทาง:

```text
ESCO / O*NET
       +
Thai Labour Market / Job Postings
       ↓
Candidate Occupation List
       ↓
Occupation Normalization
       ↓
Final Occupation Framework
```

มาตรฐานอาชีพใช้เป็น Reference Taxonomy

Job Posting ใช้เป็นข้อมูลตลาดแรงงานจริง

---

# 18. CAREER FAMILY

Initial Career Family Framework:

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

รายการนี้เป็น Starting Framework

Final occupations ต้องสามารถเพิ่ม/ปรับได้จาก:

* Standard occupation data
* Labour market data
* Occupation normalization

---

# 19. EXAMPLE OCCUPATIONS

ตัวอย่างเท่านั้น:

## Web Development

* Front-end Developer
* Back-end Developer
* Full-stack Developer
* Web Developer
* Web Application Developer

## UI/UX

* UI Designer
* UX Designer
* UI/UX Designer
* Product Designer
* UX Engineer

## Graphic / Visual

* Graphic Designer
* Visual Designer
* Brand Designer
* Digital Designer
* Art Director

## Film / Video

* Producer
* Director
* Camera Operator
* Content Producer
* Video Editor

## Game

* Game Designer
* Level Designer
* Narrative Designer
* Game Programmer
* Gameplay Programmer
* 2D Game Artist
* 3D Game Artist
* Technical Artist

These occupations MUST NOT be treated as the final fixed list.

---

# 20. LABOUR MARKET DATA

ระบบต้องมี Job Posting Dataset

Pipeline:

```text
Job Posting
    ↓
Job Title
    ↓
Description
    ↓
Requirements
    ↓
Skill Extraction
    ↓
Skill Normalization
    ↓
Skill Frequency
    ↓
Demand Analysis
    ↓
Occupation Skill Profile
```

---

# 21. JOB POSTING DATA MODEL

Recommended fields:

```text
job_id
job_title
company
description
requirements
skills
tools
experience
location
source
date_collected
occupation_id
```

ควรมี:

```text
date_collected
```

เพราะ Labour Market Data เปลี่ยนแปลงตามเวลา

---

# 22. JOB POSTING DATA PROCESSING

ต้องมี:

## Cleaning

ลบ:

* Duplicate postings
* Empty records
* Invalid records
* Irrelevant records

## Normalization

Normalize:

* Job title
* Skill names
* Tools
* Occupation aliases

## Deduplication

ประกาศงานเดียวกันที่ปรากฏหลายเว็บไซต์ไม่ควรถูกนับเป็นความต้องการหลายครั้งโดยไม่ตรวจสอบ

---

# 23. OCCUPATION-SKILL PROFILE

แต่ละ Occupation ต้องมี Skill Profile

ตัวอย่างเชิงโครงสร้าง:

```text
Occupation
    ↓
Required Skills
    ↓
Skill Importance
    ↓
Market Demand
```

ตัวอย่างเชิงแนวคิด:

```text
Front-end Developer

HTML
CSS
JavaScript
React
Git
TypeScript
Accessibility
Testing
```

ค่า Importance / Demand จริง:

**ห้ามกำหนดจากการเดา**

ควร derive จาก:

* Job Posting Dataset
* Standard occupation data
* Evaluation
* Optional expert validation

---

# 24. OCCUPATION-SKILL MATRIX

ระบบต้องสามารถสร้าง Matrix:

| Occupation          | HTML |  React |  Figma | Photoshop | Video | Communication |
| ------------------- | ---: | -----: | -----: | --------: | ----: | ------------: |
| Front-end Developer | High |   High | Medium |       Low |   Low |        Medium |
| UI/UX Designer      |  Low | Medium |   High |    Medium |   Low |          High |
| Graphic Designer    |  Low |    Low | Medium |      High |   Low |        Medium |
| Video Editor        |  Low |    Low |    Low |    Medium |  High |        Medium |

IMPORTANT:

ค่าด้านบนเป็นเพียงตัวอย่างเพื่ออธิบายโครงสร้าง

ห้าม hard-code ค่าเหล่านี้เป็นข้อมูลจริงของระบบ

---

# 25. CAREER MATCHING ENGINE

Input:

```text
Candidate Skill Profile
+
Occupation Skill Profile
+
Labour Market Demand
+
Evidence Strength
```

Output:

```text
Career Ranking
```

Conceptual model:

```text
Candidate Skills
       +
Occupation Requirements
       +
Market Demand
       +
Evidence
       ↓
Matching Engine
       ↓
Career Score
```

---

# 26. CAREER SCORE

ระบบสามารถใช้แนวคิด:

```text
Career Score
=
Skill Match
+
Evidence Strength
+
Market Relevance
```

อย่างไรก็ตาม:

**Numerical weights MUST NOT be arbitrarily fixed before evaluation.**

Weights ควรถูกกำหนดจาก:

* Research methodology
* Dataset
* Experimental comparison
* Validation results

ระบบต้องสามารถปรับ weights ได้โดยไม่ต้องแก้โครงสร้างหลักของระบบ

---

# 27. CAREER RANKING

ระบบควรแสดง Top 3–5 occupations

ตัวอย่างเท่านั้น:

```text
UI/UX Designer
Match Score: 86%

Web Designer
Match Score: 81%

Front-end Developer
Match Score: 78%
```

ตัวเลขด้านบนเป็นตัวอย่างเท่านั้น

ระบบจริงต้องคำนวณจากข้อมูลผู้ใช้และ Dataset

---

# 28. EXPLAINABLE CAREER RECOMMENDATION

ทุก Career Recommendation ต้องสามารถอธิบายได้

Structure:

```text
Career
 ↓
Matched Skills
 ↓
Evidence
 ↓
Market Demand
 ↓
Reason
```

ตัวอย่าง:

```text
UI/UX Designer

Matched Skills:
- Figma
- UI Design
- UX Design
- HTML

Evidence:
- UI Prototype Project
- Portfolio Website
- Resume

Market Relevance:
Figma และ UI-related skills ถูกตรวจพบใน Job Posting Dataset

Reason:
ผู้ใช้มีทักษะด้าน UI/UX และมีหลักฐานจาก Portfolio
ซึ่งมีความสอดคล้องกับ Skill Profile ของ UI/UX Designer
```

---

# 29. CROSS-MAJOR MATCHING

Cross-major matching เป็น Core Feature

Example:

```text
Major:
Web Full Stack

Skills:
HTML
CSS
React
Figma
Photoshop
UI Design
```

Potential recommendations:

```text
Front-end Developer
UI/UX Designer
Web Designer
Graphic Designer
Digital Designer
```

ระบบต้องไม่ใช้ Major เป็น hard constraint

Architecture:

```text
ALL OCCUPATIONS
        ↑
Career Matching Engine
        ↑
Candidate Skill Profile
        ↑
Resume + Portfolio
        ↑
Student

Major = Context
```

---

# 30. SKILL GAP ANALYSIS

หลังจากเลือก/แสดง Career Recommendation ระบบต้องวิเคราะห์ Skill Gap

Concept:

```text
Required Occupation Skills
        -
Verified / Evidenced Skills
        ↓
Skill Gap
```

ตัวอย่าง:

```text
Target:
Front-end Developer

Evidenced:
✓ HTML
✓ CSS
✓ JavaScript
✓ React

Not Evidenced:
? TypeScript
? Testing
? Accessibility
? CI/CD
```

ใช้คำว่า:

> Not Evidenced / Evidence Not Found

แทน:

> No Skill

---

# 31. SKILL GAP PRIORITY

Skill Gap สามารถแบ่ง:

```text
HIGH
MEDIUM
LOW
```

แต่ Priority ต้องอิงข้อมูล เช่น:

* Skill demand
* Skill importance
* Occupation requirements

ไม่ควรกำหนด Priority แบบ arbitrary โดยไม่มีเหตุผล

---

# 32. DEVELOPMENT GUIDANCE

ระบบควรแปลง Skill Gap เป็น Development Guidance

Pipeline:

```text
Skill Gap
   ↓
What to Learn
   ↓
What to Practice
   ↓
What to Build
```

ตัวอย่าง:

```text
Skill Gap:
TypeScript

What to Learn:
TypeScript fundamentals

What to Practice:
ใช้ TypeScript กับ React

What to Build:
สร้าง React project ที่ใช้ TypeScript
และเพิ่มลง Portfolio
```

ระบบให้คำแนะนำเพื่อการพัฒนาตนเอง

ไม่ควรกล่าวว่า:

> เรียน Skill นี้แล้วจะได้งานแน่นอน

---

# 33. PRIVACY REQUIREMENTS

Resume และ Portfolio อาจมี Personal Data

ระบบต้อง:

* Collect minimum necessary data
* Request consent before analysis
* Avoid unnecessary data retention
* Avoid permanent personal profiles
* Provide appropriate retention/deletion policy
* Protect uploaded files
* Avoid exposing personal data

Recommended flow:

```text
Upload
 ↓
Process
 ↓
Generate Result
 ↓
Temporary Storage
 ↓
Delete / Retention Policy
```

---

# 34. DATABASE CONCEPT

Initial database entities:

```text
USER_SESSION
RESUME
PORTFOLIO
PORTFOLIO_PROJECT

SKILL
SKILL_ALIAS
USER_SKILL
SKILL_EVIDENCE

CAREER_FAMILY
OCCUPATION
OCCUPATION_ALIAS
OCCUPATION_SKILL

JOB_POSTING
JOB_POSTING_SKILL

CAREER_RESULT
SKILL_GAP

USER_FEEDBACK
```

Relationship:

```text
USER_SESSION
 ├── RESUME
 └── PORTFOLIO
      └── PORTFOLIO_PROJECT
           └── SKILL_EVIDENCE
                └── USER_SKILL
                     └── CAREER_RESULT
                          ├── OCCUPATION
                          └── SKILL_GAP

OCCUPATION
 └── OCCUPATION_SKILL
      ↑
JOB_POSTING_SKILL
      ↑
JOB_POSTING
```

รายละเอียด SQL Schema จะถูกกำหนดใน:

```text
DATABASE.md
```

---

# 35. SUGGESTED DATABASE TABLES

> รายการนี้เป็นข้อเสนอเชิงแนวคิด Schema จริงอยู่ที่ `DATABASE.md` (19 ตาราง เพิ่ม `MAJOR` และ `DATASET_VERSION`)

## USER_SESSION

```text
session_id
created_at
expires_at
major_id
```

## RESUME

```text
resume_id
session_id
file_name
file_path / storage_reference
file_type
extracted_text
created_at
```

## PORTFOLIO

```text
portfolio_id
session_id
url
status
accessible
created_at
```

## PORTFOLIO_PROJECT

```text
project_id
portfolio_id
title
description
url
technologies
created_at
```

## SKILL

```text
skill_id
skill_name
category
description
```

## SKILL_ALIAS

```text
alias_id
skill_id
alias
```

## USER_SKILL

```text
user_skill_id
session_id
skill_id
confidence
source
```

## SKILL_EVIDENCE

```text
evidence_id
user_skill_id
source_type
source_reference
project_id
evidence_text
confidence
```

## CAREER_FAMILY

```text
career_family_id
family_code
family_name
description
```

## OCCUPATION

```text
occupation_id
career_family_id
occupation_name
description
source
```

## OCCUPATION_ALIAS

```text
alias_id
occupation_id
alias
```

## OCCUPATION_SKILL

```text
occupation_skill_id
occupation_id
skill_id
importance
demand
source
```

## JOB_POSTING

```text
job_id
job_title
company
description
requirements
experience
location
source
date_collected
occupation_id
```

## JOB_POSTING_SKILL

```text
job_posting_skill_id
job_id
skill_id
confidence
```

## CAREER_RESULT

```text
result_id
session_id
occupation_id
score
rank
explanation
created_at
```

## SKILL_GAP

```text
gap_id
result_id
skill_id
priority
reason
guidance
```

## USER_FEEDBACK

```text
feedback_id
session_id
sus_score
satisfaction
comment
created_at
```

---

# 36. SYSTEM ARCHITECTURE

Recommended architecture:

```text
┌──────────────────────────────┐
│       Presentation Layer     │
│ Web UI / Result / Feedback   │
└──────────────┬───────────────┘
               ↓
┌──────────────────────────────┐
│       Application Layer      │
│ Career Assessment Workflow   │
└──────────────┬───────────────┘
               ↓
┌──────────────────────────────┐
│        AI / Analysis Layer   │
│ NLP / Extraction / Matching  │
└──────────────┬───────────────┘
               ↓
┌──────────────────────────────┐
│        Knowledge Layer       │
│ Skill / Occupation / Career  │
└──────────────┬───────────────┘
               ↓
┌──────────────────────────────┐
│    Labour Market Data Layer  │
│ Job Posting / Demand Data    │
└──────────────┬───────────────┘
               ↓
┌──────────────────────────────┐
│      Database / Storage      │
└──────────────────────────────┘
```

---

# 37. UI/UX STRUCTURE

Initial user-facing pages:

```text
01. Landing Page
02. Introduction
03. Major Selection
04. Resume Upload
05. Portfolio Input
06. Privacy Consent
07. Analysis Progress
08. Candidate Skill Profile
09. Career Recommendation
10. Career Explanation
11. Skill Gap
12. Development Guidance
13. SUS / Feedback
14. Final Result
```

---

# 38. LANDING PAGE

Purpose:

Explain:

* What the system does
* Who should use it
* What information is required
* What result will be generated

Primary CTA:

```text
เริ่มประเมินอาชีพ
```

---

# 39. MAJOR SELECTION

User selects:

* Branch
* Major / Program

Major information is stored as context.

Major MUST NOT restrict occupation candidates.

---

# 40. RESUME UPLOAD PAGE

Features:

* Upload Resume
* File type validation
* File size validation
* Error handling
* Processing status

After successful upload:

```text
Resume uploaded successfully
```

---

# 41. PORTFOLIO PAGE

Input:

```text
Portfolio URL
```

Support multiple URLs if practical.

Examples:

```text
GitHub
Behance
Personal Website
GitLab
itch.io
YouTube
```

If inaccessible:

```text
Portfolio could not be accessed.

This does not mean that the user does not have the related skills.
```

---

# 42. PRIVACY CONSENT

Before processing personal documents:

Display:

* Purpose of data processing
* Types of data used
* Temporary storage information
* Deletion / retention policy

User must consent before analysis.

---

# 43. ANALYSIS PAGE

Display processing stages:

```text
✓ Resume uploaded
✓ Resume analyzed
✓ Portfolio analyzed
✓ Skills extracted
✓ Skills normalized
✓ Evidence analyzed
● Career matching
○ Skill Gap
```

Avoid displaying fake progress if the backend is not actually processing those stages.

---

# 44. CANDIDATE SKILL PROFILE PAGE

Display:

```text
Technical Skills
Design Skills
Creative Skills
Software
Communication
```

Each skill should be able to show:

* Source
* Evidence
* Confidence

Example:

```text
React
High Confidence

Sources:
Resume
GitHub Project
```

---

# 45. CAREER RECOMMENDATION PAGE

Display Top 3–5 Careers

Each card should contain:

```text
Occupation Name
Match Score
Matched Skills
Evidence
Market Relevance
Why this career?
```

Example structure:

```text
UI/UX Designer

Match Score: XX%

Matched Skills:
- Figma
- UI Design
- UX Design

Evidence:
- Portfolio Project
- Resume

Market Relevance:
Detected in labour-market dataset

Why:
Explanation generated from actual matching data
```

---

# 46. CAREER EXPLANATION

User should be able to inspect why an occupation was recommended.

Possible sections:

```text
Why this career?

1. Skill Match
2. Portfolio Evidence
3. Resume Evidence
4. Labour Market Demand
5. Overall Matching Reason
```

---

# 47. SKILL GAP PAGE

For each selected occupation:

```text
Your Skills
Required Skills
Skill Gap
Priority
```

Example:

```text
✓ HTML
✓ CSS
✓ React

! TypeScript
! Testing
! Accessibility
```

---

# 48. DEVELOPMENT GUIDANCE PAGE

For each Skill Gap:

```text
Skill
Why it matters
What to learn
What to practice
Suggested project
```

Guidance should be actionable.

---

# 49. USER SATISFACTION

At the end of the system:

Use:

> System Usability Scale (SUS)

Additional questions may measure:

* Satisfaction
* Perceived usefulness
* Recommendation usefulness
* Comments

SUS should remain separate from model accuracy evaluation.

---

# 50. SYSTEM EVALUATION

Three main levels:

## 50.1 Skill Extraction

Metrics:

* Precision
* Recall
* F1-score

---

## 50.2 Career Recommendation

Possible metrics:

* Top-1 Accuracy
* Top-3 Accuracy / Hit Rate
* Precision@K

This requires an appropriate reference / ground truth dataset.

---

## 50.3 Usability

Use:

* SUS
* User Satisfaction

---

# 51. EXPERT VALIDATION

Expert validation is optional.

If experts are available:

## AI/ML Expert

Can validate:

* NLP methodology
* AI/ML approach
* Matching methodology
* Data processing
* Algorithm design

## Media / Career Domain Expert

Can validate:

* Occupation framework
* Skill requirements
* Occupation-Skill relationships

Important:

An AI/ML expert MUST NOT automatically be described as an expert in all four media career domains unless their qualifications actually support that claim.

Experts are validators, not the sole source for creating the occupation framework.

Preferred methodology:

```text
Standard Occupation Data
+
Labour Market Data
↓
Candidate Occupations
↓
Expert Validation
↓
Final Framework
```

---

# 52. SDG ALIGNMENT

Primary:

## SDG 4 — Quality Education

The system helps students:

* Understand their skills
* Understand labour-market requirements
* Identify skill gaps
* Plan skill development

Secondary:

## SDG 8 — Decent Work and Economic Growth

The system supports:

* Career preparation
* Internship preparation
* Employment readiness

Supporting:

## SDG 9 — Industry, Innovation and Infrastructure

The system uses:

* AI
* NLP
* Digital data
* Labour-market intelligence

Priority:

```text
SDG 4
 ↓
SDG 8
 ↓
SDG 9
```

---

# 53. NON-FUNCTIONAL REQUIREMENTS

## Performance

The system should:

* Validate files efficiently
* Avoid unnecessary repeated NLP processing
* Cache reusable normalized data where appropriate
* Avoid processing the same job posting repeatedly

## Reliability

The system must gracefully handle:

* Invalid Resume
* Unsupported file
* Empty Resume
* Invalid URL
* Private Portfolio
* Blocked Portfolio
* Network error
* Parsing failure
* AI/NLP failure
* Missing data

## Security

The system should:

* Validate uploaded files
* Restrict executable file uploads
* Sanitize extracted content
* Prevent path traversal
* Protect temporary files
* Prevent SQL injection
* Validate external URLs
* Avoid exposing internal errors to users

## Maintainability

The system should separate:

```text
Frontend
Backend
AI/NLP
Database
Dataset
Configuration
```

---

# 54. ERROR HANDLING

The system must not fail silently.

Examples:

## Invalid Resume

```text
ไม่สามารถอ่านไฟล์ Resume นี้ได้
กรุณาตรวจสอบรูปแบบไฟล์และลองใหม่อีกครั้ง
```

## Portfolio inaccessible

```text
ไม่สามารถเข้าถึง Portfolio ได้

ระบบจะยังคงวิเคราะห์ข้อมูลจาก Resume
และจะไม่ถือว่าการเข้าถึง Portfolio ไม่สำเร็จ
หมายความว่าผู้ใช้ไม่มีทักษะดังกล่าว
```

## No Skill Detected

```text
ไม่พบหลักฐาน Skill ที่ชัดเจนจากข้อมูลที่ส่งมา
```

Do not say:

```text
คุณไม่มี Skill นี้
```

---

# 55. WHAT THE SYSTEM MUST NOT DO

Claude MUST NOT implement the following unless explicitly requested:

## 1. No forced occupation by major

Do NOT:

```text
if major == "Web":
    careers = webCareers
```

## 2. No login system

Do NOT add:

* Register
* Login
* Password
* User account

## 3. No arbitrary occupation list

Do NOT create occupations solely from developer assumptions.

## 4. No arbitrary skill weights

Do NOT hard-code:

```text
React = 10
HTML = 8
Figma = 5
```

without a defined methodology.

## 5. No unsupported claims

Do NOT claim:

```text
User has no skill
```

when evidence is merely absent.

Use:

```text
Evidence Not Found
```

## 6. No employment guarantee

Do NOT claim:

```text
You will get this job
```

or:

```text
You have an 86% chance of getting hired
```

unless a separately validated employment-probability model actually exists.

The Match Score represents compatibility, not hiring probability.

## 7. No score-only recommendation

Every recommendation needs an explanation.

## 8. No unnecessary personal-data retention

Do not create permanent student profiles unless explicitly required.

## 9. No separate matching algorithm for each major

Core algorithm must remain general.

---

# 56. CODE ARCHITECTURE PRINCIPLE

The system should be data-driven.

Preferred:

```text
Occupation Data
       +
Skill Data
       +
Job Posting Data
       ↓
Generic Matching Engine
       ↓
Results
```

Not:

```text
if Web:
    algorithm A

if Game:
    algorithm B

if Film:
    algorithm C
```

Adding a new occupation should preferably require adding data rather than rewriting application logic.

---

# 57. RECOMMENDED DEVELOPMENT ORDER

Claude MUST implement the system incrementally.

Step ด้านล่างเป็นลำดับเชิงแนวคิด เลข Phase ที่ใช้พัฒนาจริงอยู่ใน `IMPLEMENTATION_PLAN.md` §3 และ `CLAUDE.md` §8

| Step | Phase ที่ตรงกัน |
| --- | --- |
| 1 Project Foundation | 0 |
| 2 Database | 1 |
| 3 Skill Taxonomy, 4 Occupation Framework | 2 |
| 5 Labour Market Dataset | 3 |
| 6 Resume Analysis | 4 |
| 7 Portfolio Analysis | 5 |
| 8 Candidate Skill Profile | 6 |
| 9 Career Matching, 10 Explainability | 7 |
| 11 Skill Gap, 12 Development Guidance | 8 |
| 13 Frontend Completion | 10 |
| 14 Testing | 11-12 |

Phase 9 (Backend API) พัฒนาควบคู่ไปกับแต่ละ Step และ Phase 13 คือ Deployment

## Step 1 — Project Foundation

* Project structure
* Environment configuration
* Database connection
* Basic frontend
* Basic backend
* Error handling

## Step 2 — Database

Implement:

* Tables
* Relationships
* Constraints
* Indexes
* Seed mechanism

## Step 3 — Skill Taxonomy

Implement:

* SKILL
* SKILL_ALIAS
* Categories
* Normalization

## Step 4 — Occupation Framework

Implement:

* CAREER_FAMILY
* OCCUPATION
* OCCUPATION_ALIAS
* OCCUPATION_SKILL

## Step 5 — Labour Market Dataset

Implement:

* JOB_POSTING
* JOB_POSTING_SKILL
* Cleaning
* Deduplication
* Normalization
* Demand calculation

## Step 6 — Resume Analysis

Implement:

* File upload
* Text extraction
* Cleaning
* Skill extraction
* Skill normalization

## Step 7 — Portfolio Analysis

Implement:

* URL validation
* Accessibility checking
* Content extraction
* Project extraction
* Evidence extraction

## Step 8 — Candidate Skill Profile

Combine:

```text
Resume Skills
+
Portfolio Skills
+
Evidence
```

## Step 9 — Career Matching

Implement:

* Skill matching
* Evidence strength
* Market relevance
* Score calculation
* Ranking

## Step 10 — Explainability

Implement:

* Matched skills
* Evidence
* Market demand
* Reason

## Step 11 — Skill Gap

Implement:

* Required skills
* Evidenced skills
* Gap detection
* Priority

## Step 12 — Development Guidance

Implement:

* Learning guidance
* Practice guidance
* Project guidance

## Step 13 — Frontend Completion

Implement:

* Complete user flow
* Results UI
* Skill Profile
* Career Recommendation
* Skill Gap
* Guidance
* Feedback

## Step 14 — Testing

Perform:

* Unit testing
* Integration testing
* Error testing
* Skill extraction evaluation
* Career recommendation evaluation
* Usability testing

---

# 58. CODING RULES FOR CLAUDE

When implementing code:

1. Do not rewrite unrelated working modules.
2. Do not silently change database schema.
3. Explain schema changes before applying them.
4. Keep backend and frontend responsibilities separated.
5. Use environment variables for secrets.
6. Never hard-code API keys.
7. Validate all user inputs.
8. Sanitize uploaded files.
9. Use parameterized SQL queries.
10. Keep AI/NLP logic modular.
11. Keep Matching Engine independent from UI.
12. Keep dataset processing separate from user request processing.
13. Log errors without exposing sensitive data.
14. Use meaningful names.
15. Avoid unnecessary dependencies.
16. Add comments only where logic is non-obvious.
17. Do not duplicate business logic between frontend and backend.
18. Do not hard-code career results.
19. Do not hard-code skill demand.
20. Do not hard-code major-to-career restrictions.

---

# 59. CONFIGURATION PRINCIPLE

Values likely to change should be configurable.

Examples:

```text
TOP_K_CAREERS
MATCHING_WEIGHTS
MIN_CONFIDENCE
PORTFOLIO_TIMEOUT
MAX_UPLOAD_SIZE
ALLOWED_FILE_TYPES
DATA_RETENTION_PERIOD
```

Do not scatter these values throughout source code.

---

# 60. DATA VERSIONING

Labour-market data changes over time.

The system should record:

```text
source
date_collected
dataset_version
```

Where practical, matching results should be traceable to the dataset version used.

Example:

```text
Labour Market Dataset
Version: 2026-XX
Collected: YYYY-MM-DD
```

---

# 61. TRACEABILITY

The system should be able to trace:

```text
Career Recommendation
        ↓
Occupation
        ↓
Occupation Skills
        ↓
Labour Market Evidence
        ↓
Candidate Skills
        ↓
Resume / Portfolio Evidence
```

This is important for explainability and thesis evaluation.

---

# 62. RESULT DATA STRUCTURE

Conceptual result:

```json
{
  "occupation": "UI/UX Designer",
  "score": 0,
  "rank": 1,
  "matched_skills": [],
  "evidence": [],
  "market_relevance": [],
  "explanation": "",
  "skill_gaps": []
}
```

Actual score and data MUST be generated dynamically.

---

# 63. EXAMPLE END-TO-END SCENARIO

Input:

```text
Major:
Web Full Stack

Resume:
HTML
CSS
JavaScript
React
Figma

Portfolio:
GitHub
Personal Website
```

System processing:

```text
Resume
 ↓
Extract Skills
 ↓
HTML
CSS
JavaScript
React
Figma
```

Portfolio:

```text
GitHub Project
 ↓
React Project
 ↓
Evidence: React
```

Personal Website:

```text
UI Prototype
 ↓
Evidence: UI Design
Figma
```

Candidate Profile:

```text
HTML
CSS
JavaScript
React
Figma
UI Design
```

Matching:

```text
ALL OCCUPATIONS
        ↓
Skill Matching
        ↓
Market Demand
        ↓
Ranking
```

Possible output:

```text
Career A
Career B
Career C
```

Each result must contain explanation.

Then:

```text
Selected Career
       ↓
Required Skills
       -
Evidenced Skills
       ↓
Skill Gap
       ↓
Development Guidance
```

---

# 64. CORE SYSTEM DATA FLOW

```text
                USER
                 │
                 ▼
        ┌─────────────────┐
        │ Resume +        │
        │ Portfolio       │
        └────────┬────────┘
                 │
                 ▼
        ┌─────────────────┐
        │ Input Processing│
        └────────┬────────┘
                 │
        ┌────────┴────────┐
        ▼                 ▼
   Resume Analysis   Portfolio Analysis
        │                 │
        └────────┬────────┘
                 ▼
        ┌─────────────────┐
        │ Skill Extraction│
        └────────┬────────┘
                 ▼
        ┌─────────────────┐
        │ Normalization   │
        └────────┬────────┘
                 ▼
        ┌─────────────────┐
        │ Evidence Layer  │
        └────────┬────────┘
                 ▼
        ┌─────────────────┐
        │ Candidate Skill │
        │ Profile         │
        └────────┬────────┘
                 │
       ┌─────────┴─────────┐
       ▼                   ▼
Occupation Data      Labour Market Data
       │                   │
       └─────────┬─────────┘
                 ▼
        ┌─────────────────┐
        │ Matching Engine │
        └────────┬────────┘
                 ▼
        ┌─────────────────┐
        │ Career Ranking   │
        └────────┬────────┘
                 ▼
        ┌─────────────────┐
        │ Explainability   │
        └────────┬────────┘
                 ▼
        ┌─────────────────┐
        │ Skill Gap        │
        └────────┬────────┘
                 ▼
        ┌─────────────────┐
        │ Development      │
        │ Guidance         │
        └────────┬────────┘
                 ▼
        ┌─────────────────┐
        │ SUS / Feedback   │
        └─────────────────┘
```

---

# 65. THESIS RESEARCH POSITIONING

The system should be positioned as:

> Evidence-Based + Labour-Market-Oriented + Cross-Major + Explainable + Skill-Gap-Oriented Career Assessment System

Core statement:

> ระบบไม่ได้ทำนายอาชีพจากสาขาวิชาที่ผู้เรียนศึกษาเพียงอย่างเดียว แต่ประเมินความเหมาะสมของอาชีพจากทักษะที่ตรวจพบ หลักฐานจากผลงาน และความต้องการทักษะของตลาดแรงงาน พร้อมระบุช่องว่างทักษะเพื่อสนับสนุนการพัฒนาตนเองก่อนเข้าสู่ตลาดแรงงาน

---

# 66. CHAPTER 1 ALIGNMENT

The implementation must support:

## Background

* Changing labour market
* Importance of skills
* Difference between major and actual skills
* Career uncertainty
* Skill gap
* Labour-market alignment

## Objectives

Must align with:

```text
System Development
Skill Analysis
Labour Market Analysis
Career Recommendation
Skill Gap
Evaluation
```

## Scope

Semester 1:

```text
Web Full Stack Pilot
```

Semester 2:

```text
Whole Faculty
```

---

# 67. CHAPTER 2 ALIGNMENT

Relevant theoretical concepts:

```text
Person–Job Fit
Human Capital Theory
Skill Gap
Skill Mismatch
Skill Taxonomy
Labour Market Analysis
Job Posting Analysis
Natural Language Processing
Semantic Similarity
Embeddings
Recommender Systems
Explainable AI
Resume Analysis
Portfolio Analysis
System Usability Scale
SDG 4
SDG 8
SDG 9
```

---

# 68. CHAPTER 3 ALIGNMENT

Research / development methodology should cover:

```text
Requirement Analysis
 ↓
Data Collection
 ↓
Data Preparation
 ↓
Skill Taxonomy
 ↓
Occupation Framework
 ↓
Labour Market Analysis
 ↓
Resume Analysis
 ↓
Portfolio Analysis
 ↓
Skill Extraction
 ↓
Skill Normalization
 ↓
Matching Algorithm
 ↓
Skill Gap
 ↓
System Development
 ↓
Testing
 ↓
Evaluation
```

---

# 69. ACCEPTANCE CRITERIA

The system can be considered functionally complete when:

## Input

* [ ] User can select major
* [ ] User can upload Resume
* [ ] User can enter Portfolio URL
* [ ] User can provide consent

## Analysis

* [ ] Resume can be parsed
* [ ] Portfolio can be analyzed when accessible
* [ ] Skills can be extracted
* [ ] Skills can be normalized
* [ ] Evidence can be recorded

## Career

* [ ] Occupations are data-driven
* [ ] Labour-market data is incorporated
* [ ] Major does not hard-filter careers
* [ ] Career ranking is generated
* [ ] Top careers are displayed
* [ ] Recommendations are explainable

## Skill Gap

* [ ] Required skills can be identified
* [ ] Evidenced skills can be identified
* [ ] Skill gaps can be generated
* [ ] Priority can be assigned
* [ ] Development guidance can be shown

## Evaluation

* [ ] Skill extraction can be evaluated
* [ ] Career recommendation can be evaluated
* [ ] SUS can be collected
* [ ] User satisfaction can be collected

## Privacy

* [ ] Consent exists
* [ ] Temporary data handling exists
* [ ] Sensitive/unnecessary data is minimized
* [ ] Retention/deletion policy exists

---

# 70. DEFINITION OF DONE

A feature is not considered complete merely because the UI exists.

Each feature should satisfy:

```text
UI
+
Backend
+
Database
+
Validation
+
Error Handling
+
Testing
```

For AI/NLP features:

```text
Input
+
Processing
+
Output
+
Evidence / Traceability
+
Evaluation
```

---

# 71. FUTURE EXTENSIBILITY

The architecture should allow future additions such as:

* Additional faculties
* Additional occupations
* Additional skills
* Additional job sources
* Additional portfolio platforms
* Additional NLP models
* Additional recommendation algorithms
* Additional evaluation methods

without rewriting the entire system.

---

# 72. FINAL SYSTEM PRINCIPLE

The system is fundamentally:

```text
STUDENT
   ↓
RESUME + PORTFOLIO
   ↓
SKILL + EVIDENCE
   ↓
CANDIDATE SKILL PROFILE
   ↓
OCCUPATION + LABOUR MARKET
   ↓
CAREER MATCHING
   ↓
EXPLAINABLE CAREER RECOMMENDATION
   ↓
SKILL GAP
   ↓
DEVELOPMENT GUIDANCE
```

The most important principle is:

> **Career should be matched from evidence of skills and labour-market requirements, not determined solely by the student's academic major.**

The second most important principle is:

> **Absence of evidence is not evidence of absence.**

The third most important principle is:

> **Every career recommendation must be explainable and traceable to skills, evidence, and labour-market data.**

---

# 73. CLAUDE IMPLEMENTATION INSTRUCTION

Before writing substantial code, Claude MUST:

1. Read this entire specification.
2. Identify any missing implementation-level decisions.
3. Preserve all locked principles.
4. Propose the project architecture.
5. Propose the folder structure.
6. Propose the database schema.
7. Identify required external services/libraries.
8. Identify which parts require real datasets.
9. Separate prototype/mock data from production/research data.
10. Implement incrementally by phase.

Claude MUST NOT immediately generate the entire application in one step.

Recommended first implementation task:

```text
PHASE 0-1
Project Foundation
+
Database Architecture
+
Initial Database Schema
+
Seed Data Structure
```

Phase numbers follow IMPLEMENTATION_PLAN.md §3 (Phase 0 = Project Setup, Phase 1 = Database).

Then proceed phase-by-phase.

---

# 74. DOCUMENT STATUS

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

Technology Stack: LOCKED (see TECH_STACK.md §85)
Detailed SQL Schema: DATABASE.md
Detailed AI/NLP Methodology: AI_MATCHING_SPEC.md
Detailed Dataset Specification: DATASET_SPEC.md
Detailed UI/UX Specification: UI_UX_SPEC.md
Detailed Implementation Plan: IMPLEMENTATION_PLAN.md
```

# END OF PROJECT_SPEC.md