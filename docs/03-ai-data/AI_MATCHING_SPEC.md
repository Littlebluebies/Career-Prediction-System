# AI_MATCHING_SPEC.md

# Career Prediction and Skill Gap Analysis System

## AI / NLP / Career Matching Specification

**Project:** ระบบทำนายอาชีพสำหรับนักศึกษาคณะเทคโนโลยีสื่อสารมวลชนโดยอิงการวิเคราะห์ทักษะและความต้องการของตลาดแรงงาน

**English:** Career Prediction and Skill Gap Analysis System for Mass Communication Technology Students Based on Skill Evidence and Labour Market Demand

**Document:** AI_MATCHING_SPEC.md

**Status:** Specification / Methodology Draft

---

# 1. Purpose

เอกสารนี้กำหนดแนวทางด้าน AI, NLP, Skill Matching, Career Ranking, Explainability และ Skill Gap Analysis ของระบบ

ระบบมีหน้าที่:

```text id="f1i4q8"
Resume + Portfolio
        ↓
Text / Evidence Analysis
        ↓
Skill Extraction
        ↓
Skill Normalization
        ↓
Candidate Skill Profile
        ↓
Occupation + Skill Profile
        +
Labour Market Demand
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
```

คำว่า **Career Prediction** ในงานนี้หมายถึง:

> การประเมินและจัดอันดับความเหมาะสมของอาชีพจากหลักฐานทักษะ ผลงาน และข้อมูลความต้องการทักษะของตลาดแรงงาน

ไม่ใช่การรับประกันว่าผู้ใช้จะประกอบอาชีพนั้นในอนาคต

---

# 2. AI System Principles

## 2.1 Evidence-Based

ระบบต้องอ้างอิงจาก Evidence ที่ตรวจพบจริง

แหล่ง Evidence:

```text id="25c0sv"
Resume
Portfolio
Project
Technology
Artifact
Experience
Certificate
```

---

## 2.2 Major Is Context

Major มีหน้าที่เป็น Context

ไม่ใช่ Hard Filter

ตัวอย่าง:

```text id="yj5c0u"
Major:
Creative Media Technology

Detected Skills:
React
JavaScript
Figma
UI Design

Possible Careers:
Front-end Developer
UI/UX Designer
Web Developer
```

ระบบไม่ควรตัด UI/UX Designer ออกเพียงเพราะผู้ใช้มาจาก Web Full Stack

---

# 3. No Evidence ≠ No Skill

หลักการสำคัญ:

```text id="u8n42m"
Skill Not Found
        ≠
User Does Not Have Skill
```

ดังนั้นระบบต้องใช้คำว่า:

> Evidence Not Found / ยังไม่พบหลักฐานของ Skill

แทน:

> ผู้ใช้ไม่มี Skill นี้

ตัวอย่าง:

```text id="52o0ct"
TypeScript
→ Evidence Not Found
```

ไม่ควรแสดง:

```text id="7n1vga"
User does not have TypeScript
```

---

# 4. Input Sources

ระบบรับข้อมูลหลัก:

```text id="5hz6ud"
A. Major
B. Resume
C. Portfolio URL
```

---

## 4.1 Major

ใช้เพื่อ:

* Context
* วิเคราะห์ผลตามสาขา
* แสดงผลลัพธ์ที่เกี่ยวข้องกับสาขา
* วิเคราะห์ Cross-Major Recommendation

ไม่ใช้เป็นตัวตัด Occupation โดยอัตโนมัติ

---

## 4.2 Resume

รองรับอย่างน้อย:

```text id="u1g9d4"
PDF
DOC
DOCX
```

ส่วนที่ควรนำมาวิเคราะห์:

* Education
* Experience
* Projects
* Skills
* Certificates
* Activities

---

## 4.3 Portfolio

รองรับ URL เช่น:

```text id="8ryq1e"
Personal Website
GitHub
GitLab
Behance
itch.io
YouTube
Online Portfolio
```

ระบบต้องตรวจสอบ Accessibility ก่อน

---

# 5. Processing Pipeline

```text id="9jv5bz"
INPUT
  ↓
Validation
  ↓
Resume Parser
  +
Portfolio Analyzer
  ↓
Text Cleaning
  ↓
Skill Detection
  ↓
Skill Extraction
  ↓
Skill Normalization
  ↓
Evidence Linking
  ↓
Candidate Skill Profile
  ↓
Occupation Profile Retrieval
  ↓
Labour Market Demand
  ↓
Matching Engine
  ↓
Career Ranking
  ↓
Explanation
  ↓
Skill Gap
  ↓
Development Guidance
```

---

# 6. Input Validation

ก่อนเริ่ม AI Processing:

```text id="7v7r8f"
Validate Major
Validate Resume
Validate File Type
Validate File Size
Validate Portfolio URL
Validate URL Format
Check Accessibility
```

หากข้อมูลไม่ถูกต้อง:

```text id="z1cc4j"
STOP INVALID INPUT
```

และแสดง Error ที่ผู้ใช้เข้าใจได้

---

# 7. Resume Processing

Pipeline:

```text id="v7q6j1"
Resume File
    ↓
Text Extraction
    ↓
Text Cleaning
    ↓
Section Detection
    ↓
Skill Detection
    ↓
Evidence Extraction
```

---

# 8. Resume Section Detection

ระบบควรพยายามจำแนก Section เช่น:

```text id="p6q0sf"
Education
Experience
Projects
Skills
Certificates
Activities
```

ตัวอย่าง:

```text id="f7m6w2"
PROJECTS

Developed a responsive e-commerce website
using React, JavaScript and CSS.
```

สามารถสร้าง Evidence:

```text id="2x0m51"
React
JavaScript
CSS
Web Development
```

---

# 9. Portfolio Processing

Pipeline:

