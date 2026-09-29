# 0008: Runtime และ Dependency Versions (Phase 0)

- สถานะ: Accepted
- วันที่: 2026-09-22
- ผู้ตัดสิน: เลือกตามคำสั่งให้แก้ก่อนเริ่ม Phase 0 (ยืนยัน Documentation Freeze แล้ว) เจ้าของโครงการเปลี่ยนได้

## บริบท

`ENVIRONMENT_SETUP.md` §7, §9 และ `TECH_STACK.md` §32 กำหนดหลักการ (ใช้ LTS/Stable ที่ยัง Support ณ เวลาพัฒนา, ห้าม Hard-code Version เก่า) แต่ไม่แยก **Runtime Version** (ตัว Node.js / Python เอง) ออกจาก **Dependency Version** (Library แต่ละตัว) อย่างชัดเจน ทำให้ทั้งสองเรื่องถูกปนกันไว้ในที่เดียว (`package.json`/`package-lock.json`) ซึ่งไม่ถูกต้อง เพราะ Lockfile ตรึงเฉพาะ Dependency ไม่ใช่ตัว Runtime

เอกสารสองไฟล์นี้แก้ถ้อยคำให้แยกสองเรื่องนี้แล้ว (ก่อน ADR นี้) ADR นี้บันทึกค่าจริงที่เลือกใช้ในการเริ่ม Phase 0

## การตัดสินใจ

### Runtime Version

| Runtime | เวอร์ชันที่เลือก | ที่ตรึง | เหตุผล |
| --- | --- | --- | --- |
| Node.js | 24.x (Active LTS) | `.nvmrc` (Root, ใช้ร่วมกันทั้ง `apps/web` และ `apps/api`) = `24`; Docker base image `node:24-alpine`; `package.json` ทั้งสอง App มี `"engines": {"node": ">=24.0.0 <25.0.0"}` | ณ วันที่ตัดสิน (2026-09-22) Node 24 เป็น Active LTS (เริ่ม 2025-10-28) จะเข้าสู่ Maintenance LTS ปลายเดือนนี้ (2026-10-20) และได้รับ Support ถึง 2028-04-30 ครอบคลุมทั้ง Semester 1 และ Semester 2 ของโครงการ ยาวกว่า Node 22 (Support ถึง 2027-04-30) |
| Python | 3.13.x | Docker base image `python:3.13-slim` (ตรึงระดับ Minor ตาม `ENVIRONMENT_SETUP.md` §9) | เข้ากันได้กับ FastAPI/Pydantic เวอร์ชันที่เลือกด้านล่าง และมี Library ด้าน NLP/ML ส่วนใหญ่รองรับแล้ว ต่างจาก Python 3.14 ที่เพิ่งออก Library บางตัวอาจยังไม่รองรับเต็มที่ ซึ่งกระทบ Phase 6 (Skill Extraction) ที่ต้องใช้ Library เฉพาะทาง |
| PostgreSQL | 17 | `docker-compose.yml` `image: postgres:17` | ตัดสินไปแล้วใน [0003](0003-database-tooling.md) ไม่เปลี่ยน |

ตรึงที่ระดับ Major (Node) หรือ Minor (Python) ผ่าน Docker Tag ที่ผู้ดูแล Image ต้นทางปรับ Patch ให้อัตโนมัติ (รวม Security Patch) แทนการระบุ Patch แบบเจาะจงที่อาจไม่มี Tag จริงอยู่บน Docker Hub `.nvmrc` และ `engines.node` ใช้ค่าเดียวกันเพื่อไม่ให้ Local Dev กับ Docker เพี้ยนจากกัน

### Dependency Version — npm (`apps/web`, `apps/api`)

Package Manager คือ npm เท่านั้น (ตาม [0001](0001-repository-layout.md)) `package.json` ระบุเป็นช่วง (Caret Range ตามธรรมเนียม npm) ส่วน **`package-lock.json` คือตัวตรึง Version จริงแบบ Exact** ต้อง Commit เข้า Repository เสมอ ห้ามอยู่ใน `.gitignore`

Library หลักที่เลือก ณ วันนี้ (ยืนยันว่ามีอยู่จริงจากการค้นข้อมูล ไม่ได้เดา):

```text
apps/web:  next ^16.3.0, react ^19.0.0, react-dom ^19.0.0
           typescript ^6.0.0, tailwindcss ^3.4.17, postcss ^8.4.49, autoprefixer ^10.4.20
           eslint ^9.0.0, eslint-config-next ^16.3.0

apps/api:  express ^4.21.0, pg ^8.13.0, cors ^2.8.5, helmet ^8.0.0, dotenv ^16.4.5
           typescript ^6.0.0, tsx ^4.19.0, eslint ^9.0.0
```

### Dependency Version — pip (`services/ai`)

ตรึงแบบ Exact ด้วย `==` ทุกบรรทัดใน `requirements.txt` (ทำหน้าที่แทน Lockfile เพราะ Python ไม่มี Lockfile มาตรฐานในโครงการนี้ ไม่ใช้ poetry/pipenv/pip-tools เพื่อไม่เพิ่มเครื่องมือที่ไม่จำเป็น):

```text
fastapi==0.136.3
uvicorn[standard]==0.48.0
pydantic==2.13.5
```

ยืนยันว่ามีอยู่จริงจากการค้นข้อมูล (`fastapi` 0.136.3 เผยแพร่ 2026-05-23, `pydantic` 2.13.5 เผยแพร่ 2026-08-28, `uvicorn` 0.48.0 เผยแพร่ 2026-05-24) เพิ่ม Library อื่นเมื่อถึง Phase ที่ต้องใช้จริง พร้อมตรึง Version ในการเปลี่ยนแปลงเดียวกัน (`ENVIRONMENT_SETUP.md` §11)

