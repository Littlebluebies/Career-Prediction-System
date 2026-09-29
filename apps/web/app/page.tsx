import { BackendStatus } from "@/components/ui/backend-status";

// Phase 0 placeholder home page. The real Home page
// (Hero, How It Works, ...) is built in Phase 10 (FOLDER_STRUCTURE §5, UI_UX_SPEC).
export default function Home() {
  return (
    <main className="mx-auto flex min-h-screen max-w-2xl flex-col gap-8 px-6 py-16">
      <header className="flex flex-col gap-2">
        <h1 className="text-2xl font-semibold">
          ระบบทำนายอาชีพสำหรับนักศึกษาคณะเทคโนโลยีสื่อสารมวลชน
        </h1>
        <p className="text-zinc-600">
          Career Prediction and Skill Gap Analysis System
        </p>
        <p className="text-sm text-zinc-500">Phase 0 — Project Setup</p>
      </header>

      <section className="flex flex-col gap-3">
        <h2 className="text-lg font-medium">System status</h2>
        <BackendStatus />
      </section>
    </main>
  );
}
