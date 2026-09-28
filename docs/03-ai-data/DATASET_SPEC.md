# DATASET_SPEC.md

# Career Prediction and Skill Gap Analysis System

## Dataset Specification

**Project:** ระบบทำนายอาชีพสำหรับนักศึกษาคณะเทคโนโลยีสื่อสารมวลชนโดยอิงการวิเคราะห์ทักษะและความต้องการของตลาดแรงงาน

**English:** Career Prediction and Skill Gap Analysis System for Mass Communication Technology Students Based on Skill Evidence and Labour Market Demand

**Document:** DATASET_SPEC.md

**Status:** Specification / Research Methodology Draft

---

## 1. Purpose

เอกสารนี้กำหนดมาตรฐาน Dataset สำหรับระบบทำนายอาชีพและวิเคราะห์ Skill Gap โดยเป็นแหล่งอ้างอิงกลางสำหรับการออกแบบ การเก็บ การทำความสะอาด การ Normalize การวิเคราะห์ และการนำข้อมูลไปใช้ในระบบ

Dataset ต้องรองรับกระบวนการหลักดังนี้

```text
Data Sources
    ↓
Data Collection
    ↓
Data Cleaning
    ↓
Data Normalization
    ↓
Skill / Occupation Mapping
    ↓
Labour Market Analysis
    ↓
Occupation–Skill Profile
    ↓
Career Matching
    ↓
Skill Gap Analysis
    ↓
Evaluation
```

Dataset Specification นี้ต้องสอดคล้องกับ:

* `PROJECT_SPEC.md`
* `DATABASE.md`
* `AI_MATCHING_SPEC.md`
* `UI_UX_SPEC.md`
* `IMPLEMENTATION_PLAN.md`

---

# 2. Dataset Principles

## 2.1 Evidence-Based

ข้อมูลที่ใช้สร้าง Skill และ Occupation Profile ต้องมีแหล่งที่มาที่ตรวจสอบได้

ตัวอย่าง:

```text
Job Posting
    ↓
Job Description
    ↓
Required Skill
    ↓
Normalized Skill
```

ไม่ควรสร้างข้อมูลตลาดแรงงานจากความคิดเห็นของผู้พัฒนาเพียงอย่างเดียว

---

## 2.2 Labour-Market-Oriented

ระบบต้องใช้ข้อมูลจาก Job Posting จริงเพื่อสะท้อนความต้องการของตลาดแรงงาน

ตัวอย่างข้อมูลที่สนใจ:

* Job Title
* Required Skills
* Tools
* Technologies
* Experience
* Education
* Responsibilities
* Location
* Date Collected

---

## 2.3 Standardized

Occupation และ Skill ควรอ้างอิงจากแหล่งข้อมูลมาตรฐาน เช่น

* ESCO
* O*NET
* แหล่งข้อมูลอาชีพ/แรงงานที่เกี่ยวข้อง
* Job Posting จริง

จากนั้นจึงสร้าง Mapping ให้เหมาะสมกับบริบทของคณะ

---

## 2.4 Traceable

ข้อมูลทุกส่วนที่นำไปสร้าง Recommendation ควรสามารถย้อนกลับไปหาแหล่งข้อมูลได้

ตัวอย่าง:

```text
Career Result
    ↓
Occupation
    ↓
Occupation Skill
    ↓
Job Posting Skill
    ↓
Job Posting
    ↓
Source + Date Collected
```

---

## 2.5 Versioned

Dataset ต้องสามารถระบุได้ว่า Recommendation ถูกสร้างจาก Dataset version ใด

ตัวอย่าง:

```text
dataset_version = 2026.01
```

ไม่ควรเปลี่ยนข้อมูลหลักโดยไม่มีการบันทึก Version

---

# 3. Dataset Categories

ระบบแบ่ง Dataset หลักออกเป็น 8 กลุ่ม

```text
A. Major Dataset
B. Occupation Dataset
C. Skill Dataset
D. Skill Alias Dataset
E. Job Posting Dataset
F. Job Posting Skill Dataset
G. Occupation–Skill Dataset
H. Evaluation / Ground Truth Dataset
```

---

# 4. Major Dataset

Major Dataset ใช้สำหรับเก็บข้อมูลสาขาวิชาของคณะ

Major เป็นเพียง **Context ของผู้ใช้**

ไม่ใช่ตัวกรองอาชีพแบบตายตัว

---

## 4.1 Faculty Branches

ระบบรองรับ 4 กลุ่มหลัก

### Branch 01

สาขาวิชาเทคโนโลยีการผลิตภาพยนตร์และวิทยุโทรทัศน์

### Branch 02

สาขาวิชาเทคโนโลยีการโฆษณาและประชาสัมพันธ์

### Branch 03

สาขาวิชาเทคโนโลยีการพิมพ์ดิจิทัลและบรรจุภัณฑ์

### Branch 04

สาขาวิชาครีเอทีฟมีเดียเทคโนโลยี

โดยสามารถมี Sub-specialization เช่น