```text id="s5ghq6"
Portfolio URL
    ↓
Accessibility Check
    ↓
Page Retrieval
    ↓
Content Extraction
    ↓
Project Detection
    ↓
Technology Detection
    ↓
Artifact Detection
    ↓
Evidence Generation
```

---

# 10. Portfolio Accessibility Status

ระบบรองรับ:

```text id="w7oc9j"
ACCESSIBLE
INACCESSIBLE
INVALID
BLOCKED
LOGIN_REQUIRED
UNSUPPORTED
ERROR
```

หากเข้าถึงไม่ได้:

```text id="1jtk8q"
Do Not Infer Missing Skills
```

---

# 11. Portfolio Project Model

Portfolio:

```text id="2n8r0v"
Portfolio
  ↓
Project
  ↓
Description
  +
Technology
  +
Artifact
  ↓
Evidence
```

ตัวอย่าง:

```text id="3c4vxn"
Project:
E-Commerce Website

Technology:
React
JavaScript
CSS

Artifact:
Working Website
```

---

# 12. Evidence Model

Evidence เป็นหัวใจของระบบ

โครงสร้าง:

```text id="5p7xcm"
Source
 ↓
Evidence
 ↓
Skill
```

ตัวอย่าง:

```text id="6hxw4z"
GitHub Project
    ↓
"Built REST API using Node.js"
    ↓
Node.js
REST API
```

---

# 13. Evidence Types

ระบบรองรับ Evidence เช่น:

```text id="k1psl6"
RESUME_SKILL
RESUME_PROJECT
RESUME_EXPERIENCE
RESUME_CERTIFICATE
PORTFOLIO_PROJECT
PORTFOLIO_DESCRIPTION
PORTFOLIO_TECHNOLOGY
PORTFOLIO_ARTIFACT
```

---

# 14. Evidence Confidence

Evidence สามารถมี Confidence:

```text id="4tqv72"
High
Medium
Low
```

หรือใช้ค่าตัวเลขภายในระบบ เช่น:

```text id="g0g1c2"
0.0 – 1.0
```

แต่ Threshold ที่ใช้แบ่ง High / Medium / Low ต้องกำหนดจาก Methodology และการทดลองจริง

ไม่ควรกำหนดแบบสุ่ม

---

# 15. Skill Extraction

Pipeline:

```text id="0af8rd"
Raw Text
 ↓
Tokenization / Text Processing
 ↓
Skill Detection
 ↓
Candidate Skill
 ↓
Context Verification
 ↓
Canonical Skill
```

---

# 16. Skill Detection Methods

ระบบสามารถใช้หลายวิธีร่วมกัน:

### Method A — Dictionary / Rule-Based

ใช้:

```text
SKILL
SKILL_ALIAS
```

เพื่อค้นหา Skill ที่ตรงกัน

ข้อดี:

* เข้าใจง่าย
* ควบคุมได้
* เหมาะกับ Prototype
* Explainable

---

### Method B — NLP Entity Recognition

ใช้ NLP เพื่อระบุ Skill จากข้อความ

ตัวอย่าง:

```text
"Experienced in building applications with React and Node.js"
```

ผล:

```text
React
Node.js
```

---

### Method C — Semantic Matching

ใช้ Embedding / Semantic Similarity เพื่อค้นหา Skill ที่มีความหมายใกล้เคียง แม้ข้อความไม่ตรงกับ Alias

ตัวอย่าง:

```text
"building responsive web interfaces"
```

อาจสัมพันธ์กับ:

```text
Web Development
Responsive Web Design
UI Development
```

แต่ต้องมี Threshold และ Validation ที่เหมาะสม

---

# 17. Recommended Hybrid Skill Extraction

ระบบสามารถใช้:

```text id="h4dbs9"
Dictionary / Alias
        +
NLP
        +
Semantic Similarity
        ↓
Candidate Skills
        ↓
Context Validation
        ↓
Final Skills
```

ไม่ควรพึ่ง Semantic Similarity เพียงอย่างเดียว

---

# 18. Skill Normalization

ตัวอย่าง:

```text id="m9zjfr"
React.js
ReactJS
React JS
```

Normalize:

```text id="mb5kh2"
React
```

อีกตัวอย่าง:

```text id="iz7i0p"
JS
Java Script
JavaScript
```

Normalize:

```text id="pyk7mg"
JavaScript
```

---

# 19. Context Validation

การพบ Keyword ไม่ได้แปลว่าเป็น Skill ของผู้ใช้เสมอไป

ตัวอย่าง:

```text id="gq8x8x"
"Interested in learning React"
```

อาจไม่ควรมี Evidence strength เท่ากับ:

```text id="e2g4bs"
"Developed a React application"
```

ดังนั้นระบบควรแยก:

```text
Mention
Experience
Project Evidence
Requirement
Interest
```

---

# 20. Candidate Skill Profile

หลังจาก Resume และ Portfolio ผ่านการวิเคราะห์:

```text id="1z5t9f"
Candidate
    ↓
Skill
    ↓
Evidence
    ↓
Confidence
    ↓
Source
```

ตัวอย่าง:

| Skill     | Source    | Evidence            | Confidence |
| --------- | --------- | ------------------- | ---------- |
| React     | Resume    | Project description | High       |
| React     | Portfolio | GitHub project      | High       |
| Figma     | Portfolio | UI prototype        | High       |
| Photoshop | Resume    | Skill section       | Medium     |

---

# 21. Evidence Aggregation

หาก Skill เดียวกันมาจากหลาย Source:

```text id="oy0o9m"
Resume
 +
Portfolio
 ↓
React
```

Evidence สามารถเพิ่มความแข็งแรงของ Skill Profile

ตัวอย่าง:

```text id="xw6g8j"
React
├── Resume Evidence
└── Portfolio Evidence
```

