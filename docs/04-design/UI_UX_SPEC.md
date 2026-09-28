# UI_UX_SPEC.md

# Career Prediction and Skill Gap Analysis System

## UI / UX Specification

**Project:** ระบบทำนายอาชีพสำหรับนักศึกษาคณะเทคโนโลยีสื่อสารมวลชนโดยอิงการวิเคราะห์ทักษะและความต้องการของตลาดแรงงาน

**English:** Career Prediction and Skill Gap Analysis System for Mass Communication Technology Students Based on Skill Evidence and Labour Market Demand

**Document:** UI_UX_SPEC.md

**Status:** Specification / Prototype Design

---

# 1. Purpose

เอกสารนี้กำหนดโครงสร้างหน้าจอ User Interface และ User Experience ของระบบ ตั้งแต่ผู้ใช้เริ่มต้นจนถึงได้รับผลการวิเคราะห์และส่งแบบประเมินความพึงพอใจ

UI ต้องสอดคล้องกับ Workflow:

```text
User
 ↓
Select Major
 ↓
Upload Resume
 ↓
Submit Portfolio
 ↓
Privacy Consent
 ↓
Start Analysis
 ↓
Processing
 ↓
Candidate Skill Profile
 ↓
Career Recommendations
 ↓
Career Explanation
 ↓
Skill Gap
 ↓
Development Guidance
 ↓
SUS / Satisfaction
 ↓
End
```

---

# 2. UX Principles

ระบบต้องยึดหลัก:

1. Simple
2. Clear
3. Explainable
4. Evidence-Based
5. Privacy-Aware
6. Mobile Responsive
7. Accessible
8. Non-Deceptive

ผู้ใช้ต้องเข้าใจว่า Recommendation เป็นผลจากการวิเคราะห์ข้อมูล ไม่ใช่การรับประกันอาชีพในอนาคต

---

# 3. No Login

ระบบไม่มี User Account สำหรับผู้ใช้ทั่วไป

Flow:

```text
Open System
 ↓
Input Data
 ↓
Analysis
 ↓
Result
 ↓
Feedback
 ↓
End
```

ไม่ต้องมี:

```text
Login
Register
Password
Forgot Password
Profile Management
```

---

# 4. Overall Information Architecture

```text
HOME
 │
 ├── START ANALYSIS
 │       │
 │       ├── Major
 │       ├── Resume
 │       ├── Portfolio
 │       ├── Privacy Consent
 │       └── Start
 │
 ├── PROCESSING
 │
 ├── RESULT
 │       │
 │       ├── Career Recommendations
 │       ├── Career Explanation
 │       ├── Skill Evidence
 │       ├── Skill Gap
 │       └── Development Guidance
 │
 └── FEEDBACK
         │
         └── SUS / Satisfaction
```

---

# 5. Main Pages

ระบบประกอบด้วยหน้าหลัก:

```text
01 Home
02 Analysis Input
03 Resume Upload
04 Portfolio Input
05 Privacy Consent
06 Processing
07 Analysis Overview
08 Career Results
09 Career Detail
10 Skill Gap
11 Development Guidance
12 Feedback / SUS
13 Completion
```

สามารถรวมบางหน้าเข้าด้วยกันได้ตาม UI Implementation

---

# 6. Page 01 — Home

## Purpose

อธิบายระบบก่อนเริ่มใช้งาน

---

## Content

### Hero

หัวข้อ:

> Career Prediction & Skill Gap Analysis

คำอธิบาย:

> วิเคราะห์ทักษะจาก Resume และ Portfolio เพื่อค้นหาอาชีพที่สอดคล้องกับทักษะและความต้องการของตลาดแรงงาน

CTA:

> เริ่มวิเคราะห์อาชีพ

---

## Supporting Information

แสดง 3 จุดเด่น:

```text
01
Skill Analysis

02
Career Matching

03
Skill Gap
```

---

## Important Disclaimer

ควรมีข้อความสั้น:

> ผลการวิเคราะห์เป็นข้อมูลประกอบการวางแผนพัฒนาทักษะและอาชีพ ไม่ใช่การรับประกันการได้งานหรือเส้นทางอาชีพในอนาคต

---

# 7. Page 02 — Analysis Input

หน้าสำหรับรวบรวมข้อมูลก่อนเริ่ม Analysis

---

## Progress Indicator

```text
01 Profile
02 Resume
03 Portfolio
04 Consent
05 Analysis
```

สถานะปัจจุบันควร Highlight Step ปัจจุบัน

---

# 8. Major Selection

หัวข้อ:

> คุณกำลังศึกษาอยู่สาขาใด?

Dropdown หรือ Card Selection:

```text
เทคโนโลยีการผลิตภาพยนตร์และวิทยุโทรทัศน์

เทคโนโลยีการโฆษณาและประชาสัมพันธ์

เทคโนโลยีการพิมพ์ดิจิทัลและบรรจุภัณฑ์

ครีเอทีฟมีเดียเทคโนโลยี
```

ถ้าเลือก Creative Media Technology:

```text
Web Full Stack
Game Development
```

---

## UX Rule

ข้อความกำกับ:

> สาขาวิชาจะใช้เป็นข้อมูลประกอบการวิเคราะห์เท่านั้น ระบบยังสามารถแนะนำอาชีพที่อยู่นอกสาขาได้หากพบว่าทักษะมีความสอดคล้อง

---

# 9. Page 03 — Resume Upload

## Header

> Upload Your Resume

คำอธิบาย:

> อัปโหลด Resume เพื่อให้ระบบวิเคราะห์ประสบการณ์ โครงการ และทักษะที่เกี่ยวข้อง

---

## Supported Files

```text
PDF
DOC
DOCX
```

---

## Upload Component

```text
┌──────────────────────────────┐
│                              │
│        Upload Resume         │
│                              │
│   Drag & Drop or Browse      │
│                              │
│      PDF / DOC / DOCX        │
│                              │
└──────────────────────────────┘
```

---

## After Upload

แสดง:

```text
resume.pdf
✓ Ready for analysis
```

พร้อม:

```text
Replace
Remove
```

---

# 10. Resume Validation

ตรวจสอบ:

```text
File Type
File Size
File Readability
Text Extraction
```

Error ตัวอย่าง:

> ไม่สามารถอ่านไฟล์ Resume ได้ กรุณาอัปโหลดไฟล์ใหม่

ไม่ควรเปิดเผย Technical Error ให้ User โดยตรง

---

# 11. Page 04 — Portfolio Input

## Header

> Add Your Portfolio

คำอธิบาย:

> เพิ่มลิงก์ผลงานเพื่อให้ระบบใช้เป็นหลักฐานประกอบการวิเคราะห์ทักษะ

---

## URL Input

```text
┌─────────────────────────────────────┐
│ https://github.com/yourname         │
└─────────────────────────────────────┘

+ เพิ่ม Portfolio อีกลิงก์
```

---

## Platform Examples

แสดงตัวอย่าง:

```text
GitHub
GitLab
Behance
itch.io
YouTube
Personal Website
```

---

# 12. Portfolio Status

หลังตรวจสอบ URL:

```text
✓ Accessible
```

หรือ:

```text
⚠ Login Required
```

หรือ:

```text
✕ Unable to Access
```

---

## UX Rule

หาก Portfolio เข้าถึงไม่ได้:

> ระบบไม่สามารถเข้าถึง Portfolio นี้ได้ และจะไม่นำข้อมูลจากลิงก์ดังกล่าวมาใช้ในการวิเคราะห์

ไม่ควรแสดง:

> คุณไม่มีทักษะจาก Portfolio นี้

---

# 13. Page 05 — Privacy Consent

หน้าสำหรับขอ Consent ก่อนประมวลผล

---

## Header

> Privacy & Data Processing

ข้อความ:

> ระบบจำเป็นต้องประมวลผลข้อมูลจาก Resume และ Portfolio เพื่อวิเคราะห์ทักษะและสร้างคำแนะนำด้านอาชีพ

---

## Information

ควรแจ้ง:

```text
ข้อมูลที่ใช้
Resume
Portfolio
Major

วัตถุประสงค์
Skill Analysis
Career Matching
Skill Gap Analysis

การจัดเก็บ
เก็บข้อมูลเท่าที่จำเป็นตามระยะเวลาที่กำหนด
```

---

## Consent Checkbox

```text
☐ ฉันยินยอมให้ระบบประมวลผลข้อมูลเพื่อวัตถุประสงค์ดังกล่าว
```

ปุ่ม:

> เริ่มวิเคราะห์

Disabled จนกว่าจะ Consent

---

# 14. Page 06 — Processing

หลังจากผู้ใช้เริ่ม Analysis

---

## Processing UI

```text
Analyzing Your Career Profile

✓ Reading Resume
✓ Analyzing Portfolio
● Extracting Skills
○ Matching Careers
○ Analyzing Skill Gap
```

---

## Important UX

ไม่ควรแสดง:

> AI is thinking...

ควรแสดงกระบวนการที่ผู้ใช้เข้าใจได้ เช่น:

```text
กำลังวิเคราะห์ข้อมูล
กำลังตรวจหาทักษะ
กำลังเปรียบเทียบกับอาชีพ
กำลังวิเคราะห์ช่องว่างทักษะ
```

---

# 15. Processing Status

Backend ควรสามารถส่งสถานะ:

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

# 16. Page 07 — Analysis Overview

ก่อนแสดง Career Recommendation สามารถแสดง Summary

หัวข้อ:

> Your Skill Profile

---

## Summary

ตัวอย่าง:

```text
Skills Detected
12

Evidence Sources
8

Portfolio Projects
4
```

ตัวเลขต้องมาจากข้อมูลจริง

---

# 17. Detected Skills

แสดงเป็น Tag / Chip:

```text
HTML
CSS
JavaScript
React
Figma
Git
UI Design
```

---

## Skill Evidence Indicator

ตัวอย่าง:

```text
React
Resume + Portfolio

Figma
Portfolio

Git
Resume
```

ผู้ใช้สามารถกด Skill เพื่อดู Evidence

---

# 18. Evidence Detail

เมื่อกด Skill:

```text
React

Evidence
────────────────────────
Resume
"Developed web applications using React"

Portfolio
"E-commerce Website"

Source
GitHub Project
```

---

# 19. Page 08 — Career Results

นี่คือหน้าหลักของระบบ