* Web Full Stack
* Game Development

---

## 4.2 Major Fields

ตัวอย่างโครงสร้าง:

```text
major_id
branch_name
major_name
```

ตัวอย่าง:

```text
1 | ครีเอทีฟมีเดียเทคโนโลยี | Web Full Stack
2 | ครีเอทีฟมีเดียเทคโนโลยี | Game Development
```

---

# 5. Occupation Dataset

Occupation Dataset เป็นฐานข้อมูลอาชีพที่ระบบสามารถนำมาใช้เป็น Candidate Occupation

ไม่ควรสร้างรายการอาชีพทั้งหมดจากความคิดเห็นของผู้วิจัยเพียงอย่างเดียว

---

## 5.1 Occupation Source Strategy

ใช้แนวทาง:

```text
Standard Occupation Sources
        +
Thai Labour Market Data
        ↓
Candidate Occupations
        ↓
Occupation Normalization
        ↓
Occupation Alias Mapping
        ↓
Final Occupation Framework
```

แหล่งข้อมูลมาตรฐานที่สามารถนำมาพิจารณา:

* ESCO
* O*NET
* ฐานข้อมูลอาชีพที่เกี่ยวข้อง
* Job Posting ในตลาดแรงงานไทย

---

## 5.2 Occupation Fields

```text
occupation_id
career_family_id
occupation_name
description
source
```

---

## 5.3 Occupation Example

ตัวอย่างเพื่ออธิบายโครงสร้างเท่านั้น:

```text
Front-end Developer
Back-end Developer
Full-stack Developer
Web Developer
UI Designer
UX Designer
Graphic Designer
Video Editor
Motion Graphic Designer
Game Designer
Game Programmer
3D Artist
Content Creator
Digital Marketing Specialist
Public Relations Specialist
Packaging Designer
Prepress Technician
```

รายการจริงต้องผ่านกระบวนการ Dataset Preparation ก่อนนำไปใช้เป็นข้อมูลวิจัย

---

# 6. Career Family Dataset

Career Family ใช้สำหรับจัดกลุ่มอาชีพในระดับสูง

ตัวอย่าง Framework เริ่มต้น:

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

จำนวน Career Family สามารถปรับได้หลังจากตรวจสอบ Dataset จริง

---

# 7. Occupation Alias Dataset

Occupation เดียวกันอาจมีหลายชื่อในตลาดแรงงาน

ตัวอย่าง:

```text
Front-end Developer
Frontend Developer
Frontend Engineer
Junior Frontend Developer
```

อาจถูก Normalize ไปยัง Occupation เดียวกันตามเกณฑ์ที่กำหนด

---

## 7.1 Fields

```text
alias_id
occupation_id
alias
```

---

## 7.2 Alias Rules

Alias ต้องไม่ถูกใช้เพื่อรวมอาชีพที่มีหน้าที่แตกต่างกันอย่างมีนัยสำคัญ

ตัวอย่างเช่น:

```text
Frontend Developer
```

ไม่ควรถูก Normalize เป็น:

```text
Graphic Designer
```

เพียงเพราะ Job Posting เดียวกันมีทั้งสองตำแหน่ง

---

# 8. Skill Dataset

Skill Dataset เป็น Taxonomy กลางของทักษะที่ระบบใช้ทั้งในการวิเคราะห์ผู้ใช้และตลาดแรงงาน

---

## 8.1 Skill Categories

เริ่มต้นด้วยหมวด:

```text
Technical
Design
Creative
Software / Tool
Communication
Business
```

สามารถเพิ่ม Category ได้เมื่อพบความจำเป็นจาก Dataset จริง

---

## 8.2 Technical Skill Examples

```text
HTML
CSS
JavaScript
PHP
Python
SQL
React
Node.js
TypeScript
Git
REST API
Database
```

---

## 8.3 Design Skill Examples

```text
UI Design
UX Design
Typography
Layout
Color Theory
Wireframing
Prototyping
Visual Design
```

---

## 8.4 Creative Skill Examples

```text
Storytelling
Creative Thinking
Concept Development
Video Production
Scriptwriting
Content Creation
Visual Storytelling
```

---

## 8.5 Software / Tool Examples

```text
Figma
Adobe Photoshop
Adobe Illustrator
Adobe Premiere Pro
Adobe After Effects
DaVinci Resolve
Unity
Unreal Engine
```

---

## 8.6 Communication / Business Examples

```text
Communication
Presentation
Project Management
Marketing
Public Relations
Teamwork
Client Communication
```

รายการนี้เป็น Initial Taxonomy เท่านั้น

Skill ที่ใช้จริงต้องสามารถเพิ่มเติมจาก Dataset และ Job Posting ได้

---

# 9. Skill Alias Dataset

Skill เดียวกันอาจปรากฏหลายรูปแบบ

ตัวอย่าง:

```text
React
React.js
ReactJS
```

Normalize เป็น:

```text
React
```

---

## 9.1 Example

