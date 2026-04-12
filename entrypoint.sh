#!/bin/sh

# Ensures the script exits if:
# -e any subcommand within it fails
# -u any variable is unset
set -eu


python ingest/ingest_pipeline.py

# gunicorn is the "production" level version of uvicorn.
# It allows _multiple_ concurrent event loops handled by workers
# running on different available CPUs
# But, FastAPI is an ASGI server. Uvicorn speaks ASGI, gunicorn doesn't.
# So, we use gunicorn with Uvicorn workers.
cd backend
exec gunicorn \
    -k uvicorn.workers.UvicornWorker \
    SportsApp:app \
    --bind "${HOST:-0.0.0.0}:${PORT:-8000}" \
    --workers "${WORKERS:-2}" \
    "$@"