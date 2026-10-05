#!/usr/bin/env bash
# =============================================================
# test.sh — database tests on a throw-away database
# Sources: DATABASE_MIGRATION_PLAN §49 (5 test levels), §53 (separate test DB),
#          DATABASE.md §59 (relationship + cascade tests)
#
# Round 1 — development seed
#   1. DROP + CREATE career_system_test   (Test 1: fresh database)
#   2. migrate.sh, seed.sh on it
#   3. database/schema/tests.sql          (Tests 2-5 + cascade + seed rules)
#   4. seed.sh reference must be refused  (no DEMO + reference mix)
# Round 2 — reference seed (Phase 2, ADR 0010)
#   5. DROP + CREATE career_system_test, migrate.sh
#   6. seed.sh reference twice            (must be idempotent)
#   7. seed.sh development must be refused
#   8. database/schema/tests_reference.sql
# Always: DROP career_system_test         (even on failure)
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

run_sql() {  # run_sql <file> [psql args...]
  local file="$1"; shift
  docker compose exec -T postgres \
    sh -c 'exec psql -X -q -o /dev/null -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$0" "$@"' \
    "$TEST_DB" "$@" < "$file"
}

# expect_refused <mode> <message>: seed.sh <mode> must stop with <message>
expect_refused() {
  local out
  if out="$(DB_NAME="$TEST_DB" bash scripts/database/seed.sh "$1" 2>&1)"; then
    echo "FAIL  seed.sh $1 was allowed (data modes must not be mixed)" >&2
    exit 1
  fi
  case "$out" in
    *"$2"*) echo "PASS  seed.sh $1 refused: $2" ;;
    *) echo "FAIL  seed.sh $1 failed for another reason: $out" >&2; exit 1 ;;
  esac
}

echo "== Round 1 / Test 1: fresh database (development seed) =="
cleanup
psql_admin -c "CREATE DATABASE $TEST_DB;"
DB_NAME="$TEST_DB" bash scripts/database/migrate.sh
DB_NAME="$TEST_DB" bash scripts/database/seed.sh

expected_migrations="$(ls database/migrations/[0-9][0-9][0-9]_*.sql | wc -l | tr -d ' ')"

echo "== Tests 2-5, cascade, seed rules =="
# INFO lines (PASS ...) are always shown; the first FAIL raises an error and stops.
run_sql database/schema/tests.sql -v expected_migrations="$expected_migrations"
expect_refused reference "already holds DEMO / TEST DATA"

echo "== Round 2: fresh database (reference seed) =="
cleanup
psql_admin -c "CREATE DATABASE $TEST_DB;"
DB_NAME="$TEST_DB" bash scripts/database/migrate.sh
DB_NAME="$TEST_DB" bash scripts/database/seed.sh reference
echo "-- second run (idempotent) --"
DB_NAME="$TEST_DB" bash scripts/database/seed.sh reference

expect_refused development "already holds REFERENCE data"

echo "== Reference seed tests =="
run_sql database/schema/tests_reference.sql

echo "ALL DATABASE TESTS PASSED"