---

## Header

> Career Recommendations

คำอธิบาย:

> อาชีพที่มีความสอดคล้องกับทักษะและหลักฐานที่ระบบตรวจพบ

---

# 20. Career Result Cards

แต่ละ Card:

```text
┌──────────────────────────────────┐
│ #1                               │
│ Front-end Developer              │
│                                  │
│ Match Score                      │
│  XX.X                            │
│                                  │
│ Matched Skills                   │
│ HTML  CSS  JavaScript  React     │
│                                  │
│ Evidence                         │
│ Resume + Portfolio               │
│                                  │
│ Why this career?                 │
│ พบหลักฐานทักษะ...               │
│                                  │
│ [ดูรายละเอียด]                  │
└──────────────────────────────────┘
```

---

# 21. Score Display

ใช้คำว่า:

> Match Score

หรือ:

> Career Compatibility

ห้ามใช้:

> Employment Probability

---

## Score Disclaimer

สามารถมี Tooltip:

> คะแนนนี้สะท้อนความสอดคล้องระหว่าง Skill Evidence ของคุณกับข้อมูลทักษะของอาชีพ ไม่ใช่โอกาสในการได้งาน

---

# 22. Top-K

ระบบรองรับ:

```text
Top 3
Top 5
```

ค่า K ต้องมาจาก Configuration

UI ไม่ควรเขียน Logic ว่า:

```text
always show exactly 3
```

---

# 23. Career Result Information

ทุก Recommendation ต้องมี:

```text
Rank
Occupation
Match Score
Matched Skills
Evidence
Market Signal
Explanation
```

---

# 24. Market Signal UI

สามารถแสดง:

> Market Demand

พร้อมข้อความเชิงอธิบาย เช่น:

> ทักษะที่เกี่ยวข้องกับอาชีพนี้ปรากฏใน Job Posting ที่ใช้วิเคราะห์

ไม่ควรแสดงข้อความ:

> อาชีพนี้กำลังเป็นที่ต้องการมากที่สุด

หากไม่มีข้อมูลเพียงพอที่จะสนับสนุนคำกล่าวนั้น

---

# 25. Career Detail Page

เมื่อกด:

> ดูรายละเอียด

แสดง:

```text
Career Overview
Why Recommended
Matched Skills
Evidence
Market Skills
Skill Gap
Development Guidance
```

---

# 26. Career Overview

ตัวอย่าง:

```text
Front-end Developer

Career Family:
Web Development

Description:
พัฒนาโครงสร้างและส่วนติดต่อผู้ใช้ของเว็บไซต์และ Web Application
```

Description ต้องมาจาก Occupation Dataset

---

# 27. Why Recommended

ส่วนสำคัญที่สุดของ Explainability

หัวข้อ:

> ทำไมระบบจึงแนะนำอาชีพนี้?

แสดง:

```text
✓ พบ HTML จาก Resume
✓ พบ CSS จาก Portfolio Project
✓ พบ JavaScript จาก Resume
✓ พบ React จาก GitHub Project
```

---

# 28. Evidence Source UI

แสดง Source:

```text
Resume
Portfolio
Project
Artifact
```

ตัวอย่าง:

```text
React
Portfolio → E-commerce Website
```

---

# 29. Matched Skills

แสดง:

```text
Matched Skills

HTML
CSS
JavaScript
React
Git
```

สามารถแสดงเป็น Chips

---

# 30. Skill Relationship

สามารถแสดง:

```text
Your Skills
        ↓
Occupation Skills
        ↓
Matched
```

ตัวอย่าง:

```text
React       ✓
JavaScript  ✓
Git         ✓
TypeScript  ?
Testing     ?
```

`?` หมายถึง:

> ยังไม่พบหลักฐาน

ไม่ใช่ไม่มี Skill

---

# 31. Skill Gap Page

## Header

> Skill Gap Analysis

คำอธิบาย:

> ทักษะที่ระบบยังไม่พบหลักฐานจากข้อมูลที่คุณส่งเข้ามา และอาจเป็นทักษะที่ควรพิจารณาพัฒนาเพิ่มเติมสำหรับอาชีพนี้

---

# 32. Skill Gap Cards

ตัวอย่าง:

```text
┌──────────────────────────────────┐
│ TypeScript                       │
│ HIGH                             │
│                                  │
│ Evidence Not Found               │
│                                  │
│ Why?                             │
│ เป็นทักษะที่เกี่ยวข้องกับ        │
│ Occupation Profile               │
│                                  │
│ [ดูแนวทางพัฒนา]                 │
└──────────────────────────────────┘
```

---

# 33. Skill Gap Status

ใช้:

```text
Matched
Partial
Evidence Not Found
```

ไม่ใช้:

```text
You Don't Have This Skill
```

---

# 34. Skill Gap Priority

แสดง:

```text
HIGH
MEDIUM
LOW
```

พร้อม Reason

ตัวอย่าง:

> Priority สูงเนื่องจาก Skill นี้มีความเกี่ยวข้องกับ Occupation และพบใน Job Posting ที่ใช้วิเคราะห์

ข้อความต้องสร้างจากข้อมูลจริง

---

# 35. Development Guidance Page

## Header

> Development Guidance

คำอธิบาย:

> แนวทางสำหรับพัฒนาทักษะที่ระบบยังไม่พบหลักฐาน

---

# 36. Guidance Structure

แต่ละ Skill:

```text
Skill
 ↓
Learn
 ↓
Practice
 ↓
Build
 ↓
Portfolio Evidence
```

ตัวอย่าง:

```text
TypeScript

01 Learn
ศึกษาพื้นฐาน TypeScript

02 Practice
นำ TypeScript ไปใช้กับ React

03 Build
สร้าง Web Application

04 Document
เพิ่ม Project ลง Portfolio
```

---

# 37. Guidance Principle

คำแนะนำต้อง:

* Practical
* Actionable
* Skill-focused
* Portfolio-oriented

ไม่ควรรับประกัน:

> เรียน Skill นี้แล้วจะได้งาน

---

# 38. Career Comparison

สามารถมี Section:

> Compare Recommended Careers

ตัวอย่าง:

| Skill | Front-end | UI/UX | Full-stack |
| ----- | --------: | ----: | ---------: |
| HTML  |         ✓ |     ○ |          ✓ |
| React |         ✓ |     ○ |          ✓ |
| Figma |         ○ |     ✓ |          ○ |
| Git   |         ✓ |     ○ |          ✓ |

Legend:

```text
✓ Strong relevance
○ Relevant / supporting
– Not identified
```

หากใช้ Score ต้องอธิบาย Scale ให้ชัดเจน

---

# 39. Cross-Major Indicator

หาก Career ไม่ใช่ Career ที่ตรงกับ Major:

```text
Cross-Major Match
```

คำอธิบาย:

> ระบบพบความสอดคล้องจาก Skill Evidence แม้อาชีพนี้จะอยู่นอกสายสาขาหลักของคุณ

---

# 40. Result Summary

สามารถแสดง:

```text
Your Profile

Major
Creative Media Technology – Web Full Stack

Skills Detected
12

Top Career Matches
5

Skill Gaps
7
```

ตัวเลขต้องมาจาก Backend

---

# 41. Feedback / SUS Page

หลังดูผลลัพธ์:

> ช่วยประเมินการใช้งานระบบ

---

# 42. SUS

ใช้แบบสอบถาม System Usability Scale

ประกอบด้วย 10 ข้อ ตามแบบมาตรฐาน SUS

รูปแบบ:

```text
1 Strongly Disagree
2 Disagree
3 Neutral
4 Agree
5 Strongly Agree
```

ไม่ควรแก้ไขข้อความ SUS โดยพลการหากต้องการใช้เป็น Standard SUS

---

# 43. Additional Satisfaction

สามารถมี:

```text
Overall Satisfaction
1 ───────── 5
```

และ:

```text
ความคิดเห็นเพิ่มเติม
[____________________________]
```

Overall Satisfaction เก็บสเกล 1-5 ใน UI และ Frontend แปลงเป็นคะแนน 0-100 (คูณ 20) ก่อนส่งไป API เพื่อให้ตรงกับ `user_feedback.satisfaction` ใน `DATABASE.md` §28

---

# 44. Feedback Data

Backend ส่ง:

```text
sus_score
satisfaction
comment
```

ไปยัง:

```text
USER_FEEDBACK
```

ตาม `DATABASE.md`

---

# 45. Page 13 — Completion

ข้อความ:

> Analysis Completed

หรือ:

> การวิเคราะห์เสร็จสมบูรณ์

แสดง:

```text
Career Recommendations
Skill Gap
Development Guidance
```

และปุ่ม:

```text
เริ่มการวิเคราะห์ใหม่
```

---

# 46. Start New Analysis

เนื่องจากระบบไม่มี Login:

```text
Start New Analysis
```

ต้องสร้าง Session ใหม่

ไม่ควรนำข้อมูลของ User เดิมมาใช้โดยอัตโนมัติ

---

# 47. Navigation

ระบบสามารถใช้ Navigation แบบ:

```text
Logo
About System
How It Works
Privacy
```

แต่ไม่จำเป็นต้องมี Navigation ที่ซับซ้อน

---

# 48. Analysis Progress

บนหน้าวิเคราะห์ควรแสดง:

```text
Profile
Resume
Portfolio
Consent
Analysis
Result
```

เพื่อให้ผู้ใช้รู้ว่าอยู่ขั้นตอนไหน

---

# 49. Back Navigation

ก่อนเริ่ม Processing:

```text
Back
```

สามารถย้อนกลับไปแก้ข้อมูลได้

หลังเริ่ม Processing:

ไม่ควรแก้ Input ระหว่าง Analysis

---

# 50. Responsive Design

ระบบต้องรองรับ:

```text
Desktop
Tablet
Mobile
```

---

## Desktop

ใช้:

```text
Max-width Container
Two-column Layout
Card Grid
```

---

## Mobile

เปลี่ยนเป็น:

```text
Single Column
Full-width Cards
Stacked Buttons
Scrollable Skill Chips
```

---

# 51. Accessibility

ควรรองรับ:

* Keyboard Navigation
* Visible Focus
* Semantic HTML
* Form Labels
* Error Messages
* Sufficient Contrast
* Alt Text
* Accessible Buttons
* Screen Reader-friendly structure

