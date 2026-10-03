#!/usr/bin/env bash
# =============================================================
# seed.sh — load DEVELOPMENT seed data (DEMO / TEST DATA)
# Sources: DATABASE_MIGRATION_PLAN §42-48, docs/decisions/0003-database-tooling.md §6
#
# Usage (after migrate.sh):
#   scripts/database/seed.sh
#   DB_NAME=career_system_test scripts/database/seed.sh
#
# Safe to run many times: every INSERT uses ON CONFLICT DO NOTHING.
# =============================================================
set -euo pipefail
cd "$(dirname "$0")/../.."

SEED_DIR="database/seed/development"
# Explicit order: parents before children (occupation needs career_family)
SEED_FILES=(major career_family skill occupation)
DB_NAME="${DB_NAME:-}"

psql_db() {
  docker compose exec -T -e TARGET_DB="$DB_NAME" postgres \
    sh -c 'export PGOPTIONS="-c client_min_messages=warning"; exec psql -X -q -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "${TARGET_DB:-$POSTGRES_DB}" "$@"' psql "$@"
}

if ! docker compose exec -T postgres pg_isready -q; then
  echo "ERROR: postgres container is not running or not ready. Run: docker compose up -d postgres" >&2
  exit 1
fi

ready="$(psql_db -tA -c "SELECT to_regclass('career_system.occupation_alias') IS NOT NULL;")"
if [ "$ready" != "t" ]; then
  echo "ERROR: tables not found. Run scripts/database/migrate.sh first." >&2
  exit 1
fi

for name in "${SEED_FILES[@]}"; do
  file="$SEED_DIR/$name.seed.sql"
  echo "Seeding $name ..."
  {
    echo "SET search_path TO career_system, public;"
    cat "$file"
  } | psql_db --single-transaction
done

echo "Done. Development seed loaded (database: ${DB_NAME:-POSTGRES_DB})"