ระบบควรเก็บ Evidence แยกกัน ไม่ควรลบหลักฐานเดิม

---

# 22. Candidate Skill Profile Fields

ภายในระบบควรมีข้อมูลอย่างน้อย:

```text id="8c4r31"
skill_id
source
confidence
evidence_count
evidence_references
```

---

# 23. Occupation Profile

Occupation Profile มาจาก:

```text id="h4ag83"
Occupation
    ↓
Required / Relevant Skills
    +
Skill Importance
    +
Labour Market Demand
```

ตัวอย่าง:

```text id="h8v8iv"
Front-end Developer

Skills:
HTML
CSS
JavaScript
React
Git
Accessibility
Testing
```

รายการจริงต้องสร้างจาก Dataset

---

# 24. Occupation–Skill Profile

แต่ละ Occupation ต้องมี:

```text id="t7x3ic"
Skill
Importance
Demand
Source
```

เชื่อมกับ:

```text
OCCUPATION_SKILL
```

ตาม `DATABASE.md`

---

# 25. Labour Market Signal

ระบบใช้ Job Posting เพื่อสร้าง Market Signal

Pipeline:

```text id="m4sz6a"
Job Posting
 ↓
Occupation Mapping
 ↓
Skill Extraction
 ↓
Skill Normalization
 ↓
Skill Frequency
 ↓
Occupation Skill Demand
```

---

# 26. Demand Calculation

แนวคิดพื้นฐาน:

```text id="qz5e9d"
Demand(skill, occupation)
=
Number of relevant job postings
containing skill
/
Number of relevant job postings
for occupation
```

สามารถปรับเป็น Weighted Demand ในอนาคตได้

แต่ Weight ต้องมีเหตุผลจาก Methodology

---

# 27. Occupation Similarity

Candidate Skill Profile ต้องถูกเปรียบเทียบกับ Occupation Skill Profile

แนวคิด:

```text id="5k4qpg"
Candidate Skills
       ↓
Compare
       ↓
Occupation Skills
       ↓
Skill Match
```

---

# 28. Skill Match

ตัวอย่าง:

Candidate:

```text id="o3o0pp"
HTML
CSS
JavaScript
React
Git
```

Occupation:

```text id="m6a4p9"
HTML
CSS
JavaScript
React
Git
Testing
Accessibility
```

Matched:

```text id="h5cq4q"
HTML
CSS
JavaScript
React
Git
```

Not Evidenced:

```text id="qq4u8e"
Testing
Accessibility
```

---

# 29. Matching Score Architecture

Conceptual model:

```text id="n2j9bc"
                 Candidate
                    Skills
                      │
                      ▼
             ┌────────────────┐
             │ Skill Matching │
             └───────┬────────┘
                     │
                     ▼
               Skill Match
                     │
                     +
                     │
             Evidence Strength
                     │
                     +
                     │
             Market Relevance
                     │
                     ▼
              Career Score
```

---

# 30. Career Score

Conceptually:

```text id="y0m6re"
Career Score
=
Skill Match
+
Evidence Strength
+
Market Relevance
```

แต่ละ component สามารถถูก Normalize ก่อนรวมคะแนน

ตัวอย่างเชิงแนวคิด:

```text id="b1k2y7"
Skill Match       → How many relevant skills match
Evidence Strength → How strong the evidence is
Market Relevance  → How relevant the skills are in current job postings
```

---

# 31. Weight Configuration

Weight ต้องไม่ Hard-code ใน Source Code

ควรออกแบบเป็น Configuration:

```text id="42e6he"
MATCHING_CONFIG

skill_match_weight
evidence_weight
market_weight
```

แต่ค่าเริ่มต้นต้องถูกกำหนดหลังจาก:

* Literature Review
* Dataset Analysis
* Pilot Experiment
* Validation

---

# 32. Why Weight Must Not Be Arbitrary

ตัวอย่างที่ไม่ควรทำ:

```text id="o9p5ed"
Skill Match = 50%
Evidence = 30%
Market = 20%
```

หากไม่มีเหตุผลสนับสนุน

ควรบันทึก:

```text id="p8j0s0"
Weight
+
Rationale
+
Version
+
Experiment Result
```

---

# 33. Candidate–Occupation Matching

สำหรับแต่ละ Occupation:

```text id="x7w6s3"
Candidate Profile
       +
Occupation Profile
       ↓
Calculate Skill Match
       ↓
Calculate Evidence Strength
       ↓
Calculate Market Relevance
       ↓
Calculate Final Score
```

จากนั้นทำกับ Occupation ทั้งหมดใน Framework

---

# 34. Cross-Major Matching

สำคัญมาก:

```text id="c5m7f9"
Major
  ↓
Context
```

ไม่ใช่:

```text id="7w8q0u"
Major
  ↓
Occupation Filter
```

ตัวอย่าง:

```text id="j5x8ef"
Major:
Game Development

Skills:
HTML
CSS
JavaScript
React

Possible Career:
Front-end Developer
```

Recommendation นี้สามารถเกิดขึ้นได้แม้ Career ไม่ได้อยู่ใน Major โดยตรง

---

# 35. Ranking

หลังจากคำนวณทุก Occupation:

```text id="q7u9bz"
All Occupations
      ↓
Calculate Score
      ↓
Sort by Score
      ↓
Top K
```

K อาจกำหนดเป็น:

```text
Top 3
Top 5
```

ตาม UI/UX และ Research Requirement

ไม่ควร Hard-code ในหลายจุดของระบบ

---

# 36. Recommendation Output

แต่ละ Career Result ควรประกอบด้วย:

```text id="0t0q5p"
Occupation
Score
Rank
Matched Skills
Evidence
Market Demand
Explanation
Skill Gap
```

---

# 37. Explainable Recommendation

ระบบต้องไม่แสดงเพียง:

```text id="k5gk9j"
Front-end Developer
92.4
```

แต่ต้องอธิบาย:

```text id="2h4t6x"
แนะนำอาชีพ Front-end Developer
เนื่องจากพบหลักฐานของ HTML, CSS, JavaScript และ React
จาก Resume และ Portfolio
ซึ่งเป็นทักษะที่พบในข้อมูลตำแหน่งงานที่ใช้วิเคราะห์
```

ข้อความจริงต้องถูกสร้างจากข้อมูลที่ระบบตรวจพบ

---

# 38. Explanation Components

Explanation ควรประกอบด้วย:

### Why Recommended

ทำไม Career นี้จึงติด Recommendation

### Evidence

Evidence มาจากไหน

### Matched Skills

Skill ใดที่ Match

### Market Signal

Skill ใดมีความต้องการใน Job Posting

### Skill Gap

ยังไม่พบ Evidence ของ Skill ใด

---

# 39. Evidence Traceability

ผู้ใช้ควรสามารถเห็น:

```text id="x8c1un"
Career
 ↓
Matched Skill
 ↓
Evidence
 ↓
Source
```

ตัวอย่าง:

```text id="q7t5kg"
React
↓
GitHub Project
↓
E-Commerce Website
```

---

# 40. Skill Gap Analysis

หลังจากได้ Career Result:

```text id="s6c1ad"
Occupation Skills
        -
Candidate Evidenced Skills
        ↓
Skill Gap
```

---

# 41. Skill Gap Categories

ระบบสามารถแบ่ง:

```text id="9f5x0z"
MATCHED
PARTIAL
EVIDENCE_NOT_FOUND
```

### MATCHED

พบ Evidence ที่ตรงกับ Skill

### PARTIAL

พบ Evidence บางส่วนหรือมีความเกี่ยวข้องแต่ไม่เพียงพอ

### EVIDENCE_NOT_FOUND

ยังไม่พบ Evidence

ไม่ควรใช้คำว่า:

```text
MISSING
USER DOES NOT HAVE
```

เป็นข้อสรุปเกี่ยวกับความสามารถจริงของผู้ใช้

---

# 42. Skill Gap Priority

สามารถแบ่ง:

```text id="j6r1o7"
HIGH
MEDIUM
LOW
```

Priority ต้องพิจารณาจากข้อมูล เช่น:

```text id="i0j7c5"
Occupation Importance
+
Labour Market Demand
+
Candidate Evidence
```

ไม่ควรกำหนด Priority จากความคิดเห็นของ Developer เพียงอย่างเดียว

---

# 43. Skill Gap Example

Occupation:

```text id="k8s5k3"
Front-end Developer
```

Candidate:

```text id="n7w0s8"
HTML
CSS
JavaScript
React
```

ระบบอาจแสดง:

```text id="4x7p1m"
Matched:
HTML
CSS
JavaScript
React

Evidence Not Found:
TypeScript
Testing
Accessibility
CI/CD
```

---

# 44. Development Guidance

Skill Gap ต้องนำไปสู่ Action

Pipeline:

```text id="0q1j3z"
Skill Gap
 ↓
What to Learn
 ↓
What to Practice
 ↓
What to Build
 ↓
Portfolio Evidence
```

---

# 45. Guidance Example

Skill:

```text id="5z6v2n"
TypeScript
```

Guidance:

```text id="6m3q9x"
Learn:
TypeScript fundamentals

Practice:
Convert a JavaScript project to TypeScript

Build:
Add TypeScript to a React project

Evidence:
Document the project in portfolio
```

Guidance เป็นแนวทางพัฒนาทักษะ ไม่ใช่การรับประกันการได้งาน

---

# 46. Career Recommendation Flow

```text id="5q5z2d"
Candidate
   ↓
Extract Skills
   ↓
Normalize Skills
   ↓
Collect Evidence
   ↓
Build Candidate Profile
   ↓
Load All Occupations
   ↓
Load Occupation Skills
   ↓
Load Market Demand
   ↓
Calculate Match
   ↓
Rank
   ↓
Top K
   ↓
Explain
   ↓
Skill Gap
   ↓
Guidance
```

---

# 47. Algorithm Pseudocode

Conceptual pseudocode:

```text id="v4q1d0"
INPUT:
    major
    resume
    portfolio_urls

PROCESS:

    validate_input()

    resume_text = parse_resume(resume)

    portfolio_data = analyze_portfolios(portfolio_urls)

    resume_evidence = extract_evidence(resume_text)

    portfolio_evidence = extract_evidence(portfolio_data)

    all_evidence = merge_evidence(
        resume_evidence,
        portfolio_evidence
    )

    skills = normalize_skills(all_evidence)

    candidate_profile = build_candidate_profile(
        skills,
        all_evidence
    )

    occupations = load_all_occupations()

    FOR occupation IN occupations:

        occupation_profile =
            load_occupation_skill_profile(occupation)

        market_signal =
            load_market_demand(occupation)

        skill_match =
            calculate_skill_match(
                candidate_profile,
                occupation_profile
            )

        evidence_strength =
            calculate_evidence_strength(
                candidate_profile,
                occupation_profile
            )

        market_relevance =
            calculate_market_relevance(
                candidate_profile,
                market_signal
            )

        career_score =
            combine_scores(
                skill_match,
                evidence_strength,
                market_relevance
            )

        save_intermediate_result()

    ranked_results =
        rank_occupations(all_results)

    top_results =
        select_top_k(ranked_results)

    FOR result IN top_results:

        explanation =
            generate_explanation(result)

        skill_gap =
            calculate_skill_gap(
                candidate_profile,
                result.occupation
            )

        guidance =
            generate_guidance(skill_gap)

        save_result()

OUTPUT:
    career_recommendations
    skill_gaps
    development_guidance
```