---

# 52. Color System

สีควรสื่อ:

```text
Primary
Secondary
Success
Warning
Error
Neutral
```

ไม่ควรใช้สีเพียงอย่างเดียวเพื่อสื่อ Status

ตัวอย่าง:

```text
HIGH
⚠ High Priority
```

ไม่ใช่เพียงใช้สีแดงโดยไม่มีข้อความ

---

# 53. Typography

UI ควรใช้ Font ที่:

* อ่านง่าย
* รองรับภาษาไทย
* รองรับภาษาอังกฤษ
* มีน้ำหนักหลายระดับ

ควรกำหนด Typography Token:

```text
H1
H2
H3
Body
Small
Caption
Button
```

Font จริงให้ Finalize ตาม Technology Stack / Visual Design

---

# 54. Component System

ควรสร้าง Reusable Components:

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
Modal
Alert
Toast
LoadingState
EmptyState
```

---

# 55. Button Types

กำหนด:

```text
Primary
Secondary
Tertiary
Danger
```

ตัวอย่าง:

```text
Primary:
เริ่มวิเคราะห์

Secondary:
ย้อนกลับ

Tertiary:
ดูรายละเอียด
```

---

# 56. Form Validation UX

Validation ต้องแสดงใกล้ Field

ตัวอย่าง:

```text
Resume
[ upload ]

⚠ กรุณาอัปโหลด Resume ก่อนดำเนินการต่อ
```

ไม่ควรแสดง Error เพียงด้านบนของหน้า

---

# 57. Empty States

## No Portfolio

```text
ยังไม่ได้เพิ่ม Portfolio

คุณสามารถดำเนินการต่อโดยใช้ Resume
```

---

## No Evidence

```text
ไม่พบหลักฐานทักษะที่เพียงพอ
```

พร้อมคำแนะนำ:

> ลองเพิ่มรายละเอียด Project หรือ Portfolio

---

# 58. Error States

### Resume Error

> ไม่สามารถอ่าน Resume ได้

### Portfolio Error

> ไม่สามารถเข้าถึง Portfolio ได้

### Processing Error

> เกิดปัญหาระหว่างการวิเคราะห์ กรุณาลองใหม่อีกครั้ง

### Server Error

> ระบบไม่สามารถประมวลผลคำขอได้ในขณะนี้

ไม่แสดง Stack Trace

---

# 59. Loading States

ทุก Async Operation ควรมี:

```text
Loading
Progress
Success
Error
```

---

# 60. Result Loading

หาก AI ใช้เวลานาน:

```text
กำลังวิเคราะห์ข้อมูลของคุณ...

1. วิเคราะห์ Resume ✓
2. วิเคราะห์ Portfolio ✓
3. ตรวจหาทักษะ ●
4. จับคู่กับอาชีพ ○
5. วิเคราะห์ Skill Gap ○
```

---

# 61. Explainability UX Principle

ทุก Recommendation ต้องตอบคำถาม:

```text
Why?
What Evidence?
Which Skills?
What Market Signal?
What Should I Improve?
```

---

# 62. Career Result Hierarchy

UI ต้องทำให้ผู้ใช้เห็นข้อมูลตามลำดับ:

```text
1. Career
2. Match Score
3. Why Recommended
4. Matched Skills
5. Evidence
6. Skill Gap
7. Guidance
```

ไม่ควรแสดงรายละเอียด AI ที่ซับซ้อนก่อนคำตอบหลัก

---

# 63. Information Density

ไม่ควรนำข้อมูลทั้งหมดจาก Database มาแสดง

Database:

```text
Many Fields
```

UI:

```text
Important Information
```

ผู้ใช้ควรสามารถกด:

```text
View Details
```

เพื่อดูข้อมูลเพิ่มเติม

---

# 64. Result Trust Design

เพื่อป้องกันการตีความเกินจริง:

แสดง:

> จากข้อมูลที่คุณให้มา

และ:

> ระบบพบหลักฐาน...

แทน:

> คุณเหมาะกับอาชีพนี้แน่นอน

---

# 65. Privacy UX

ผู้ใช้ต้องเห็น:

```text
What is collected
Why it is collected
How it is processed
How long it is retained
```

ก่อน Consent

---

# 66. Data Deletion UX

หากระบบมีปุ่ม:

> ลบข้อมูลการวิเคราะห์

ควรสามารถลบ Temporary User Data ที่เกี่ยวข้องกับ Session ได้

เช่น:

```text
Resume
Portfolio
Evidence
User Skills
Career Results
Skill Gaps
```

ตาม Retention Policy

---

# 67. Session Concept

Session:

```text
Start
 ↓
Input
 ↓
Analysis
 ↓
Result
 ↓
Feedback
 ↓