## ข้อจำกัดของการติดตั้งจริงใน Session นี้

Sandbox ที่ใช้สร้าง Phase 0 นี้ไม่มีการเชื่อมต่อ Internet (`npm install`/`pip install` ถูกปฏิเสธที่ระดับ Network) และไม่มี Docker จึงไม่สามารถรัน `npm install` เพื่อสร้าง `package-lock.json` จริง, `pip install` เพื่อตรวจ Import จริง, หรือ `docker compose up --build` ได้ในรอบนี้ ผลคือ:

- `package-lock.json` ของทั้งสอง App **ยังไม่ถูกสร้าง** ต้องรัน `npm install` ในเครื่องที่ต่อ Internet ได้ก่อน แล้ว Commit ไฟล์ที่ได้เข้า Repository
- Import จริงของ FastAPI/Uvicorn/Pydantic ยังไม่ได้ทดสอบ ตรวจได้เพียง Syntax ของไฟล์ Python (`python3 -m py_compile`)
- `docker compose up --build` ยังไม่ได้รัน ตรวจได้เพียงว่า `docker-compose.yml` เป็น YAML ที่ถูกต้อง

รายละเอียดการทดสอบที่ทำได้จริงและยังไม่ได้ทำ อยู่ในรายงาน Phase 0

## ภาคผนวก (2026-09-28): devDependencies เพิ่มเติมของ `apps/api`

- ผู้ตัดสิน: เจ้าของโครงการ (เลือกทางเลือก A ระหว่าง Phase 0)

รายการ npm ข้างบนไม่พอให้ TypeScript และ ESLint ทำงานกับ Express ได้จริง จึงเพิ่มเป็น devDependencies (ไม่อยู่ใน Production image):

| Package | เหตุผล |
| --- | --- |
| `@types/node` (^24) | Type ของ Node.js ให้ตรงกับ Runtime 24 |
| `@types/express` (^4.17) | Type ของ Express 4 |
| `@types/pg` | Type ของ node-postgres |
| `@types/cors` | Type ของ cors |
| `typescript-eslint` | Parser และ Rules ให้ ESLint อ่านไฟล์ `.ts` ได้ |
| `@eslint/js` (^9) | Recommended rules ของ ESLint 9 |

`helmet` และ `dotenv` มี Type ในตัว ไม่ต้องเพิ่ม

เวอร์ชันที่ติดตั้งจริงครั้งแรก (ตรึงใน `apps/api/package-lock.json`):

```text
express 4.22.3, pg 8.23.0, cors 2.8.6, helmet 8.3.0, dotenv 16.6.1
typescript 6.0.3, tsx 4.23.15, eslint 9.39.5, @eslint/js 9.39.5, typescript-eslint 8.70.1
@types/node 24.19.0, @types/express 4.17.25, @types/pg 8.23.1, @types/cors 2.8.19
```

ข้อควรระวัง: `typescript-eslint` 8.70.1 รองรับ TypeScript `>=4.8.4 <6.1.0` แต่ `package.json` ระบุ `typescript: ^6.0.3` ซึ่งยอมรับ 6.1 ขึ้นไป ก่อนอัปเดต TypeScript ให้ตรวจ Peer Dependency ของ `typescript-eslint` ก่อน

## ภาคผนวก (2026-09-30): `apps/web` และ Tailwind CSS v4

- ผู้ตัดสิน: เจ้าของโครงการ (เลือกทางเลือก B ระหว่าง Phase 0)

`apps/web` สร้างด้วย `create-next-app@16` ซึ่งตั้งค่า **Tailwind CSS v4** เป็นค่าเริ่มต้น เจ้าของโครงการเลือกใช้ v4 แทน `tailwindcss ^3.4.17` ที่ระบุไว้ข้างบน `CLAUDE.md` §4 ระบุเพียง "Tailwind CSS" จึงไม่เปลี่ยน Locked Stack

| เดิม (ข้างบน) | ใช้จริง | เหตุผล |
| --- | --- | --- |
| `tailwindcss ^3.4.17` | `tailwindcss ^4` | ค่าเริ่มต้นของ Next.js 16 และเป็นรุ่นที่พัฒนาต่อ |
| `postcss ^8.4.49`, `autoprefixer ^10.4.20` | `@tailwindcss/postcss ^4` | v4 ใช้ Plugin นี้แทน และไม่ต้องใช้ autoprefixer (`postcss` ยังถูกติดตั้งเป็น Dependency ย่อย) |
| `tailwind.config.ts` (FOLDER_STRUCTURE §4) | ไม่มีไฟล์นี้ | v4 ตั้งค่าใน CSS (`app/globals.css`: `@import "tailwindcss"`) |

ปรับจาก Template ให้ตรงกับข้างบน: `typescript` `^5` -> `^6.0.0`, `@types/node` `^20` -> `^24`, เพิ่ม `engines.node` `>=24.0.0 <25.0.0`

เวอร์ชันที่ติดตั้งจริงครั้งแรก (ตรึงใน `apps/web/package-lock.json`):

```text
next 16.3.6, react 19.2.8, react-dom 19.2.8
tailwindcss 4.3.3, @tailwindcss/postcss 4.3.3
typescript 6.0.3, @types/node 24.19.0, @types/react 19.3.0, @types/react-dom 19.3.0
eslint 9.39.5, eslint-config-next 16.3.6
```

ข้อสังเกต: npm แจ้งว่า `eslint@9.39.5` deprecated (มี ESLint 10 แล้ว) ทั้ง `apps/api` และ `apps/web` ยังใช้ ESLint 9 ตามข้างบน ถ้าจะอัปเกรดให้ทำพร้อมกันทั้งสอง App และบันทึกใน ADR
