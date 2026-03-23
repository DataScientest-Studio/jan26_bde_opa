#!/bin/bash
set -e

if [ ! -f /app/models/model.pkl ]; then
  echo "[init] model.pkl absent — exécution de la pipeline initiale..."
  PYTHONPATH=/app bash /app/run_pipeline.sh
  echo "[init] Pipeline initiale terminée."
fi

exec uvicorn src.api.main:app --host 0.0.0.0 --port 8000