| Raw Skill    | Canonical Skill            |
| ------------ | -------------------------- |
| React.js     | React                      |
| ReactJS      | React                      |
| Photoshop    | Adobe Photoshop            |
| Adobe PS     | Adobe Photoshop            |
| JS           | JavaScript                 |
| Java Script  | JavaScript                 |
| Figma Design | Figma / UI Design ตามบริบท |

การ Normalize ต้องพิจารณาบริบทเพื่อหลีกเลี่ยงการจับคำที่ผิดความหมาย

---

# 10. Job Posting Dataset

Job Posting Dataset เป็น Dataset สำคัญสำหรับสะท้อน Labour Market Demand

---

## 10.1 Required Fields

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

---

## 10.2 Recommended Additional Fields

สามารถเพิ่ม:

```text
employment_type
salary
education_requirement
responsibilities
skills_raw
tools_raw
source_url
dataset_version_id
```

ไม่จำเป็นต้องเก็บข้อมูลทุก field หากไม่มีประโยชน์ต่อการวิเคราะห์

---

# 11. Job Posting Source

แหล่งข้อมูลต้องสามารถระบุที่มาได้

ตัวอย่างประเภท Source:

```text
Job Portal
Company Career Page
Public Labour Market Dataset
Government / Public Dataset
Research Dataset
```

หากระบบเก็บ URL:

```text
source_url
```

ควรเก็บ URL และวันที่เก็บข้อมูลด้วย

---

# 12. Job Posting Inclusion Criteria

Job Posting ที่นำมาใช้ควร:

1. เป็นตำแหน่งงานที่เกี่ยวข้องกับ Candidate Occupation
2. มีรายละเอียดงานหรือ Requirement ที่เพียงพอต่อการวิเคราะห์
3. สามารถระบุวันที่เก็บข้อมูลได้
4. มีแหล่งที่มาตรวจสอบได้
5. ไม่เป็นข้อมูลซ้ำ
6. อยู่ในช่วงเวลาที่กำหนดของการวิจัย

---

# 13. Job Posting Exclusion Criteria

ควรตัดข้อมูลออกหาก:

* ไม่มี Job Description และ Requirement ที่ใช้วิเคราะห์ได้
* ข้อมูลซ้ำ
* เป็นประกาศที่หมดอายุและไม่อยู่ในช่วง Dataset ที่กำหนด
* เป็นตำแหน่งที่ไม่เกี่ยวข้องกับ Scope
* ข้อมูลไม่สมบูรณ์จนไม่สามารถวิเคราะห์ได้
* ไม่สามารถตรวจสอบแหล่งที่มาได้

---

# 14. Sampling Scope

Researcher ต้องกำหนด:

```text
Collection Period
Target Market
Job Source
Occupation Scope
Number of Job Postings
```

ตัวอย่าง:

```text
Collection Period:
กำหนดเป็นช่วงเวลาที่ระบุในงานวิจัย

Target Market:
ประเทศไทย

Target:
ตำแหน่งงานที่เกี่ยวข้องกับสายงานของคณะ
```

ไม่ควรกำหนดจำนวน Job Posting หรือช่วงเวลาแบบตายตัวโดยไม่มีเหตุผลด้านระเบียบวิธีวิจัย

---

# 15. Data Collection Procedure

ขั้นตอน:

```text
Define Scope
    ↓
Select Sources
    ↓
Collect Job Postings
    ↓
Store Raw Data
    ↓
Record Collection Date
    ↓
Clean Data
    ↓
Deduplicate
    ↓
Extract Skills
    ↓
Normalize Skills
    ↓
Map Occupation
    ↓
Create Dataset Version
```

---

# 16. Raw Data vs Processed Data

ระบบควรแยก:

```text
RAW DATA
    ↓
PROCESSED DATA
```

## Raw Data

ข้อมูลต้นฉบับที่เก็บมา

ตัวอย่าง:

```text
Original Job Title
Original Description
Original Requirements
Original URL
Collection Date
```

## Processed Data

ข้อมูลที่ผ่านการประมวลผล

```text
Normalized Job Title
Occupation
Skills
Normalized Skills
Demand
Occupation–Skill Relationship
```

การแยกสองระดับนี้ช่วยให้สามารถตรวจสอบย้อนกลับได้

---

# 17. Data Cleaning

ก่อนนำ Dataset ไปวิเคราะห์ต้องทำความสะอาดข้อมูล

ขั้นตอน:

```text
Remove HTML / Markup
    ↓
Normalize Whitespace
    ↓
Normalize Encoding
    ↓
Remove Unnecessary Text
    ↓
Standardize Field Format
    ↓
Check Missing Values
```

---

# 18. Deduplication

Job Posting ซ้ำต้องไม่ถูกนับเป็นหลายตำแหน่งโดยไม่จำเป็น

ตรวจสอบจาก:

```text
Job Title
Company
Location
Description
Source URL
```

สามารถใช้หลาย field ร่วมกันเพื่อหา Duplicate

---

# 19. Skill Extraction from Job Posting

Pipeline:

```text
Job Description
        +
Requirements
        +
Responsibilities
        ↓
Text Cleaning
        ↓
Skill Detection
        ↓
Skill Extraction
        ↓
Skill Normalization
        ↓
Canonical Skill
```

ตัวอย่าง:

```text
"Experience with React.js and Git"

        ↓

React
Git
```

---

# 20. Skill Extraction Context

การตรวจพบ Skill ต้องพิจารณาบริบท

ตัวอย่าง:

```text
"Experience with Photoshop"
```

มีหลักฐาน Skill:

```text
Adobe Photoshop
```

แต่:

```text
"Photoshop knowledge is a plus"
```

อาจถูกเก็บเป็น Skill ที่มี Requirement Level แตกต่างกัน

ดังนั้น Dataset ควรรองรับข้อมูลด้านบริบทในอนาคต

---

# 21. Job Posting Skill Dataset

ตารางเชื่อมระหว่าง Job Posting และ Skill

Fields:

```text
job_posting_skill_id
job_id
skill_id
confidence
```

---

## 21.1 Example

```text
Job #001
    ↓
React
JavaScript
Git
HTML
CSS
```

---

# 22. Occupation Mapping

Job Posting แต่ละรายการควรถูก Mapping ไปยัง Occupation

```text
Job Title
    ↓
Occupation Alias
    ↓
Canonical Occupation
```

ตัวอย่าง:

```text
Junior Frontend Developer
Frontend Developer
Front-end Engineer
```

อาจถูก Mapping ไปยัง:

```text
Front-end Developer
```

การ Mapping ต้องใช้ทั้ง Job Title และบริบทของ Job Description หากจำเป็น

---

# 23. Occupation–Skill Dataset

Dataset นี้เป็นหัวใจสำคัญของ Career Matching

โครงสร้าง:

```text
Occupation
    +
Skill
    +
Importance
    +
Demand
    +
Source
```

Fields:

```text
occupation_skill_id
occupation_id
skill_id
importance
demand
source
```

---

# 24. Labour Market Demand

Demand ต้องมาจากข้อมูล Job Posting จริง

แนวคิดพื้นฐาน:

```text
Skill Demand
=
Number of relevant job postings containing the skill
/
Number of relevant job postings
```

เมื่อวิเคราะห์ในระดับ Occupation:

```text
Demand(skill, occupation)
=
Job postings for occupation containing skill
/
All job postings for occupation
```

สูตรนี้เป็นแนวคิดพื้นฐาน

รายละเอียด normalization, weighting และ threshold จะถูกกำหนดใน `AI_MATCHING_SPEC.md` หลังจากตรวจสอบ Dataset จริง

---

# 25. Skill Importance

Importance หมายถึงระดับความสำคัญของ Skill ต่อ Occupation

สามารถพิจารณาจาก:

```text
Standard Occupation Data
        +
Job Posting Frequency
        +
Requirement Context
        +
Optional Expert Validation
```

ไม่ควรกำหนด:

```text
HTML = 0.9
React = 0.8
```

โดยไม่มีหลักฐานหรือเกณฑ์รองรับ

---

# 26. Occupation–Skill Evidence

ทุกความสัมพันธ์ระหว่าง Occupation และ Skill ควรสามารถระบุ Source ได้

ตัวอย่าง:

```text
Front-end Developer
    ↓
React
    ↓
Source:
Job Posting Dataset
```

หรือ:

```text
Front-end Developer
    ↓
JavaScript
    ↓
Source:
Standard Occupation Source
+
Job Posting Dataset
```

---

# 27. Resume Evaluation Dataset

ใช้สำหรับประเมินความสามารถของ Skill Extraction

โครงสร้าง:

```text
resume_id
resume_text
expected_skills
annotator
annotation_date
```

---

# 28. Ground Truth Dataset

สำหรับประเมินระบบ Career Recommendation จำเป็นต้องมี Reference / Ground Truth ที่เหมาะสม

ตัวอย่าง:

```text
Candidate
    ↓
Expected / Reference Career
    ↓
System Top-K Results
```

ตัวอย่างข้อมูล:

| Candidate | Expected Career     | System Result |
| --------- | ------------------- | ------------- |
| R001      | Front-end Developer | Top 3         |
| R002      | UI/UX Designer      | Top 3         |
| R003      | Video Editor        | Top 5         |

Ground Truth ต้องมีหลักเกณฑ์ในการสร้างที่ชัดเจน

ไม่ควรสร้าง Expected Career เพื่อให้ตรงกับผลลัพธ์ของระบบ

---

# 29. Skill Annotation

สำหรับ Evaluation Dataset สามารถใช้ Human Annotation เพื่อสร้าง Reference Skill Set

ตัวอย่าง:

```text
Resume:
"Developed a responsive website using React and CSS."

Expected Skills:
React
CSS
Web Development
Responsive Web Design
```

จากนั้นเปรียบเทียบกับ:

```text
System Extracted Skills
```

---

# 30. Evaluation Dataset Structure

แนะนำ:

