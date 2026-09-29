// ESLint flat config (ESLint 9) for the Express backend.
// Lint is a Phase 0 acceptance check (ENVIRONMENT_SETUP §46).
import eslint from "@eslint/js";
import { defineConfig } from "eslint/config";
import tseslint from "typescript-eslint";

export default defineConfig(
  // Build output is generated code, never lint it
  { ignores: ["dist/"] },
  // ESLint's recommended rules for JavaScript
  eslint.configs.recommended,
  // TypeScript parser + recommended TypeScript rules
  tseslint.configs.recommended,
);
