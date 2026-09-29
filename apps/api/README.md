# apps/api — Express Backend

หน้าที่: API / Business Logic / Orchestration (`CLAUDE.md` §5)
Stack: Node.js 24 + Express 4 + TypeScript + `pg` (ADR 0003, ADR 0008)

## กติกา

- Layered Architecture: Route -> Controller -> Service -> Repository -> Database (`CLAUDE.md` §12)
- SQL อยู่ใน `src/repositories/` เท่านั้น ไม่ใช้ ORM (ADR 0003 §5)
- เรียก Python AI Service ผ่าน `src/clients/python.client.ts` เท่านั้น
- Error response ใช้ Standard Response Format (API.md §6)

## Endpoints

| Method | Path | หน้าที่ | Phase |
| --- | --- | --- | --- |
| GET | `/health` | สถานะ backend / database / ai_service (ENVIRONMENT_SETUP §32, §40) | 0 |
| - | `/api/...` | User Flow API (API.md) | ยังไม่สร้าง |

`/health` ตอบ HTTP 200 เสมอ; `data.status` เป็น `ok` หรือ `degraded`
และไม่แสดงรายละเอียด Error (ENVIRONMENT_SETUP §40)

## Environment Variables

| Variable | Required | Default |
| --- | --- | --- |
| `DATABASE_URL` | yes | - |
| `AI_SERVICE_URL` | yes | - |
| `BACKEND_PORT` | no | `4000` |
| `FRONTEND_PORT` | no | `3000` (ใช้สร้าง CORS origin) |
| `NODE_ENV` | no | `development` |

Local: ค่าอยู่ใน `apps/api/.env` (ENVIRONMENT_SETUP §17) ห้าม Commit
ใช้ `localhost` แทนชื่อ Service เมื่อรันนอก Docker (ENVIRONMENT_SETUP §14)

## Scripts

| Command | หน้าที่ |
| --- | --- |
| `npm run dev` | รันด้วย tsx (reload อัตโนมัติ, ไม่ตรวจ type) |
| `npm run typecheck` | ตรวจ type ด้วย tsc |
| `npm run lint` | ESLint |
| `npm run build` | Compile ไป `dist/` |
| `npm start` | รัน `dist/server.js` |

## Docker

```bash
docker build -t career-api-service .
```

รันร่วมกับ Service อื่นผ่าน `docker-compose.yml` ที่ Root

## Structure

ดู `docs/01-architecture/FOLDER_STRUCTURE.md` §12-13