```text
EVALUATION_CANDIDATE
    ↓
EVALUATION_SKILL
    ↓
EVALUATION_CAREER
```

หรือเก็บเป็น Dataset แบบ:

```text
candidate_id
document_reference
expected_skills
expected_career
annotation_source
annotation_date
```

---

# 31. Dataset Versioning

ทุก Dataset สำคัญต้องมี Version

ตัวอย่าง:

```text
occupation_v1
skill_v1
job_market_2026_v1
occupation_skill_v1
evaluation_v1
```

หรือใช้:

```text
Dataset Version:
2026.01
```

---

# 32. Dataset Metadata

ทุก Dataset ควรบันทึก:

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

ตัวอย่าง:

```text
Dataset:
Thailand Job Posting Dataset

Version:
2026.01

Collection Period:
[Research-defined period]

Target:
Media / Digital / Creative-related occupations
```

---

# 33. Data Quality Checks

ก่อนนำ Dataset เข้า Production ต้องตรวจสอบ:

### Completeness

ข้อมูลสำคัญไม่ควรว่างโดยไม่มีเหตุผล

### Consistency

รูปแบบข้อมูลต้องสอดคล้องกัน

### Validity

Skill และ Occupation ต้องอยู่ใน Taxonomy ที่ถูกต้อง

### Uniqueness

ไม่ควรมี Duplicate โดยไม่จำเป็น

### Traceability

ต้องสามารถย้อนกลับไปยัง Source ได้

---

# 34. Skill Quality Check

ตรวจสอบ:

```text
Raw Skill
    ↓
Canonical Skill
    ↓
Category
    ↓
Alias
```

ตัวอย่าง:

```text
React.js
    ↓
React
    ↓
Technical
```

ต้องไม่เกิด:

```text
React.js
    ↓
React
    ↓
Software / Tool
```

โดยไม่มีเหตุผลด้าน Taxonomy ที่ชัดเจน

---

# 35. Occupation Quality Check

ตรวจสอบ:

* Occupation มีชื่อชัดเจน
* ไม่มี Duplicate Occupation
* Alias ไม่ขัดแย้ง
* Career Family ถูกต้อง
* Source ถูกบันทึก
* Job Posting Mapping สามารถตรวจสอบได้

---

# 36. Labour Market Bias

Job Posting Dataset อาจมี Bias เช่น:

* Source บางแห่งมีประกาศมากกว่า Source อื่น
* บางอาชีพมีประกาศจำนวนมากกว่าอาชีพอื่น
* บริษัทบางประเภทมีสัดส่วนสูง
* Job Posting อาจไม่สะท้อนทักษะทั้งหมดที่องค์กรใช้จริง
* งานบางประเภทอาจถูกประกาศผ่านช่องทางอื่น

ดังนั้น Labour Market Demand ต้องอธิบายว่าเป็น:

> ความต้องการทักษะที่สังเกตได้จาก Job Posting Dataset ที่เก็บในช่วงเวลาที่กำหนด

ไม่ใช่การอ้างว่าเป็นความต้องการของตลาดแรงงานทั้งหมด

---

# 37. Geographic Scope

หากงานวิจัยกำหนดประเทศไทยเป็น Target Market:

```text
Target Market = Thailand
```

สามารถเก็บ:

```text
location
```

เพื่อใช้วิเคราะห์เพิ่มเติม

เช่น:

```text
Bangkok
Chiang Mai
Chonburi
Remote
```

แต่ Location ไม่ควรนำมาเป็นตัวกรองอาชีพโดยอัตโนมัติ เว้นแต่ระบบมี Requirement ด้าน Location โดยเฉพาะ

---

# 38. Semester 1 Dataset Scope

Semester 1 ใช้เป็น Pilot Dataset

ขอบเขตเริ่มต้น:

```text
Creative Media Technology
        ↓
Web Full Stack
```

เน้นอาชีพ เช่น:

```text
Front-end Developer
Back-end Developer
Full-stack Developer
Web Developer
Web Application Developer
UI/UX Designer
```

รายการสุดท้ายต้องขึ้นอยู่กับ Dataset ที่เก็บจริง

---

# 39. Semester 2 Dataset Expansion

Semester 2 ต้องขยายจาก Pilot ไปสู่ทั้งคณะ

```text
Semester 1
    ↓
Web Full Stack Pilot
    ↓
Validate Pipeline
    ↓
Improve Dataset
    ↓
Semester 2
    ↓
Whole Faculty
```

ครอบคลุม:

```text
Film / TV
Advertising / PR
Digital Printing / Packaging
Creative Media Technology
    ├── Web Full Stack
    └── Game Development
```

---

# 40. Dataset Expansion Principle

ไม่ควรสร้างระบบแยกตามสาขา

ควรใช้ Architecture เดียวกัน:

```text
One Skill Taxonomy
        +
One Occupation Framework
        +
One Labour Market Dataset
        +
Major as Context
```