---

# 48. Intermediate Results

ระบบควรเก็บข้อมูลระหว่างการคำนวณเพื่อ Debug และ Research Analysis

ตัวอย่าง:

```text id="9n6v1y"
skill_match
evidence_strength
market_relevance
final_score
```

ไม่จำเป็นต้องแสดงทั้งหมดแก่ผู้ใช้

แต่ควรสามารถตรวจสอบได้โดย Developer / Researcher

---

# 49. Determinism

หาก Input และ Dataset Version เหมือนกัน:

```text id="5h4m7w"
Same Input
+
Same Dataset Version
+
Same Model Version
+
Same Configuration
```

ควรได้ผลลัพธ์เหมือนเดิม หรือมีความแตกต่างที่อธิบายได้

---

# 50. Model Versioning

AI Processing ควรมี Version

ตัวอย่าง:

```text id="5l7v6k"
skill_extraction_version
matching_algorithm_version
dataset_version
configuration_version
```

เพื่อให้ผลลัพธ์สามารถตรวจสอบย้อนหลังได้

---

# 51. Fallback Strategy

หาก AI / NLP component ไม่สามารถทำงานได้:

```text id="q0v1z7"
Semantic Model
      ↓
Failed
      ↓
Dictionary / Alias Matching
      ↓
Continue Processing
```

หากยังไม่สามารถวิเคราะห์ได้:

```text id="l2e8s6"
Return Partial Result
+
Explain Limitation
```

ไม่ควรสร้าง Recommendation แบบสุ่ม

---

# 52. Low Evidence Scenario

หาก Resume และ Portfolio มี Evidence น้อย:

```text id="s7x4k0"
Low Evidence
```

ระบบควร:

* ลดความมั่นใจของ Recommendation
* แสดง Evidence ที่ตรวจพบ
* แจ้งว่า Result มีข้อจำกัด
* แนะนำให้เพิ่มข้อมูล Portfolio / Project

ไม่ควรสร้างความมั่นใจเกินจริง

---

# 53. No Skill Scenario

หากไม่สามารถตรวจพบ Skill:

```text id="g4x8c1"
No Reliable Skill Evidence
```

ระบบควรแสดง:

> ไม่พบหลักฐานทักษะที่เพียงพอสำหรับการวิเคราะห์ในครั้งนี้

และไม่ควรเดาอาชีพจาก Major เพียงอย่างเดียว

---

# 54. No Portfolio Scenario

หากผู้ใช้ไม่มี Portfolio:

```text id="q5f3r8"
Resume
  ↓
Skill Extraction
  ↓
Candidate Profile
```

ระบบยังสามารถทำงานได้

แต่ Evidence Strength อาจแตกต่างจากกรณีที่มี Resume + Portfolio

---

# 55. Multiple Portfolio Scenario

หากมีหลาย URL:

```text id="8j1s4k"
Portfolio 1
Portfolio 2
Portfolio 3
       ↓
Analyze Separately
       ↓
Merge Evidence
       ↓
Deduplicate Skills
```

ห้ามถือว่า Portfolio URL หลายอันหมายถึง Skill เพิ่มขึ้นโดยอัตโนมัติ

---

# 56. Confidence Model

ระบบสามารถเก็บ Confidence ระดับต่าง ๆ:

```text id="q7j8m2"
Extraction Confidence
Evidence Confidence
Matching Confidence
```

แต่ต้องไม่เรียกว่า:

```text
Probability of Getting Job
```

เพราะระบบไม่ได้พยากรณ์โอกาสได้งาน

---

# 57. Similarity Methods

หากใช้ Semantic Similarity สามารถพิจารณา:

```text id="1n4z0s"
Cosine Similarity
```

ระหว่าง:

```text
Candidate Skill Representation
```

กับ:

```text
Occupation Skill Representation
```

ตัวอย่างแนวคิด:

```text id="9q2h6d"
Similarity =
cosine(candidate_embedding,
       occupation_embedding)
```

Model ที่ใช้จริงยังไม่ถูกล็อกในเอกสารนี้

---

# 58. Hybrid Matching

ระบบสามารถใช้:

```text id="4p8f2w"
Exact / Alias Match
        +
Semantic Match
        +
Evidence
        +
Market Demand
```

ตัวอย่าง:

```text id="8n5t1r"
Exact Skill Match
        ↓
Strong Signal

Semantic Similarity
        ↓
Additional Signal

Portfolio Evidence
        ↓
Evidence Strength

Job Posting Demand
        ↓
Market Signal
```

---

# 59. Avoid Double Counting

ต้องระวังการนับ Evidence ซ้ำ

ตัวอย่าง:

```text id="5v2n0a"
Resume:
React

Portfolio:
React

GitHub:
React
```

ไม่ควรตีความว่า:

```text
React = 3 independent skills
```

แต่ควรตีความว่า:

```text
React
+
Multiple Evidence Sources
```

---

# 60. Occupation Ranking Across All Careers

ระบบต้องพิจารณา Candidate Occupation ทั้งหมดที่อยู่ใน Framework

```text id="2g6v9p"
All Occupations
      ↓
Matching
      ↓
Ranking
```

ไม่ควรทำ:

```text id="7k8w2x"
Major
 ↓
Only Related Occupations
```

เพราะจะทำให้เกิด Major Bias

---

# 61. Major-Aware Explanation

Major สามารถนำมาใช้ใน Explanation ได้

ตัวอย่าง:

> แม้ว่าผู้ใช้ศึกษาสาขา Web Full Stack แต่จากหลักฐานทักษะด้าน Figma และ UI Design ระบบพบความสอดคล้องกับงาน UI/UX Designer

Major ถูกใช้เพื่อ Context ไม่ใช่เป็นตัวกำหนดผลลัพธ์

---

