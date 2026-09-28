# services/ai — Python AI/NLP Service

หน้าที่: AI / NLP / Data Processing (`CLAUDE.md` §5)
Framework: FastAPI + Uvicorn + Pydantic (`docs/decisions/0004-ai-service.md`)
Runtime: Python 3.13 (`docs/decisions/0008-runtime-and-dependency-versions.md`)

## กติกา

- **Internal service เท่านั้น** เรียกได้จาก Express Backend ไม่ใช่ Public API
  Frontend ห้ามเรียก Service นี้โดยตรง (API.md §34)
- ห้ามเป็น Main Backend (`CLAUDE.md` §5)
- `/docs`, `/redoc`, `/openapi.json` เปิดเฉพาะเมื่อ `NODE_ENV=development` (ADR 0004 §5)
- `requirements.txt` ตรึงทุกบรรทัดด้วย `==` (ENVIRONMENT_SETUP §11)

## Endpoints

| Method | Path | หน้าที่ | Phase |
| --- | --- | --- | --- |
| GET | `/health` | Health check (Standard Response Format, API.md §6) | 0 |
| POST | `/internal/analyze` | Analysis (API.md §35-37) | ยังไม่สร้าง |

## Environment Variables

| Variable | Default | หน้าที่ |
| --- | --- | --- |
| `NODE_ENV` | `development` | เปิด/ปิด API docs |
| `AI_SERVICE_PORT` | `8000` | Port ที่ Service listen |

## Run (local, Git Bash)

```bash
cd services/ai
py -3.13 -m venv .venv            # ครั้งแรกเท่านั้น
source .venv/Scripts/activate     # CMD/PowerShell: .venv\Scripts\activate
python -m pip install -r requirements.txt
python -m app.main
```

ตรวจ: `curl http://localhost:8000/health`

## Run (Docker)

```bash
docker build -t career-ai-service .
docker run --rm -p 8000:8000 career-ai-service
```

## Structure

ดู `docs/01-architecture/FOLDER_STRUCTURE.md` §14-15
