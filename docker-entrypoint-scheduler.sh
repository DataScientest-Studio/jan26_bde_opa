#!/bin/bash
set -e

export PYTHONPATH=/app

echo "Starting cron scheduler..."

mkdir -p /app/logs

echo "[$(date -u '+%Y-%m-%d %H:%M:%S UTC')] Bootstrap ingestion..." >> /app/logs/bootstrap.log
python3 /app/scripts/update_latest.py >> /app/logs/bootstrap.log 2>&1 || true

echo "[$(date -u '+%Y-%m-%d %H:%M:%S UTC')] Bootstrap ETL..." >> /app/logs/bootstrap.log
python3 /app/scripts/run_etl.py >> /app/logs/bootstrap.log 2>&1 || true

echo "[$(date -u '+%Y-%m-%d %H:%M:%S UTC')] Installing crontab..." >> /app/logs/bootstrap.log
crontab /app/crontab.docker

echo "[$(date -u '+%Y-%m-%d %H:%M:%S UTC')] Cron started" >> /app/logs/bootstrap.log
exec cron -f