Expire/Delete
```

ใช้ `USER_SESSION.session_id`

---

# 68. Frontend State

Frontend ควรรักษาสถานะหลัก:

```text
major
resume
portfolio_urls
consent
processing_status
analysis_result
selected_career
feedback
```

ไม่ควรเก็บ Personal Data ใน Local Storage โดยไม่จำเป็น

---

# 69. Backend API Concept

Frontend ควรสื่อสารกับ Backend ผ่าน API / Controller Layer

ตัวอย่าง Endpoint Concept:

```text
POST /api/session
POST /api/resume
POST /api/portfolio
POST /api/analyze
GET  /api/analysis/{session_id}
GET  /api/career/{result_id}
GET  /api/skill-gap/{result_id}
POST /api/feedback
```

ชื่อ Endpoint จริงสามารถเปลี่ยนตาม Technology Stack

---

# 70. API Response Principle

Frontend ไม่ควรคำนวณ Career Score เอง

Backend / AI Layer เป็นผู้คำนวณ:

```text
Backend
 ↓
Career Score
 ↓
Ranking
 ↓
Explanation
 ↓
Skill Gap
```

Frontend มีหน้าที่แสดงผล

---

# 71. Security UX

Frontend ห้ามเปิดเผย:

* API Keys
* Database Credentials
* Internal AI Configuration
* System Prompts
* Private Dataset Credentials

---

# 72. Mobile Career Card

บน Mobile:

```text
┌─────────────────────┐
│ #1                  │
│ Front-end Developer │
│                     │
│ Match 88%           │
│                     │
│ React               │
│ JavaScript          │
│ HTML                │
│                     │
│ [รายละเอียด]        │
└─────────────────────┘
```

---

# 73. Desktop Career Layout

Desktop:

```text
┌────────────────────────────────────────────────────┐
│ Career Recommendations                             │
├────────────────────────────────────────────────────┤
│                                                    │
│ ┌────────────────┐  ┌──────────────────────────┐  │
│ │ #1             │  │ #2                       │  │
│ │ Front-end Dev  │  │ UI/UX Designer            │  │
│ │ Match XX       │  │ Match XX                  │  │
│ └────────────────┘  └──────────────────────────┘  │
│                                                    │
│ ┌────────────────┐  ┌──────────────────────────┐  │
│ │ #3             │  │ #4                       │  │
│ └────────────────┘  └──────────────────────────┘  │
│                                                    │
└────────────────────────────────────────────────────┘
```

---

# 74. Skill Profile Visualization

สามารถใช้:

```text
Skill Chips
Progress Indicators
Evidence Badges
```

หลีกเลี่ยงกราฟที่ซับซ้อนเกินจำเป็น

---

# 75. Optional Skill Radar

Radar Chart สามารถใช้ได้หากต้องการ Visual Summary

เช่น:

```text
Technical
Design
Creative
Communication
Business
```

แต่ไม่ควรนำ Radar Score มาแทน Evidence Detail

---

# 76. Skill Gap Visualization

สามารถใช้:

```text
Matched
Partial
Evidence Not Found
```

ในรูปแบบ:

```text
Matched Skills       8
Partial Skills       3
Evidence Not Found   5
```

---

# 77. User Journey

```text id="0d9c4w"
OPEN
 ↓
Understand System
 ↓
Select Major
 ↓
Upload Resume
 ↓
Add Portfolio
 ↓
Read Privacy
 ↓
Consent
 ↓
Start
 ↓
Wait
 ↓
See Skill Profile
 ↓
See Career Recommendations
 ↓
Explore Career
 ↓
See Skill Gap
 ↓
Read Guidance
 ↓
Give Feedback
 ↓
Finish
```

---

# 78. Primary User Flow

```text id="6j4z5k"
[HOME]
   │
   ▼
[SELECT MAJOR]
   │
   ▼
[UPLOAD RESUME]
   │
   ▼
[ADD PORTFOLIO]
   │
   ▼
[CONSENT]
   │
   ▼
[START ANALYSIS]
   │
   ▼
[PROCESSING]
   │
   ▼
[SKILL PROFILE]
   │
   ▼
[CAREER RESULTS]
   │
   ▼
[CAREER DETAIL]
   │
   ▼
[SKILL GAP]
   │
   ▼
[GUIDANCE]
   │
   ▼
[SUS]
   │
   ▼
[COMPLETE]
```

---

# 79. Alternative Flow — No Portfolio

```text id="4t7c8m"
Major
 ↓
Resume
 ↓
Skip Portfolio
 ↓
Consent
 ↓
Analysis
 ↓
Result
```

ต้องสามารถทำงานได้

---

# 80. Alternative Flow — Portfolio Inaccessible

```text id="7q2z6p"
Portfolio URL
 ↓
Accessibility Check
 ↓
INACCESSIBLE
 ↓
Show Warning
 ↓
Continue with Accessible Data
```

---

# 81. Alternative Flow — Resume Error

```text id="2g6m5x"
Upload
 ↓
Parse Failed
 ↓
Error
 ↓
Replace Resume
 ↓
Retry
```

---

# 82. Alternative Flow — Low Evidence

```text id="9w4p7k"
Analysis
 ↓
Low Evidence
 ↓
Show Limited Result
 ↓
Explain Limitation
 ↓
