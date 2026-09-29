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
# แก้รหัสผ่านใน .env ก่อนใช้งาน (POSTGRES_PASSWORD และใน DATABASE_URL ให้ตรงกัน) ห้าม Commit .env
```

### Docker (ทุก Service)

```bash
docker compose up --build
```

| Service | URL |
| --- | --- |
| Frontend | http://localhost:3000 |
| Backend health | http://localhost:4000/health |
| AI Service health | http://127.0.0.1:8000/health (เครื่องนี้เท่านั้น) |
| PostgreSQL | 127.0.0.1:5432 (เครื่องนี้เท่านั้น) |

ปิด: `docker compose down` / รีเซ็ต Database: `docker compose down -v`

### Local Development

ดูวิธีรันแต่ละ Service ใน `apps/web/README.md`, `apps/api/README.md`, `services/ai/README.md`
และ `docs/01-architecture/ENVIRONMENT_SETUP.md` §67

## Development Status

- Phase 0 — Project Setup: ทุก Service Start ได้และติดต่อกันได้ใน Docker Compose (รอ Review)
- ลำดับ Phase ทั้งหมดดูใน `CLAUDE.md` §8