ดังนั้นนักศึกษาจากสาขาหนึ่งสามารถได้รับ Recommendation ที่อยู่นอกสาขาได้ หาก Skill Evidence มีความเหมาะสม

---

# 41. Example CSV: Skills

```csv
skill_id,skill_name,category,description
1,HTML,Technical,Markup language for web development
2,CSS,Technical,Styling technology for web interfaces
3,JavaScript,Technical,Programming language for web development
4,React,Technical,JavaScript library for user interfaces
5,Figma,Software / Tool,Design and prototyping tool
```

ข้อมูลตัวอย่างนี้เป็นเพียงโครงสร้างสำหรับ Development และไม่ถือเป็น Research Dataset

---

# 42. Example CSV: Skill Alias

```csv
alias_id,skill_id,alias
1,4,React.js
2,4,ReactJS
3,3,JS
4,3,Java Script
```

---

# 43. Example CSV: Occupation

```csv
occupation_id,career_family_id,occupation_name,description,source
1,10,Front-end Developer,Web interface development,[source]
2,10,Back-end Developer,Server-side application development,[source]
3,10,Full-stack Developer,Full-stack web application development,[source]
4,11,UI/UX Designer,Digital interface and user experience design,[source]
```

`[source]` ต้องถูกแทนที่ด้วยแหล่งข้อมูลจริงก่อนใช้ในงานวิจัย

---

# 44. Example CSV: Job Posting

```csv
job_id,job_title,company,description,requirements,experience,location,source,date_collected,occupation_id
1,Junior Frontend Developer,Example Company,[description],[requirements],0-2 years,Bangkok,[source],2026-xx-xx,1
```

ข้อมูลนี้เป็น Prototype Schema เท่านั้น

---

# 45. Example CSV: Job Posting Skill

```csv
job_posting_skill_id,job_id,skill_id,confidence
1,1,1,0.98
2,1,2,0.97
3,1,3,0.96
4,1,4,0.95
```

ค่า Confidence ในตัวอย่างไม่ใช่ค่าจริงจาก Research Dataset

---

# 46. Data Processing Pipeline

ภาพรวม Dataset Pipeline:

```text
                 ┌───────────────────┐
                 │ Standard Sources  │
                 └─────────┬─────────┘
                           │
                 ┌─────────▼─────────┐
                 │ Occupation Data   │
                 └─────────┬─────────┘
                           │
                           │
┌──────────────┐    ┌──────▼───────┐
│ Job Sources  │───►│ Raw Dataset  │
└──────────────┘    └──────┬───────┘
                           │
                    Cleaning
                           │
                    Deduplication
                           │
                    Skill Extraction
                           │
                    Skill Normalization
                           │
                    Occupation Mapping
                           │
                 ┌─────────▼─────────┐
                 │ Processed Dataset │
                 └─────────┬─────────┘
                           │
                 ┌─────────▼─────────┐
                 │ Labour Market     │
                 │ Analysis          │
                 └─────────┬─────────┘
                           │
                 ┌─────────▼─────────┐
                 │ Occupation-Skill  │
                 │ Profile           │
                 └─────────┬─────────┘
                           │
                 ┌─────────▼─────────┐
                 │ Matching Engine   │
                 └───────────────────┘
```

---

# 47. Relationship to Database

Dataset ต้องสอดคล้องกับ `DATABASE.md`

ความสัมพันธ์หลัก:

```text
MAJOR
  ↓
USER_SESSION
  ↓
RESUME
  ↓
USER_SKILL
  ↓
SKILL
  ↓
SKILL_EVIDENCE
```

และ:

```text
CAREER_FAMILY
  ↓
OCCUPATION
  ↓
OCCUPATION_SKILL
  ↓
SKILL
```

ตลาดแรงงาน:

```text
JOB_POSTING
  ↓
JOB_POSTING_SKILL
  ↓
SKILL
```

ผลลัพธ์:

```text
CAREER_RESULT
  ↓
OCCUPATION
  ↓
SKILL_GAP
  ↓
SKILL
```

---

# 48. Resume / Portfolio Data

Resume และ Portfolio ไม่ใช่ Labour Market Dataset

แต่เป็น Candidate Evidence Dataset

แบ่งเป็น:

```text
Candidate Input
    ↓
Resume
    +
Portfolio
    ↓
Extracted Evidence
    ↓
Candidate Skill Profile
```

Portfolio Evidence ต้องมี Source Reference เช่น:

```text
Portfolio URL
Project URL
Project Description
Technology
Artifact
```

---

# 49. Evidence Quality

Portfolio URL ไม่ถือเป็นหลักฐาน Skill โดยอัตโนมัติ

ตัวอย่าง:

```text
Portfolio URL
```

เพียงอย่างเดียว:

```text
Evidence = Weak / Insufficient
```

หากพบ:

```text
Project:
Website Development

Technology:
React
CSS
JavaScript

Artifact:
Accessible Website
```

จึงสามารถสร้าง Evidence ที่มีความเกี่ยวข้องกับ:

```text
React
CSS
JavaScript
Web Development
```

---