Suggest Additional Evidence
```

---

# 83. Result Page Wireframe

```text id="7q5j1x"
┌──────────────────────────────────────────────┐
│ Your Career Analysis                         │
│                                              │
│ Major: Creative Media Technology             │
│                                              │
│ Skills Detected                              │
│ [HTML] [CSS] [React] [Figma] [Git]          │
│                                              │
├──────────────────────────────────────────────┤
│ Career Recommendations                       │
│                                              │
│ ┌──────────────────────────────────────────┐ │
│ │ #1 Front-end Developer                   │ │
│ │ Match Score: XX                          │ │
│ │                                          │ │
│ │ ✓ HTML  ✓ CSS  ✓ JavaScript  ✓ React    │ │
│ │                                          │ │
│ │ Why Recommended?                         │ │
│ │ พบหลักฐานจาก Resume + Portfolio          │ │
│ │                                          │ │
│ │ [ดูรายละเอียด]                          │ │
│ └──────────────────────────────────────────┘ │
│                                              │
│ ┌──────────────────────────────────────────┐ │
│ │ #2 UI/UX Designer                       │ │
│ └──────────────────────────────────────────┘ │
│                                              │
└──────────────────────────────────────────────┘
```

---

# 84. Career Detail Wireframe

```text id="w0s8h4"
┌──────────────────────────────────────────────┐
│ ← Career Recommendations                     │
│                                              │
│ Front-end Developer                          │
│ Career Family: Web Development               │
│                                              │
│ Match Score: XX                              │
│                                              │
├──────────────────────────────────────────────┤
│ Why Recommended?                             │
│                                              │
│ ✓ React — Portfolio                          │
│ ✓ JavaScript — Resume                       │
│ ✓ HTML — Portfolio                          │
│                                              │
├──────────────────────────────────────────────┤
│ Market Skills                                │
│ [React] [JavaScript] [HTML] [CSS]            │
│                                              │
├──────────────────────────────────────────────┤
│ Skill Gap                                    │
│                                              │
│ TypeScript             HIGH                   │
│ Testing                MEDIUM                 │
│ Accessibility          MEDIUM                 │
│                                              │
│ [View Development Guidance]                  │
└──────────────────────────────────────────────┘
```

---

# 85. Privacy Wireframe

```text id="t3m7v9"
┌──────────────────────────────────────────────┐
│ Privacy & Data Processing                    │
│                                              │
│ What we use                                  │
│ ✓ Resume                                     │
│ ✓ Portfolio                                  │
│ ✓ Major                                      │
│                                              │
│ Why?                                          │
│ Skill and Career Analysis                    │
│                                              │
│ Data retention                               │
│ Temporary processing according to policy     │
│                                              │
│ ☐ I agree to data processing                 │
│                                              │
│ [Back]                 [Start Analysis]      │
└──────────────────────────────────────────────┘
```

---

# 86. SUS Wireframe

```text id="6n2w7r"
┌──────────────────────────────────────────────┐
│ How was your experience?                     │
│                                              │
│ 1. I would use this system frequently.       │
│                                              │
│ ○ 1  ○ 2  ○ 3  ○ 4  ○ 5                    │
│                                              │
│ 2. I found the system unnecessarily complex. │
│                                              │
│ ○ 1  ○ 2  ○ 3  ○ 4  ○ 5                    │
│                                              │
│ ...                                          │
│                                              │
│ Overall Satisfaction                         │
│ ○ 1  ○ 2  ○ 3  ○ 4  ○ 5                    │
│                                              │
│ [Submit Feedback]                            │
└──────────────────────────────────────────────┘
```

---

# 87. Design Tokens

Frontend ควรแยก Design Tokens:

```text
--color-primary
--color-secondary
--color-success
--color-warning
--color-error
--color-text
--color-muted
--color-background

--space-xs
--space-sm
--space-md
--space-lg
--space-xl

--radius-sm
--radius-md
--radius-lg

--shadow-sm
--shadow-md
```

ค่าจริงต้อง Finalize ใน Visual Design

---

# 88. Component Data Contract

### CareerCard

Input:

```text
rank
occupation
score
matched_skills
evidence_count
explanation
```

### SkillCard

Input:

```text
skill
status
confidence
sources
evidence
```

### SkillGapCard

Input:

```text
skill
priority
status
reason
guidance
```

---

# 89. UI–Backend Mapping

```text id="w5m4q8"
UI Component
      ↓
API Response
      ↓
Database
```

ตัวอย่าง:

```text
CareerCard
    ↓
CAREER_RESULT
    ↓
OCCUPATION
```

Matched Skills:

```text
Career Detail
    ↓
OCCUPATION_SKILL
    +
USER_SKILL
```

Evidence:

```text
Evidence Card
    ↓
SKILL_EVIDENCE
```

Skill Gap:

```text
SkillGapCard
    ↓
SKILL_GAP
```

Feedback:

```text
SUS Form
    ↓
