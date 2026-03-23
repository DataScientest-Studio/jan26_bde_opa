#!/bin/bash
# run_pipeline.sh — Pipeline complète CryptoBot OPA
# Exécution : ingestion + ETL + feature engineering + entraînement modèle

set -e  # Arrêt immédiat en cas d'erreur
export PYTHONPATH=/app

echo "[$(date +"%Y-%m-%d %H:%M:%S")] ============================================"
echo "[$(date +"%Y-%m-%d %H:%M:%S")] Démarrage de la pipeline CryptoBot OPA..."
echo "[$(date +"%Y-%m-%d %H:%M:%S")] ============================================"

cd /app

# 1. Ingestion Binance → MongoDB
echo "[$(date +"%Y-%m-%d %H:%M:%S")] Étape 1/4 : Ingestion Binance → MongoDB"
python3 scripts/ingest_historical.py && \
  echo "[$(date +"%Y-%m-%d %H:%M:%S")] ✓ Ingestion terminée" || \
  { echo "[$(date +"%Y-%m-%d %H:%M:%S")] ✗ ERREUR lors de l'ingestion"; exit 1; }

# 2. ETL MongoDB → PostgreSQL
echo "[$(date +"%Y-%m-%d %H:%M:%S")] Étape 2/4 : ETL MongoDB → PostgreSQL"
python3 scripts/run_etl.py && \
  echo "[$(date +"%Y-%m-%d %H:%M:%S")] ✓ ETL terminé" || \
  { echo "[$(date +"%Y-%m-%d %H:%M:%S")] ✗ ERREUR lors de l'ETL"; exit 1; }

# 3. Feature engineering + création des labels
echo "[$(date +"%Y-%m-%d %H:%M:%S")] Étape 3/4 : Feature engineering + labels"
python3 binance_strategy_pipeline.py && \
  echo "[$(date +"%Y-%m-%d %H:%M:%S")] ✓ Dataset créé" || \
  { echo "[$(date +"%Y-%m-%d %H:%M:%S")] ✗ ERREUR lors du feature engineering"; exit 1; }

# 4. Entraînement du modèle ML
echo "[$(date +"%Y-%m-%d %H:%M:%S")] Étape 4/4 : Entraînement du modèle ML"
python3 src/models/train_model.py && \
  echo "[$(date +"%Y-%m-%d %H:%M:%S")] ✓ Modèle entraîné et sauvegardé" || \
  { echo "[$(date +"%Y-%m-%d %H:%M:%S")] ✗ ERREUR lors de l'entraînement"; exit 1; }

echo "[$(date +"%Y-%m-%d %H:%M:%S")] ============================================"
echo "[$(date +"%Y-%m-%d %H:%M:%S")] Pipeline terminée avec succès."
echo "[$(date +"%Y-%m-%d %H:%M:%S")] ============================================"
