# 0011: Continuous Integration (CI) ด้วย GitHub Actions

- สถานะ: Accepted
- วันที่: 2026-10-07
- ผู้ตัดสิน: เจ้าของโครงการ (เลือกตามข้อเสนอก่อนเริ่ม Phase 3: บันทึกใน ADR อย่างเดียว, ทำครบ 6 step, merge `feature/ci` ก่อน Phase 3, C-14 ตัดสินตอนเริ่ม Phase 3, ตรวจ Python ด้วย `compileall`)

## บริบท

- `DATABASE_MIGRATION_PLAN.md` §51 ต้องการให้ Developer และ CI/CD สร้าง Schema เดียวกันจาก Migration ชุดเดียวกัน และ §61 วางลำดับ CI ไว้ (Start PostgreSQL -> Migrations -> Seed -> Tests -> Build) พร้อมกติกาว่า **ไม่ควร Merge Code ที่ทำให้ Fresh Database สร้างไม่ได้**
- `ENVIRONMENT_SETUP.md` §46-50 กำหนดการตรวจ: Frontend/Backend ต้องมี TypeScript Check, Lint, Unit Tests, Build ส่วน Python ต้องมี Syntax Check, Unit Tests, Dependency Check, AI Service ต้อง Start และตอบ Health Check ได้ และ Database ต้องตรวจ Migration, Constraint, Seed
- ตอนนี้ทุกการตรวจข้างต้นทำด้วยมือบนเครื่องผู้พัฒนา (Windows) ไม่มีอะไรกันไม่ให้ PR ที่ทำให้ Build หรือ Database พัง ถูก Merge เข้า `develop` / `main`
- Phase 3 จะเพิ่ม Dataset และ Script ใหม่ จึงควรมี CI ก่อนเริ่ม เพื่อให้ทุก PR ของ Phase 3 ถูกตรวจตั้งแต่แรก
- `IMPLEMENTATION_PLAN.md` §72-73 ให้ Deployment เป็น Phase 13 และยังไม่ได้เลือกที่ Deploy
- `FOLDER_STRUCTURE.md` ไม่มีโฟลเดอร์ `.github/`

## การตัดสินใจ

1. **ทำเฉพาะ CI ด้วย GitHub Actions ยังไม่ทำ CD** ไฟล์เดียวที่ `.github/workflows/ci.yml` (โฟลเดอร์ `.github/` เพิ่มตาม ADR นี้ ไม่แก้ `FOLDER_STRUCTURE.md`) CD ทำใน Phase 13 หลังเลือกที่ Deploy และบันทึกเป็น ADR ใหม่
2. **บันทึกงาน CI ไว้ใน ADR นี้เท่านั้น** ไม่เพิ่มหัวข้อใน `IMPLEMENTATION_PLAN.md` เพราะเอกสาร Source of Truth ถูก Freeze ตาม ADR 0007 และ CI เป็นงานที่ใช้กับทุก Phase ไม่ใช่ Phase ใหม่ (ลำดับ Phase ใน `CLAUDE.md` §8 ไม่เปลี่ยน)
3. **เมื่อไหร่ CI รัน:** ทุก Pull Request ที่เข้า `develop` หรือ `main` และทุก Push เข้า `develop` / `main` ไม่ใช้ Path Filter เพราะ Required Check ที่ไม่ได้รันจะค้างสถานะรอ และทำให้ Merge ไม่ได้
4. **Job และสิ่งที่ตรวจ** (ชื่อ Job คือชื่อ Required Check ในข้อ 8)

    | Job | ขั้นตอน | ข้อกำหนดที่รองรับ |
    | --- | --- | --- |
    | `node (api)`, `node (web)` | Node ตาม `.nvmrc` -> `npm ci` -> `npm run lint` -> `npm run typecheck` -> `npm run build` | ENV §46-48, ADR 0008 (lockfile) |
    | `dataset` | Python 3.13 -> `compileall` ของ `services/ai` และ `scripts/dataset` -> `validate.py` -> `import.py` -> `git status --porcelain` ต้องว่าง | ENV §46 (Syntax Check), DATASET_SPEC §32-35, ADR 0010 §14-15 |
    | `database` | `cp .env.example .env` -> `docker compose up -d --wait postgres` -> `bash scripts/database/test.sh` | MIG §51, §61, ENV §50 |
    | `docker` | `docker compose up -d --build --wait` -> เรียก Backend `/health` ซ้ำจนกว่า `data.status` = `ok` -> `docker compose logs` เมื่อ Fail | ENV §48-49, §39-40 |

    รายละเอียดที่ตั้งใจ:
    - `dataset` ใช้ `git status --porcelain` ไม่ใช่ `git diff --exit-code` อย่างเดียว เพราะ `git diff` ไม่เห็นไฟล์ใหม่ที่ยังไม่ถูก Track เช่น Seed ไฟล์ใหม่ที่ `import.py` สร้างแต่ลืม Commit
    - `database` ใช้ `test.sh` ไม่ใช้ `reset.sh` เพราะ `reset.sh` ต้องพิมพ์ยืนยัน และ `test.sh` สร้าง/ลบ `career_system_test` เอง (ADR 0009 §4) ครอบคลุมทั้ง Seed โหมด development และ reference (ADR 0010 §16)
    - `docker` ตรวจค่า `data.status` ใน Body ไม่ใช่แค่ HTTP 200 เพราะ Backend `/health` ตอบ 200 เสมอแม้ Database หรือ AI Service ล่ม (สถานะ `degraded`, Phase 0) และต้องเรียกซ้ำ เพราะ `backend` / `frontend` ไม่มี Healthcheck ใน Compose ทำให้ `--wait` รอแค่ให้ Container เริ่มทำงาน
    - Dependency Check ของ Python (ENV §46) อยู่ใน `docker` เพราะการ Build Image ของ AI Service ติดตั้ง `requirements.txt` ทั้งหมด
