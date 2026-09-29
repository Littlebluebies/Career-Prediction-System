"use client";

import { useEffect, useState } from "react";

import { getBackendHealth } from "@/lib/api/client";
import type { BackendHealth } from "@/types/health";

// Runs in the browser, so it proves the real path
// Browser -> Express (CORS) -> PostgreSQL / Python (ENVIRONMENT_SETUP §65).

type State =
  | { kind: "loading" }
  | { kind: "loaded"; health: BackendHealth }
  | { kind: "failed"; message: string };

const ROWS: { key: keyof BackendHealth; label: string }[] = [
  { key: "status", label: "Overall" },
  { key: "backend", label: "Backend (Express)" },
  { key: "database", label: "Database (PostgreSQL)" },
  { key: "ai_service", label: "AI Service (Python)" },
];

export function BackendStatus() {
  const [state, setState] = useState<State>({ kind: "loading" });

  useEffect(() => {
    getBackendHealth()
      .then((health) => setState({ kind: "loaded", health }))
      .catch((error: unknown) =>
        setState({
          kind: "failed",
          message: error instanceof Error ? error.message : "Unknown error",
        }),
      );
  }, []);

  if (state.kind === "loading") {
    return <p className="text-zinc-500">Checking backend…</p>;
  }

  if (state.kind === "failed") {
    return (
      <p className="text-red-600">
        Cannot reach backend: {state.message}
      </p>
    );
  }

  return (
    <ul className="divide-y divide-zinc-200 rounded border border-zinc-200">
      {ROWS.map(({ key, label }) => {
        const value = state.health[key];
        const good = value === "ok";
        return (
          <li key={key} className="flex justify-between px-4 py-2">
            <span>{label}</span>
            <span className={good ? "text-green-700" : "text-red-600"}>
              {value}
            </span>
          </li>
        );
      })}
    </ul>
  );
}
