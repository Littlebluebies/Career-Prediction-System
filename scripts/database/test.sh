#!/usr/bin/env bash
# =============================================================
# test.sh — database tests on a throw-away database
# Sources: DATABASE_MIGRATION_PLAN §49 (5 test levels), §53 (separate test DB),
#          DATABASE.md §59 (relationship + cascade tests)
#
#   1. DROP + CREATE career_system_test   (Test 1: fresh database)
#   2. migrate.sh, seed.sh on it
#   3. database/schema/tests.sql          (Tests 2-5 + cascade + seed rules)
#   4. DROP career_system_test            (always, even on failure)
#
# The development database is never touched.
# =============================================================
set -euo pipefail
cd "$(dirname "$0")/../.."

TEST_DB="career_system_test"

psql_admin() {
  docker compose exec -T postgres \
    sh -c 'export PGOPTIONS="-c client_min_messages=warning"; exec psql -X -q -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d postgres "$@"' psql "$@"
}

cleanup() {
  psql_admin -c "DROP DATABASE IF EXISTS $TEST_DB WITH (FORCE);" || true
}
trap cleanup EXIT

if ! docker compose exec -T postgres pg_isready -q; then
  echo "ERROR: postgres container is not running. Run: docker compose up -d postgres" >&2
  exit 1
fi

echo "== Test 1: fresh database =="
cleanup
psql_admin -c "CREATE DATABASE $TEST_DB;"
DB_NAME="$TEST_DB" bash scripts/database/migrate.sh
DB_NAME="$TEST_DB" bash scripts/database/seed.sh

expected_migrations="$(ls database/migrations/[0-9][0-9][0-9]_*.sql | wc -l | tr -d ' ')"

echo "== Tests 2-5, cascade, seed rules =="
# INFO lines (PASS ...) are always shown; the first FAIL raises an error and stops.
docker compose exec -T postgres \
  sh -c 'exec psql -X -q -o /dev/null -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$0" "$@"' \
  "$TEST_DB" -v expected_migrations="$expected_migrations" \
  < database/schema/tests.sql

echo "ALL DATABASE TESTS PASSED"
