# apps/web — Next.js Frontend

หน้าที่: UI / Frontend (`CLAUDE.md` §5)
Stack: Next.js 16 (App Router, no `src/`) + React 19 + TypeScript + Tailwind CSS v4
(ADR 0001, ADR 0008)

## กติกา

- Frontend เรียก **Express Backend เท่านั้น** ห้ามเรียก PostgreSQL หรือ Python โดยตรง
  (`CLAUDE.md` §5, ENVIRONMENT_SETUP §64)
- การเรียก API อยู่ใน `lib/api/` เท่านั้น ห้ามกระจาย `fetch()` ใน Component (FOLDER_STRUCTURE §9)
- Base URL มาจาก `NEXT_PUBLIC_API_BASE_URL` ห้าม Hard-code (API.md §3)
- เฉพาะตัวแปร `NEXT_PUBLIC_*` ที่ Browser เห็นได้ (ENVIRONMENT_SETUP §16)

## Environment Variables

| Variable | ตัวอย่าง | หมายเหตุ |
| --- | --- | --- |
| `NEXT_PUBLIC_API_BASE_URL` | `http://localhost:4000/api` | ถูกฝังลงใน JavaScript ตอน **build** |

Local: ใส่ใน `apps/web/.env.local` (ENVIRONMENT_SETUP §17) ห้าม Commit
Docker: ส่งเป็น build argument (ดู `Dockerfile`)

## Scripts

| Command | หน้าที่ |
| --- | --- |
| `npm run dev` | Development server ที่ http://localhost:3000 |
| `npm run typecheck` | ตรวจ type |
| `npm run lint` | ESLint (eslint-config-next) |
| `npm run build` | Production build (`output: "standalone"`) |
| `npm start` | รัน Production build |

## Phase 0

หน้าแรกแสดงสถานะ `GET /health` ของ Backend เพื่อตรวจเส้นทาง Frontend -> Backend
หน้าจริงตาม UI_UX_SPEC สร้างใน Phase 10

## Notes

- `AGENTS.md` / `CLAUDE.md` ในโฟลเดอร์นี้สร้างโดย Next.js (`next dev` สร้างใหม่ถ้าถูกลบ)
  เป็นคำแนะนำของ Next.js ไม่ใช่ Source of Truth ของโครงการ ดู `CLAUDE.md` ที่ Root

## Structure

ดู `docs/01-architecture/FOLDER_STRUCTURE.md` §4-11