# 62. Explainable Cross-Major Result

หาก Recommendation อยู่นอกสาย Major โดยตรง ระบบควรแสดง:

```text id="l8j7m4"
Cross-Major Recommendation
```

พร้อมเหตุผลจาก Skill Evidence

ตัวอย่าง:

> ผลลัพธ์นี้อยู่นอกสายงานหลักของสาขาที่ศึกษา แต่พบหลักฐานทักษะที่เกี่ยวข้องกับอาชีพดังกล่าวจาก Portfolio

---

# 63. Career Result Data

ผลลัพธ์แต่ละรายการควรมี:

```text id="q8w6e2"
occupation_id
score
rank_position
matched_skills
evidence
market_signal
explanation
```

Database หลักเก็บ:

```text
CAREER_RESULT
```

และเชื่อมไปยัง:

```text
SKILL_GAP
```

---

# 64. Result JSON Concept

ระบบ Backend สามารถส่งข้อมูลลักษณะ:

```json
{
  "occupation": {
    "id": 1,
    "name": "Front-end Developer"
  },
  "rank": 1,
  "score": 0.00,
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
      "reference": "Project Website"
    }
  ],
  "market_signal": {
    "skills": [
      "React",
      "JavaScript"
    ]
  },
  "skill_gap": [
    {
      "skill": "TypeScript",
      "status": "EVIDENCE_NOT_FOUND"
    }
  ]
}
```

ค่า `0.00` เป็น Placeholder เท่านั้น

ห้ามนำตัวเลขนี้ไปใช้เป็น Research Result

---

# 65. Score Interpretation

Score เป็น:

> Compatibility / Match Score

ไม่ใช่:

> Employment Probability

ตัวอย่างการแสดงผล:

```text id="5d6m2p"
Career Compatibility
```

หรือ:

```text
Match Score
```

หลีกเลี่ยง:

```text
Probability of Employment
Chance of Getting Hired
```

---

# 66. Score Normalization

หากหลาย Component มี Scale ต่างกัน:

```text id="x6p1k8"
Skill Match
Evidence
Market Demand
```

ต้อง Normalize ให้อยู่ใน Scale ที่สามารถเปรียบเทียบกันได้ก่อนรวมคะแนน

วิธี Normalize ต้องระบุใน Methodology ที่ Final

---

# 67. Thresholds

ระบบอาจมี Threshold เช่น:

```text id="7q5m9r"
Minimum Evidence Threshold
Semantic Similarity Threshold
Skill Match Threshold
```

แต่ค่าจริงต้องได้จาก:

* Literature
* Pilot Testing
* Validation
* Dataset Distribution
* Experiment

ไม่ควรตั้งค่าโดยไม่มีเหตุผล

---

# 68. Evaluation: Skill Extraction

ประเมิน Skill Extraction ด้วย:

```text id="g4y2x9"
Precision
Recall
F1-score
```

แนวคิด:

```text
Precision =
Correct Extracted Skills
/
All Extracted Skills
```

```text
Recall =
Correct Extracted Skills
/
All Expected Skills
```

---

# 69. Evaluation: Career Recommendation

ใช้:

```text id="e7v5q1"
Top-1 Accuracy
Top-3 Accuracy / Hit Rate
Precision@K
```

ต้องมี Ground Truth หรือ Reference Set ที่เหมาะสม

---

# 70. Evaluation: Skill Gap

สามารถประเมิน:

```text id="u4m7d2"
Detected Skill Gap
vs
Reference Skill Gap
```

หากมี Ground Truth เพียงพอ

---

# 71. Evaluation: Explainability

สามารถประเมินเชิง User Study เช่น:

* ผู้ใช้เข้าใจเหตุผลของ Recommendation หรือไม่
* ผู้ใช้สามารถระบุ Matched Skills ได้หรือไม่
* ผู้ใช้เข้าใจ Skill Gap หรือไม่

---

# 72. Evaluation: Usability

ใช้:

```text id="m7n3p8"
System Usability Scale (SUS)
```

SUS ใช้ประเมิน Usability

ไม่ใช่ Accuracy ของ AI

---

# 73. Expert Validation

Expert Validation เป็นอีกส่วนหนึ่งจาก User Satisfaction

### AI / ML Expert

สามารถตรวจสอบ:

* NLP Method
* Matching Logic
* Data Processing
* Evaluation Method

### Domain Expert

สามารถตรวจสอบ:

* Occupation
* Career Family
* Skill Requirement
* Occupation–Skill Relationship

ผู้เชี่ยวชาญเป็น Validator

ไม่ใช่ผู้สร้าง Dataset ทั้งหมดเพียงฝ่ายเดียว

---

# 74. Research Experiment Structure

สามารถทดลองหลาย Configuration:

```text id="0p5f8j"
Configuration A
Configuration B
Configuration C
```

แล้วเปรียบเทียบ:

```text
F1
Top-1
Top-3
Precision@K
SUS
```

เพื่อเลือก Configuration ที่เหมาะสมตามเกณฑ์วิจัย

---

# 75. Ablation / Component Testing

สามารถทดสอบผลของแต่ละ Component:

```text id="0x6q7z"
Skill Match only
Skill + Evidence
Skill + Market
Skill + Evidence + Market
```

เพื่อศึกษาว่าแต่ละ Component มีผลต่อ Recommendation อย่างไร

---

# 76. Important Research Principle

หากผลการทดลองพบว่า Component หนึ่งมีผลน้อย:

ไม่ควรปรับผลลัพธ์เพื่อให้ระบบดูดีขึ้น

ควรรายงานผลตามการทดลองจริง

---

# 77. Data Leakage Prevention

Evaluation Dataset ต้องไม่รั่วเข้า Training / Knowledge Dataset ในลักษณะที่ทำให้ผลประเมินสูงเกินจริง

