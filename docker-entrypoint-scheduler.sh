#!/bin/bash
set -e

mkdir -p /app/logs
crontab /app/crontab.docker
echo "[scheduler] Crontab installé. Démarrage de cron..."
cron -f
