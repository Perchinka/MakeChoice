#!/usr/bin/env bash
set -euo pipefail

# Wait for Postgres to be ready
while ! </dev/tcp/db/5432; do
  echo "Waiting for Postgres…"
  sleep 1
done

# Run Alembic migrations via the module interface
# (make sure your alembic.ini is in /app or adjust -c accordingly)
python -m alembic upgrade head

# Start the FastAPI app
exec uvicorn src.api.app:app \
     --host 0.0.0.0 \
     --port "${PORT:-8000}" \
     $( [ "${ENV:-}" = "development" ] && echo "--reload" )
