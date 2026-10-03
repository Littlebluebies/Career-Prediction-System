#!/usr/bin/env bash
# =============================================================
# migrate.sh — apply SQL migrations in order
# Sources: docs/decisions/0003-database-tooling.md §1-4,
#          DATABASE_MIGRATION_PLAN.md §5-§9
#
# Usage (from anywhere, PostgreSQL container must be running):
#   scripts/database/migrate.sh                     # development DB (POSTGRES_DB)
#   DB_NAME=career_system_test scripts/database/migrate.sh
#
# Rules:
#   * each file runs in ONE transaction together with its schema_migrations row
#     -> a file is either fully applied and recorded, or not at all
#   * an applied file whose checksum changed is an error (migrations are immutable, MIG §7)
# =============================================================
set -euo pipefail

# Always run from the repository root (where docker-compose.yml lives)
cd "$(dirname "$0")/../.."

MIGRATIONS_DIR="database/migrations"
DB_NAME="${DB_NAME:-}"

# Run psql INSIDE the postgres container (no psql needed on Windows).
# Credentials come from the container's own environment; local socket = no password.
# TARGET_DB empty -> falls back to POSTGRES_DB.
psql_db() {
  docker compose exec -T -e TARGET_DB="$DB_NAME" postgres \
    sh -c 'export PGOPTIONS="-c client_min_messages=warning"; exec psql -X -q -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "${TARGET_DB:-$POSTGRES_DB}" "$@"' psql "$@"
}

if ! docker compose exec -T postgres pg_isready -q; then
  echo "ERROR: postgres container is not running or not ready. Run: docker compose up -d postgres" >&2
  exit 1
fi

# Migration version tracking (ADR 0003 §2). Lives in "public" because it must
# exist before 001 creates the career_system schema.
psql_db -c "CREATE TABLE IF NOT EXISTS public.schema_migrations (
  version    TEXT PRIMARY KEY,
  checksum   TEXT NOT NULL,
  applied_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);"

applied=0
skipped=0

for file in "$MIGRATIONS_DIR"/[0-9][0-9][0-9]_*.sql; do
  [ -e "$file" ] || { echo "No migration files found in $MIGRATIONS_DIR"; exit 0; }

  version="$(basename "$file" .sql)"
  checksum="$(sha256sum "$file" | cut -d' ' -f1)"
  recorded="$(psql_db -tA -c "SELECT checksum FROM public.schema_migrations WHERE version = '$version';")"

  if [ -n "$recorded" ]; then
    if [ "$recorded" != "$checksum" ]; then
      echo "ERROR: $version was already applied but the file has changed." >&2
      echo "       Applied migrations are immutable. Create a new migration instead (MIG §7)." >&2
      exit 1
    fi
    skipped=$((skipped + 1))
    continue
  fi

  echo "Applying $version ..."
  {
    echo "SET search_path TO career_system, public;"
    cat "$file"
    echo
    echo "INSERT INTO public.schema_migrations (version, checksum) VALUES ('$version', '$checksum');"
  } | psql_db --single-transaction
  applied=$((applied + 1))
done

echo "Done. Applied: $applied, already up to date: $skipped (database: ${DB_NAME:-POSTGRES_DB})"
