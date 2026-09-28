# 0002: เลข Phase และขอบเขต Semester 1

- สถานะ: Accepted
- วันที่: 2026-09-20
- การยืนยัน: เจ้าของโครงการสั่งให้ดำเนินการต่อหลังตรวจว่าไม่ขัดกับชิ้นงาน (2026-09-20)
- ผู้ตัดสิน: เลือกตามคำสั่งให้แก้ความเสี่ยงโดยตรง เจ้าของโครงการเปลี่ยนได้

## บริบท

เอกสารใช้เลข Phase ไม่ตรงกัน 6 แบบ:

| เอกสาร | รูปแบบเดิม |
| --- | --- |
| CLAUDE.md §8 | Phase 0-13 |
| IMPLEMENTATION_PLAN §3 | เขียนว่า 12 Phases (0-12) แต่เนื้อหามี Phase 13 (Deployment) |
| PROJECT_SPEC §57 | Phase 1-14 (เนื้อหาต่างกัน) |
| FOLDER_STRUCTURE §51 | Phase 0-15 (เนื้อหาต่างกัน) |
| TECH_STACK §78 | Phase 1-6 |
| Prompt เริ่มต้น (ไม่อยู่ใน Repository) | Phase 0-3 โดย Phase 3 คือ Vertical Slice |

เป้าหมาย Semester 1 ก็ไม่ตรงกัน `CLAUDE.md` §15 ให้เป้าหมายเป็น Vertical Slice (Major → Session → Resume → Candidate Skill Profile) ส่วน `IMPLEMENTATION_PLAN.md` §75 และ §80 กำหนด MVP ตลอดสายถึง Skill Gap และ Guidance

## การตัดสินใจ

1. เลข Phase ของ `CLAUDE.md` §8 (0-13) เป็นเลขเดียวที่ใช้ทั้งโครงการ
2. `IMPLEMENTATION_PLAN.md` §3 แก้เป็น 14 Phases ตรงกับ `CLAUDE.md`
3. `FOLDER_STRUCTURE.md` §51 แทนที่ด้วยรายการเดียวกัน
4. `PROJECT_SPEC.md` §57 เปลี่ยนคำว่า Phase เป็น Step และ `TECH_STACK.md` §78 เปลี่ยนเป็น Stage พร้อมตารางเทียบกับ Phase จริง เนื้อหาไม่ถูกลบ
5. Vertical Slice เป็น Milestone แรกของ Semester 1 เมื่อผ่านการทดสอบให้ต่อยอดเป็น MVP ตาม `IMPLEMENTATION_PLAN.md` §75 และ §80 เป้าหมายของ Semester 1 ตาม `PROJECT_SPEC.md` §6 คือ Pilot System บน Web Full Stack ที่ทำให้ Core Engine ทำงานได้จริง โดย Core Engine ต้องไม่ผูกกับ Web Full Stack ขอบเขตของ Pilot System คือ MVP ใน `IMPLEMENTATION_PLAN.md` §75 และ §80
6. เมื่ออ้าง Phase ในเอกสารหรือ Prompt ให้ใช้เลขนี้เสมอ

## ผลที่ตามมา

- `CLAUDE.md` §15 เพิ่มประโยคเชื่อม Vertical Slice กับ MVP
- `IMPLEMENTATION_PLAN.md` §75 เพิ่มประโยคลำดับการสร้าง
- Prompt เริ่มต้นที่ใช้ Phase 0-3 คนละความหมาย ต้องแก้ก่อนนำกลับมาใช้