ตัวอย่าง:

```text id="5w8q1f"
Training / Knowledge Data
        ≠
Evaluation Ground Truth
```

ต้องกำหนด Data Split หรือ Evaluation Protocol อย่างชัดเจน

---

# 78. Temporal Validation

เนื่องจาก Labour Market เปลี่ยนแปลงตามเวลา ควรเก็บ:

```text id="9w1k3v"
date_collected
dataset_version
```

เพื่อให้สามารถระบุช่วงเวลาของ Market Signal ได้

---

# 79. Recommendation Limitations

ระบบต้องสื่อสารข้อจำกัดว่า:

* Job Posting ไม่ใช่ตลาดแรงงานทั้งหมด
* Portfolio อาจเข้าถึงไม่ได้
* Resume อาจมีข้อมูลไม่ครบ
* Skill Extraction อาจผิดพลาด
* Occupation Mapping อาจมีความคลุมเครือ
* Labour Market เปลี่ยนแปลงตามเวลา

---

# 80. What AI Must Not Do

AI ห้าม:

1. รับประกันว่าจะได้งาน
2. อ้างว่า User มี Skill หากไม่มี Evidence
3. อ้างว่า User ไม่มี Skill เพียงเพราะไม่พบในข้อมูล
4. ตัด Career เพราะ Major โดยอัตโนมัติ
5. สร้าง Job Market Demand จากตัวเลขสมมติ
6. สร้าง Skill Importance แบบสุ่ม
7. สร้าง Occupation Ranking จากความคิดเห็นส่วนตัว
8. สร้าง Evidence จาก Portfolio URL เพียงอย่างเดียว
9. แสดง Score เป็น Employment Probability
10. ซ่อนเหตุผลของ Recommendation

---

# 81. Privacy in AI Processing

AI Pipeline ควรประมวลผลเฉพาะข้อมูลที่จำเป็น:

```text id="0z3k1f"
Resume
Portfolio
Evidence
Skills
```

ไม่ควรนำ Personal Data ที่ไม่เกี่ยวข้องไปใช้ใน Matching

---

# 82. AI Pipeline Logging

ควรเก็บ Log ที่ไม่เปิดเผยข้อมูลส่วนบุคคลเกินจำเป็น:

```text id="x3f5p7"
processing_id
dataset_version
model_version
algorithm_version
configuration_version
processing_time
status
```

---

# 83. Error Handling

กรณี:

### Resume Parse Failed

```text
Unable to analyze resume
```

### Portfolio Blocked

```text
Portfolio could not be accessed
```

### No Skill Evidence

```text
Insufficient evidence for reliable analysis
```

### AI Service Failed

```text
AI analysis temporarily unavailable
```

ห้าม fallback เป็น Random Recommendation

---

# 84. Performance Consideration

AI Processing อาจใช้เวลานาน

ระบบควรแยก:

```text id="1f6w9a"
Input Processing
↓
Analysis Job
↓
Result
```

หากระบบใน Prototype ไม่จำเป็นต้องใช้ Queue สามารถประมวลผลแบบ synchronous ได้

แต่ Architecture ควรสามารถเปลี่ยนเป็น asynchronous ได้ในอนาคต

---

# 85. Recommended Internal Modules

โครงสร้างเชิง Logic:

```text id="1k8x0d"
ai/
├── resume_parser
├── portfolio_analyzer
├── skill_extractor
├── skill_normalizer
├── evidence_analyzer
├── candidate_profile
├── occupation_profile
├── market_analyzer
├── matching_engine
├── ranking_engine
├── explanation_engine
├── skill_gap_engine
└── guidance_engine
```

ชื่อไฟล์จริงขึ้นอยู่กับ Technology Stack

---

# 86. Configuration Management

Configuration ควรแยกจาก Business Logic

ตัวอย่าง:

```text id="9f6m2x"
matching:
    skill_weight
    evidence_weight
    market_weight

ranking:
    top_k

similarity:
    threshold

evidence:
    minimum_confidence
```

ค่าเหล่านี้ต้อง Version และบันทึกไว้

---

# 87. End-to-End Example

Input:

```text id="m4n6s9"
Major:
Creative Media Technology – Web Full Stack

Resume:
HTML
CSS
JavaScript
React

Portfolio:
GitHub Web Project
```

---

### Step 1

Extract:

```text id="4z8c0j"
HTML
CSS
JavaScript
React
```

---

### Step 2

Evidence:

```text id="8n2v7d"
React
→ Resume
→ GitHub Project

JavaScript
→ Resume
→ GitHub Project
```

---

### Step 3

Candidate Profile:

```text id="6f5j1k"
HTML
CSS
JavaScript
React
```

---

### Step 4

Compare Occupations:

```text id="4x6z2a"
Front-end Developer
Back-end Developer
Full-stack Developer
UI/UX Designer
Graphic Designer
...
```

---

### Step 5

Calculate:

```text id="9v4c8m"
Skill Match
Evidence Strength
Market Relevance
```

---

### Step 6

Rank:

```text id="2f8m7x"
Top K Careers
```

---

### Step 7

Explain:

```text id="0g6d3p"
พบหลักฐานของ React, JavaScript, CSS และ HTML
จาก Resume และ Portfolio
ซึ่งมีความสัมพันธ์กับทักษะของอาชีพที่แนะนำ
```

---

### Step 8

Skill Gap:

```text id="j8c2v4"
TypeScript
Testing
Accessibility
```

สถานะ:

```text
EVIDENCE_NOT_FOUND
```

---

### Step 9

Guidance:

```text id="x9m5q7"
Learn TypeScript
↓
Practice with React
↓
Build / Convert Project
↓
Add Evidence to Portfolio
```

---

# 88. Complete AI Architecture

