# Career Prediction System

**ระบบทำนายอาชีพสำหรับนักศึกษาคณะเทคโนโลยีสื่อสารมวลชนโดยอิงการวิเคราะห์ทักษะและความต้องการของตลาดแรงงาน**

Career Prediction and Skill Gap Analysis System for Mass Communication Technology Students
Based on Skill Evidence and Labour Market Demand.

ระบบประเมินความเหมาะสมของอาชีพจาก Skills, Resume Evidence, Portfolio Evidence,
Occupation Knowledge และ Labour Market Demand แล้วแสดง Top 3-5 Career Recommendations
พร้อมคำอธิบาย, Skill Gap Analysis และ Development Guidance

> ระบบไม่ได้รับประกันว่าผู้ใช้จะได้งาน (`CLAUDE.md` §2)

## Technology Stack (`CLAUDE.md` §4)

| Layer | Technology |
| --- | --- |
| Frontend | Next.js, React, TypeScript, Tailwind CSS |
| Backend | Node.js, Express.js, TypeScript |
| AI/NLP | Python (FastAPI) |
| Database | PostgreSQL |
| Infrastructure | Docker, Docker Compose |

## Architecture (`CLAUDE.md` §5)

```text
User -> Next.js -> (REST API) -> Express.js -> Service -> Repository -> PostgreSQL
                                  Express.js -> Python AI/NLP Service
```

## Repository Structure

| Path | หน้าที่ |
| --- | --- |
| `apps/web/` | Frontend (Next.js) |
| `apps/api/` | Backend (Express) |
| `services/ai/` | AI/NLP Service (Python) |
| `database/` | Migrations, Seed, Schema documentation |
| `datasets/` | Raw, Processed, Evaluation datasets and Metadata |
| `scripts/` | Automation scripts |
| `tests/` | Integration, E2E tests and synthetic fixtures |
| `docs/` | Source of Truth documentation |

รายละเอียด: `docs/01-architecture/FOLDER_STRUCTURE.md`

## Documentation

เริ่มอ่านที่ `CLAUDE.md` แล้วตามด้วย `docs/` ตามลำดับใน `CLAUDE.md` §3
การตัดสินใจทางเทคนิคบันทึกใน `docs/decisions/`

## Prerequisites (`docs/decisions/0008-runtime-and-dependency-versions.md`)

- Git
- Node.js 24.x (ดู `.nvmrc`) + npm
- Python 3.13.x
- Docker + Docker Compose

## Getting Started

```bash
git clone <repository-url>
cd Career-Prediction-System
cp .env.example .env
# แก้รหัสผ่านใน .env ก่อนใช้งาน ห้าม Commit .env
```

คำสั่งรันระบบจะเพิ่มเมื่อ Phase 0 (Project Setup) ผ่านเกณฑ์

## Development Status

Phase 0 — Project Setup (อยู่ระหว่างพัฒนา) ดูลำดับ Phase ใน `CLAUDE.md` §8