5. **ค่าพื้นฐานของ Workflow:** `permissions: contents: read` (สิทธิ์อ่านอย่างเดียว), `concurrency` แยกตาม Branch พร้อม `cancel-in-progress` (Push ใหม่ยกเลิกรอบเก่าที่ยังรันอยู่), Matrix ของ `node` ใช้ `fail-fast: false` (api พังไม่ยกเลิก web เพื่อให้เห็นผลทั้งคู่)
6. **กติกาความปลอดภัย** (Repository และ Log ของ Actions เป็น Public)
    - CI ไม่เรียก API ภายนอก และไม่มี API Key / Secret จริง ใช้ค่าตัวอย่างจาก `.env.example` เท่านั้น (Password `change_me` ใช้กับ Container ชั่วคราวบน Runner)
    - CI ไม่ดาวน์โหลด NLP / Embedding Model ขนาดใหญ่ทุกครั้งที่รัน เมื่อเลือก Model แล้ว (Phase 4-6) ให้ตัดสินวิธีทดสอบ (Mock, Fixture ขนาดเล็ก หรือ Cache) เป็น ADR ใหม่
    - Test Fixture ต้องเป็นข้อมูลสังเคราะห์เท่านั้น (ADR 0005 ข้อ 3)
    - `build_esco_reference.py` ไม่รันใน CI เพราะใช้ไฟล์ ESCO ดิบที่ไม่อยู่ใน Git (ADR 0010 §5) CI ตรวจผลที่ Commit แล้วแทน
7. **สิ่งที่ยังไม่ตรวจ และเพิ่มเมื่อไหร่**

    | ยังไม่ตรวจ | เหตุผล | เพิ่มเมื่อ |
    | --- | --- | --- |
    | Unit Tests ของ `apps/api` | ยังไม่มีโค้ด Business Logic (ADR 0009 §1: ใช้ `node:test`) | Phase ที่เริ่มมีโค้ด Backend ให้ทดสอบ (ไม่เกิน Phase 9) |
    | Unit Tests ของ `apps/web` | ยังไม่มีหน้าจอจริง และยังไม่ได้เลือกเครื่องมือ | Phase 10 (ตัดสินเครื่องมือเป็น ADR) |
    | Unit Tests ของ Python | เครื่องมือตัดสินใน Phase 4 (ADR 0009 §1) | Phase 4 |
    | Job Posting Dataset | ขึ้นกับ C-14 (Raw Job Posting เข้า Git หรือไม่) | ตอนเริ่ม Phase 3 |
    | Model / Embedding | ยังไม่ได้เลือก Model | Phase 4-6 (ADR ใหม่ ตามข้อ 6) |
    | Integration / E2E | ยังไม่มี Flow ครบ | Phase 11 |
