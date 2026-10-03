#!/usr/bin/env bash
# =============================================================
# reset.sh — recreate the DEVELOPMENT database from scratch
# Source: ENVIRONMENT_SETUP §38, docs/decisions/0003-database-tooling.md §3
#   (development: reset and re-run; never use DROP DATABASE in production)
#
# Steps: DROP DATABASE -> CREATE DATABASE -> migrate.sh -> seed.sh
# =============================================================
set -euo pipefail
cd "$(dirname "$0")/../.."

DEV_DB="$(docker compose exec -T postgres printenv POSTGRES_DB | tr -d '\r')"

echo "This deletes ALL data in the development database \"$DEV_DB\"."
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
bash scripts/database/seed.sh

echo "Reset complete."