# 50. Inaccessible Portfolio

หาก Portfolio:

```text
LOGIN_REQUIRED
BLOCKED
INVALID
UNSUPPORTED
ERROR
```

ระบบต้อง:

* บันทึก Status
* ไม่สร้าง Skill จากข้อมูลที่ไม่สามารถเข้าถึงได้
* ไม่สรุปว่าผู้ใช้ไม่มี Skill
* แจ้งผู้ใช้ตามความเหมาะสม

---

# 51. Privacy Dataset Policy

Resume และ Portfolio อาจมี Personal Data

ระบบควร:

```text
Collect Minimum Data
        ↓
Obtain Consent
        ↓
Process
        ↓
Generate Result
        ↓
Temporary Storage
        ↓
Delete / Retain According to Policy
```

ไม่ควรเก็บข้อมูลส่วนบุคคลที่ไม่จำเป็นต่อวัตถุประสงค์ของระบบ

---

# 52. Research Data vs Seed Data

ต้องแยกอย่างชัดเจน

## Research Data

ข้อมูลที่เก็บจริงตามวิธีการวิจัย

ใช้สำหรับ:

* Dataset Analysis
* Labour Market Analysis
* Model Development
* Evaluation
* Thesis Results

## Seed / Mock Data

ใช้สำหรับ:

* Development
* UI Testing
* Database Testing
* Demonstration

Seed Data ห้ามนำไปอ้างว่าเป็นข้อมูลตลาดแรงงานจริง

---

# 53. Reproducibility

การเก็บ Dataset ต้องสามารถอธิบายได้ว่า:

```text
ข้อมูลมาจากไหน
↓
เก็บเมื่อใด
↓
เก็บด้วยวิธีใด
↓
Clean อย่างไร
↓
Normalize อย่างไร
↓
Map อย่างไร
↓
สร้าง Version ใด
```

เพื่อให้สามารถอธิบาย Methodology ใน Chapter 3 ได้

---

# 54. Dataset Documentation

แต่ละ Dataset ควรมีเอกสาร:

```text
datasets/
├── raw/
├── processed/
├── evaluation/
├── metadata/
└── README.md
```

Annotation และ Ground Truth อยู่ใน `evaluation/` ส่วน Metadata อยู่ใน `metadata/` ดู `docs/decisions/0006-dataset-metadata.md`

ตัวอย่าง:

```text
datasets/raw/ และ datasets/processed/ แบ่งย่อยตามชนิด Dataset
├── occupation/
├── skill/
├── job_posting/
└── occupation_skill/
```

---

# 55. Recommended Processing Scripts

เมื่อเริ่ม Coding สามารถแยก Script ตามหน้าที่:

```text
scripts/dataset/
├── clean_job_postings
├── normalize_skills
├── map_occupations
├── extract_job_skills
├── calculate_skill_demand
├── build_occupation_profiles
└── validate_dataset
```

ชื่อไฟล์จริงสามารถเปลี่ยนตาม Technology Stack

---

# 56. Dataset Validation Checklist

ก่อน Dataset พร้อมใช้งาน ต้องตรวจสอบ:

```text
[ ] Source recorded
[ ] Collection date recorded
[ ] Required fields complete
[ ] Duplicate removed
[ ] Encoding normalized
[ ] Skill aliases normalized
[ ] Occupation aliases normalized
[ ] Job postings mapped
[ ] Job posting skills extracted
[ ] Occupation–Skill relationships generated
[ ] Demand calculated from actual data
[ ] Dataset version recorded
[ ] Research data separated from seed data
[ ] Traceability available
```

---

# 57. Dataset Acceptance Criteria

Dataset ถือว่าพร้อมสำหรับระบบเมื่อ:

### Criterion 1

มี Skill Taxonomy ที่สามารถใช้ร่วมกันทั้ง Resume, Portfolio และ Job Posting

### Criterion 2

มี Occupation Framework ที่มี Source และ Alias Mapping

### Criterion 3

มี Job Posting Dataset ที่มี Collection Date และ Source

### Criterion 4

สามารถ Extract และ Normalize Skill จาก Job Posting ได้

### Criterion 5

สามารถเชื่อม:

```text
Job Posting
→ Skill
→ Occupation
```

ได้

### Criterion 6

สามารถสร้าง Occupation–Skill Profile ได้

### Criterion 7

สามารถคำนวณ Labour Market Demand จากข้อมูลจริงได้

### Criterion 8

สามารถย้อนกลับจาก Occupation–Skill ไปยัง Source ได้

### Criterion 9

Dataset สามารถ Version ได้

### Criterion 10

Semester 1 สามารถใช้ Dataset สำหรับ Web Full Stack Pilot ได้

### Criterion 11

Dataset สามารถขยายไปยังทั้ง 4 สาขาใน Semester 2 ได้

---

# 58. Claude Implementation Rules

เมื่อส่งเอกสารนี้ให้ Claude:

1. ห้ามสร้าง Labour Market Dataset จริงจากข้อมูลสมมติแล้วนำเสนอว่าเป็นข้อมูลจริง
2. ห้ามกำหนด Demand แบบสุ่ม
3. ห้ามกำหนด Skill Importance แบบสุ่ม
4. ห้ามสร้าง Occupation ทั้งหมดจากความคิดเห็นของ Developer
5. ต้องแยก Raw Data และ Processed Data
6. ต้องบันทึก Source และ Collection Date
7. ต้อง Normalize Skill ผ่าน Canonical Skill
8. ต้องรองรับ Skill Alias
9. ต้องรองรับ Occupation Alias
10. ต้องรองรับ Dataset Version
11. ต้องสามารถ Trace Source ได้
12. Seed Data ต้องระบุชัดว่าเป็น Mock / Development Data
13. Major ห้ามเป็น Hard Filter ของ Career Matching
14. Portfolio URL ห้ามถูกตีความเป็น Skill Evidence โดยอัตโนมัติ
15. หาก Portfolio เข้าถึงไม่ได้ ห้ามสรุปว่า User ไม่มี Skill
16. หากไม่พบ Skill ใน Resume/Portfolio ให้ใช้แนวคิด `Evidence Not Found`
17. ห้าม Hard-code จำนวน Career Recommendation หาก Requirement ยังไม่ได้กำหนด
18. ห้าม Hard-code Matching Weight โดยไม่มีการกำหนดใน `AI_MATCHING_SPEC.md`
19. Dataset Processing ต้องสามารถทำซ้ำได้
20. ระบบต้องเก็บข้อมูลเท่าที่จำเป็นและคำนึงถึง Privacy

---

# 59. Dataset–AI Boundary

Dataset Specification กำหนด:

```text
What Data
Where Data Comes From
How Data Is Stored
How Data Is Cleaned
How Data Is Normalized
```

แต่ไม่ได้ล็อก:

```text
Exact AI Model
Exact Embedding Model
Exact Similarity Algorithm
Exact Matching Weight
Exact Threshold
Exact Ranking Formula
```

รายละเอียดเหล่านี้ต้องกำหนดใน:

```text
AI_MATCHING_SPEC.md
```

---

# 60. Final Dataset Architecture

ระบบ Dataset ทั้งหมดมีโครงสร้าง:

```text
                    ┌─────────────────────┐
                    │ Standard Occupation │
                    │ Sources             │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Occupation Dataset  │
                    └──────────┬──────────┘
                               │
                               │
┌──────────────────┐           │
│ Job Posting      │           │
│ Sources          │           │
└────────┬─────────┘           │
         │                     │
         ▼                     ▼
┌────────────────────────────────────┐
│         Raw Labour Dataset         │
└──────────────────┬─────────────────┘
                   │
                   ▼
            Data Cleaning
                   │
                   ▼
          Skill Extraction
                   │
                   ▼
        Skill Normalization
                   │
          ┌────────┴────────┐
          ▼                 ▼
      SKILL DATA       OCCUPATION DATA
          │                 │
          └────────┬────────┘
                   ▼
          Occupation–Skill
              Profile
                   │
                   ▼
           Labour Market
              Demand
                   │
                   ▼
          Career Matching
```

ส่วน Candidate:

```text
Resume
   +
Portfolio
   ↓
Evidence Extraction
   ↓
Skill Normalization
   ↓
Candidate Skill Profile
   ↓
Career Matching
```

---

# 61. Final Research Principle

Dataset ของระบบต้องทำหน้าที่เป็นสะพานระหว่าง:

```text
Student Skills
        ↕
Skill Taxonomy
        ↕
Occupation
        ↕
Labour Market
```

ดังนั้นระบบไม่ได้พิจารณาเพียงว่า:

```text
นักศึกษาเรียนสาขาอะไร?
```

แต่พิจารณาว่า:

```text
นักศึกษามีหลักฐานของทักษะอะไร?
        +
ทักษะเหล่านั้นสัมพันธ์กับอาชีพใด?
        +
ตลาดแรงงานต้องการทักษะเหล่านั้นมากน้อยเพียงใด?
        ↓
Career Compatibility
        ↓
Skill Gap
        ↓
Development Guidance
```

---

# 62. Document Status

```text
Dataset Architecture: LOCKED
Data Categories: LOCKED
Evidence-Based Principle: LOCKED
Labour Market Orientation: LOCKED
Skill Normalization: LOCKED
Occupation Normalization: LOCKED
Dataset Versioning: LOCKED
Traceability: LOCKED
Research Data / Seed Data Separation: LOCKED

Exact Data Sources: TO BE FINALIZED
Collection Period: TO BE FINALIZED
Sampling Method: TO BE FINALIZED
Exact Dataset Size: TO BE DETERMINED
Exact Skill Taxonomy: TO BE FINALIZED
Exact Occupation List: TO BE FINALIZED
Exact Demand Formula: AI_MATCHING_SPEC.md
Exact Matching Algorithm: AI_MATCHING_SPEC.md
```

---

## End of DATASET_SPEC.md