8. **Branch Protection:** `develop` และ `main` ต้องผ่าน Required Checks ทั้ง 5 (`node (api)`, `node (web)`, `dataset`, `database`, `docker`) ก่อน Merge ตั้งค่าหลังจาก Workflow รันผ่านอย่างน้อยหนึ่งครั้ง (GitHub จะให้เลือกได้เฉพาะ Check ที่เคยรันแล้ว)
9. **ลำดับการ Merge:** `feature/ci` -> `develop` -> `main` ให้เสร็จและตั้ง Branch Protection ก่อน แล้วจึงแตก Branch ของ Phase 3 จาก `develop` ที่มี CI แล้ว
10. **CI ต้องโตไปพร้อมกับ Phase:** PR ที่เพิ่ม Script, Test หรือ Dataset ใหม่ ต้องเพิ่มการตรวจใน `ci.yml` ใน PR เดียวกัน และระบุในรายงาน Phase (`CLAUDE.md` §11)

## เหตุผล

- ใช้ GitHub Actions เพราะ Repository อยู่บน GitHub อยู่แล้ว ไม่ต้องเพิ่มบริการภายนอก และ Repository แบบ Public ใช้ GitHub-hosted Runner ได้โดยไม่เสียค่าใช้จ่าย
- CI เรียก Script เดิมที่ผู้พัฒนาใช้บนเครื่อง (`npm run ...`, `test.sh`, `validate.py`, `import.py`) ไม่เขียนการตรวจซ้ำในอีกที่ ทำให้ผลบนเครื่องกับบน CI ตรงกัน
- ยังไม่ทำ CD เพราะยังไม่มีที่ Deploy, ยังไม่มี Production Secret / Database (ENV §57) และ `CLAUDE.md` §16 ห้ามทำเกิน Scope

## ความต่างระหว่างเครื่องผู้พัฒนา (Windows) กับ Runner (Ubuntu Linux)

| เรื่อง | Windows (Git Bash) | Runner | ผล |
| --- | --- | --- | --- |
| เรียก Python | `py -3.13` | `python` จาก `actions/setup-python` (3.13) | คำสั่งต่างกัน แต่ Script เดียวกัน |
| Line Ending | `core.autocrlf=true` แปลงเป็น CRLF ตอน Checkout | LF | `.gitattributes` บังคับ LF ให้ `*.sh`, `*.sql`, `*.csv`, Metadata JSON จึงตรงกันทุกไบต์ (ทดสอบแล้วใน Phase 2) |
| Path | `C:\...` / MSYS แปลง Path อัตโนมัติ | `/home/runner/...` | Script ใช้ Path แบบ Relative จาก Root และ `test.sh` เลี่ยงการแปลง Path ของ MSYS อยู่แล้ว |
| Docker | Docker Desktop | Docker Engine + Compose Plugin ที่ติดตั้งมากับ Runner | คำสั่ง `docker compose` เหมือนกัน |

## ผลที่ตามมา

- ไฟล์ใหม่: `.github/workflows/ci.yml` (สร้างทีละ Job ตามข้อ 4: `node` -> `dataset` -> `database` -> `docker`)
- `docs/decisions/README.md`: เพิ่มรายการ 0011 และระบุว่า C-14 มีผลกับ Job `dataset`
- ตั้ง Branch Protection บน GitHub (ข้อ 8) ทำผ่านหน้า Settings ไม่มีไฟล์ใน Repository
- ไม่แก้เอกสาร Source of Truth และไม่เปลี่ยน Stack, Architecture หรือ Scope