USER_FEEDBACK
```

---

# 90. UI Security Rules

Frontend ห้าม:

```text
Calculate final career score
Access database directly
Expose credentials
Expose private source data
```

Frontend ทำหน้าที่:

```text
Collect Input
Display Processing
Display Result
Collect Feedback
```

---

# 91. UI Performance

ควร:

* Lazy load Career Detail
* Optimize Resume Upload
* Show progress during AI Processing
* Avoid loading all Evidence initially
* Paginate / collapse large Evidence sections

---

# 92. Responsive Breakpoints

ไม่ล็อก Framework แต่ควรรองรับอย่างน้อย:

```text
Mobile
Tablet
Desktop
Large Desktop
```

ค่าจริงให้กำหนดใน Implementation

---

# 93. UI Acceptance Criteria

ระบบ UI ถือว่าผ่านเมื่อ:

```text
[ ] User can start analysis
[ ] User can select Major
[ ] User can upload Resume
[ ] User can add Portfolio
[ ] User can see Portfolio status
[ ] User must consent before analysis
[ ] User can see processing status
[ ] User can see detected skills
[ ] User can see evidence
[ ] User can see Top-K Careers
[ ] User can understand why careers were recommended
[ ] User can inspect matched skills
[ ] User can inspect Skill Gap
[ ] User can read Development Guidance
[ ] User can complete SUS
[ ] User can start a new analysis
[ ] UI works on mobile
[ ] UI handles errors
[ ] UI does not claim employment probability
[ ] UI uses Evidence Not Found correctly
```

---

# 94. UI Non-Goals

UI ไม่ควรมี:

```text
Login Dashboard
User Account
Password
Employment Guarantee
AI Chatbot as Primary Function
Social Network
Job Application System
Recruitment System
```

ระบบมีหน้าที่:

```text
Career Analysis
Skill Evidence
Career Matching
Skill Gap
Development Guidance
```

---

# 95. Final User Experience

ผู้ใช้ควรรู้สึกว่า:

```text
ฉันให้ข้อมูลอะไร?
        ↓
ระบบวิเคราะห์อะไร?
        ↓
พบ Skill อะไร?
        ↓
ทำไมแนะนำ Career นี้?
        ↓
หลักฐานมาจากไหน?
        ↓
ตลาดแรงงานต้องการอะไร?
        ↓
ฉันควรพัฒนา Skill อะไร?
        ↓
ฉันจะนำผลนี้ไปใช้ต่ออย่างไร?
```

---

# 96. Final UI Architecture

```text id="3q6x8a"
                    HOME
                      │
                      ▼
              ANALYSIS INPUT
                      │
         ┌────────────┼────────────┐
         ▼            ▼            ▼
       MAJOR        RESUME      PORTFOLIO
         │            │            │
         └────────────┼────────────┘
                      ▼
                 PRIVACY
                   CONSENT
                      │
                      ▼
                 PROCESSING
                      │
                      ▼
              SKILL PROFILE
                      │
                      ▼
            CAREER RECOMMENDATIONS
                      │
                      ▼
               CAREER DETAIL
                 │         │
                 ▼         ▼
             EVIDENCE    SKILL GAP
                            │
                            ▼
                    DEVELOPMENT
                     GUIDANCE
                            │
                            ▼
                          SUS
                            │
                            ▼
                       COMPLETE
```

---

# 97. Claude Implementation Rules

เมื่อส่งเอกสารนี้ให้ Claude:

1. อ่าน `PROJECT_SPEC.md`
2. อ่าน `DATABASE.md`
3. อ่าน `DATASET_SPEC.md`
4. อ่าน `AI_MATCHING_SPEC.md`
5. ใช้ Workflow เดิม
6. ห้ามเพิ่ม Login โดยไม่ได้รับอนุญาต
7. Major เป็น Context ไม่ใช่ Hard Filter
8. Career Result ต้อง Explainable
9. Match Score ห้ามแสดงเป็น Employment Probability
10. Skill Gap ต้องใช้ `Evidence Not Found`
11. Portfolio ที่เข้าถึงไม่ได้ต้องไม่ถูกตีความว่า User ไม่มี Skill
12. Frontend ห้ามคำนวณ Career Score
13. Frontend ห้ามเข้าถึง Database โดยตรง
14. API เป็นตัวกลางระหว่าง Frontend และ Backend
15. Component ต้อง Reusable
16. UI ต้อง Responsive
17. Form ต้อง Validate
18. Async Processing ต้องมี Loading / Error / Success State
19. Sensitive Data ต้องไม่ถูกเก็บใน Browser โดยไม่จำเป็น
20. Privacy Consent ต้องเกิดก่อนการประมวลผล
21. SUS ต้องใช้โครงสร้างมาตรฐาน
22. ห้ามสร้าง UI ที่รับประกันผลลัพธ์ด้านการจ้างงาน
23. ห้ามสร้างข้อมูล Market Demand ปลอมเพื่อแสดงใน UI
24. ใช้ Real Dataset เมื่อระบบเข้าสู่ Research Phase
25. Seed Data ต้องระบุชัดว่าเป็น Mock Data

---

# 98. Document Status

```text id="1q7z5m"
Main User Flow: LOCKED
No Login: LOCKED
Major Selection: LOCKED
Resume Upload: LOCKED
Portfolio Input: LOCKED
Privacy Consent: LOCKED
Processing Flow: LOCKED
Skill Profile: LOCKED
Career Results: LOCKED
Explainability: LOCKED
Skill Gap: LOCKED
Development Guidance: LOCKED
SUS: LOCKED
Responsive Requirement: LOCKED

Visual Theme: TO BE FINALIZED
Color Palette: TO BE FINALIZED
Typography: TO BE FINALIZED
Frontend Framework: Next.js + React + TypeScript + Tailwind CSS (LOCKED, see TECH_STACK.md §85)
Exact API Routes: TO BE FINALIZED
Exact Component Library: TO BE FINALIZED
```

---

## End of UI_UX_SPEC.md