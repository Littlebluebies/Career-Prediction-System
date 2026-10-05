#!/usr/bin/env bash
# =============================================================
# reset.sh — recreate the DEVELOPMENT database from scratch
# Source: ENVIRONMENT_SETUP §38, docs/decisions/0003-database-tooling.md §3
#   (development: reset and re-run; never use DROP DATABASE in production)
#
# Steps: DROP DATABASE -> CREATE DATABASE -> migrate.sh -> seed.sh <mode>
#
# Usage:
#   scripts/database/reset.sh              # development seed (DEMO / TEST DATA)
#   scripts/database/reset.sh reference    # reference seed (ESCO pilot dataset)
# =============================================================
set -euo pipefail
cd "$(dirname "$0")/../.."

MODE="${1:-development}"
case "$MODE" in
  development|reference) ;;
  *) echo "Usage: $0 [development|reference]" >&2; exit 1 ;;
esac

DEV_DB="$(docker compose exec -T postgres printenv POSTGRES_DB | tr -d '\r')"

echo "This deletes ALL data in the development database \"$DEV_DB\" and loads the $MODE seed."
read -r -p "Type 'reset' to continue: " answer
if [ "$answer" != "reset" ]; then
  echo "Cancelled."
  exit 1
fi

# Connect to the maintenance database "postgres" to drop/create the dev database
psql_admin() {
  docker compose exec -T postgres \
    sh -c 'export PGOPTIONS="-c client_min_messages=warning"; exec psql -X -q -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d postgres "$@"' psql "$@"
}

# WITH (FORCE) closes open connections, e.g. a running backend
psql_admin -c "DROP DATABASE IF EXISTS \"$DEV_DB\" WITH (FORCE);"
psql_admin -c "CREATE DATABASE \"$DEV_DB\";"

bash scripts/database/migrate.sh
bash scripts/database/seed.sh "$MODE"

echo "Reset complete ($MODE seed)."