```text id="6w2h9k"
                 USER INPUT
                     │
          ┌──────────┴──────────┐
          │                     │
       RESUME              PORTFOLIO
          │                     │
          ▼                     ▼
    Resume Parser       Portfolio Analyzer
          │                     │
          └──────────┬──────────┘
                     ▼
              Evidence Extraction
                     │
                     ▼
                Skill Detection
                     │
                     ▼
              Skill Normalization
                     │
                     ▼
             Candidate Skill Profile
                     │
                     │
        ┌────────────┴─────────────┐
        │                          │
        ▼                          ▼
 Occupation Knowledge        Labour Market
        │                          │
        └────────────┬─────────────┘
                     ▼
              Matching Engine
                     │
                     ▼
               Career Ranking
                     │
                     ▼
              Top K Careers
                     │
          ┌──────────┴──────────┐
          ▼                     ▼
     Explanation            Skill Gap
                                │
                                ▼
                       Development Guidance
```

---

# 89. Definition of Done

AI Matching Module ถือว่าพร้อมเมื่อ:

```text id="w7j4c2"
[ ] Resume can be parsed
[ ] Portfolio can be analyzed
[ ] Skill can be extracted
[ ] Skill aliases can be normalized
[ ] Evidence can be linked to Skill
[ ] Candidate Skill Profile can be created
[ ] Occupation profiles can be loaded
[ ] Labour Market Demand can be loaded
[ ] Occupation matching works
[ ] Cross-Major matching works
[ ] Career ranking works
[ ] Top-K can be configured
[ ] Recommendation explanation is generated
[ ] Skill Gap is generated
[ ] Development Guidance is generated
[ ] No Evidence ≠ No Skill is enforced
[ ] Employment probability is not claimed
[ ] Model / Dataset versions are traceable
[ ] Errors have fallback handling
```

---

# 90. Claude Implementation Rules

เมื่อส่งเอกสารนี้ให้ Claude:

1. อ่าน `PROJECT_SPEC.md` ก่อน
2. อ่าน `DATABASE.md` ก่อน
3. อ่าน `DATASET_SPEC.md` ก่อน
4. ห้ามเปลี่ยน Core Workflow
5. ห้ามใช้ Major เป็น Hard Filter
6. ห้ามสร้าง Employment Probability
7. ใช้ Match / Compatibility Score
8. ห้ามสร้าง Skill Evidence จาก URL เพียงอย่างเดียว
9. ใช้ `Evidence Not Found` แทนการสรุปว่าไม่มี Skill
10. ห้ามสร้าง Labour Market Demand จากข้อมูลสมมติ
11. ห้ามกำหนด Matching Weight แบบไม่มีเหตุผล
12. Weight ต้องแยกเป็น Configuration
13. Top-K ต้อง Configuration
14. Model Version ต้องบันทึก
15. Dataset Version ต้องบันทึก
16. Intermediate Score ควรตรวจสอบได้
17. Recommendation ต้อง Explainable
18. Skill Gap ต้อง Trace กลับไปยัง Occupation Skill
19. Evidence ต้อง Trace กลับไปยัง Resume / Portfolio
20. AI Failure ต้องไม่ทำให้ระบบสุ่มผลลัพธ์
21. Seed Data ต้องแยกจาก Research Data
22. ต้องออกแบบให้ขยายจาก Web Full Stack ไปทั้งคณะได้
23. ห้ามเขียน Logic แบบผูกกับสาขา Web Full Stack
24. ห้ามล็อก Occupation จำนวนตายตัวใน Business Logic
25. ห้ามล็อก Skill จำนวนตายตัวใน Business Logic

---

# 91. Research Traceability

ทุก Recommendation ควรสามารถตรวจสอบได้:

```text id="5p3x7d"
Career Result
    │
    ├── Score
    │     ├── Skill Match
    │     ├── Evidence Strength
    │     └── Market Relevance
    │
    ├── Occupation
    │     └── Occupation–Skill Profile
    │
    ├── Matched Skills
    │     └── Candidate Skill Profile
    │            └── Evidence
    │                   └── Resume / Portfolio
    │
    └── Market Signal
          └── Job Posting Dataset
```

นี่เป็นส่วนสำคัญสำหรับการอธิบายระบบใน Chapter 3 และการตอบคำถามกรรมการว่า:

> “ระบบได้ผลลัพธ์อาชีพนี้มาจากอะไร?”

---

# 92. Final AI Principle

ระบบควรเปลี่ยนจาก:

```text
Resume
 ↓
Guess Career
```

เป็น:

```text
Resume
+
Portfolio
 ↓
Evidence
 ↓
Skills
 ↓
Occupation Requirements
+
Labour Market Demand
 ↓
Compatibility Analysis
 ↓
Explainable Career Recommendation
 ↓
Skill Gap
 ↓
Development Guidance
```

ดังนั้น AI ของระบบมีหน้าที่ **วิเคราะห์และสนับสนุนการตัดสินใจของผู้ใช้** ไม่ใช่ตัดสินอนาคตทางอาชีพแทนผู้ใช้

---

# 93. Document Status

```text id="3y5m8c"
AI Workflow: LOCKED
Evidence-Based Matching: LOCKED
Cross-Major Matching: LOCKED
Explainability: LOCKED
Skill Gap: LOCKED
Development Guidance: LOCKED
No Evidence ≠ No Skill: LOCKED
Match Score ≠ Employment Probability: LOCKED
Traceability: LOCKED

Exact AI Model: TO BE FINALIZED
Exact Embedding Model: TO BE FINALIZED
Exact Matching Formula: TO BE FINALIZED
Exact Weights: TO BE DETERMINED
Exact Thresholds: TO BE DETERMINED
Top-K Value: TO BE FINALIZED
Evaluation Protocol: TO BE FINALIZED
```

---

## End of AI_MATCHING_SPEC.md