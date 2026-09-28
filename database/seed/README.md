# database/seed/

ข้อมูลเริ่มต้นของ Database แยกจาก Migration (DATABASE_MIGRATION_PLAN §42)

```text
Migration -> สร้างโครงสร้าง Database
Seed      -> ใส่ข้อมูลเริ่มต้น
```

| โฟลเดอร์ | ใช้สำหรับ | อ้างอิง |
| --- | --- | --- |
| `development/` | **DEMO / TEST DATA** สำหรับ Development, Testing, Demo | DATABASE_MIGRATION_PLAN §43.1 |
| `reference/` | ข้อมูลอ้างอิงที่ผ่านการตรวจสอบแล้ว (Source Collection -> Validation -> Normalization -> Import) | DATABASE_MIGRATION_PLAN §43.2 |

## กติกา

- ข้อมูลใน `development/` ต้องระบุว่าเป็น DEMO / TEST DATA (FOLDER_STRUCTURE §18)
- Seed ห้ามถูกนำเสนอเป็น Labour Market Dataset จริง (FOLDER_STRUCTURE §18)
- Job Posting ไม่ใช่ Static Seed ใช้ Dataset Import Pipeline แทน (DATABASE_MIGRATION_PLAN §43.3)
- **ห้ามใส่ข้อมูลจริงของนักศึกษา** เช่น Resume, Email, Phone Number, Address, Portfolio Credentials (DATABASE_MIGRATION_PLAN §48, `CLAUDE.md` §7)
