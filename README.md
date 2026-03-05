# 🚀 OPA – CryptoBot

# 🎯 Objectif du projet

Construire un pipeline data complet :

1. Collecte des données depuis l'API Binance
2. Stockage brut dans MongoDB
3. Transformation des données via un ETL Python
4. Chargement dans PostgreSQL (data warehouse)
5. Exposition des données via une API FastAPI
6. Prédiction du marché avec un modèle de Machine Learning

---

## 🏗️ Architecture

Le pipeline de données suit les étapes suivantes :

Binance API  
⬇  
MongoDB (collection : raw_binance_klines) — stockage brut des données  
⬇  
ETL Python — nettoyage et transformation  
⬇  
PostgreSQL (table : candles) — stockage structuré  
⬇  
FastAPI — API REST  
⬇  
Machine Learning — prédiction UP / DOWN

---

## 🗄️ Technologies utilisées

- Python
- MongoDB
- PostgreSQL
- Docker & Docker Compose
- FastAPI
- Uvicorn
- Pandas
- Scikit-learn
- Joblib

---

## 📂 Structure du projet
src/
├── ingestion/ → récupération des données Binance
├── processors/ → transformation ETL
├── storage/ → stockage MongoDB / PostgreSQL
└── api/ → API FastAPI

scripts/
├── ingest_historical.py → ingestion historique Binance
└── run_etl.py → pipeline ETL Mongo → Postgres

notebooks/
└── training_model.ipynb → entraînement du modèle ML

models/
└── model.pkl → modèle entraîné

predict_model.py
→ script de prédiction utilisant le modèle

reports/
├── 01_architecture.md
├── 02_ingestion_binance.md
├── 03_mongodb_storage.md
├── 04_etl_pipeline.md
├── 05_postgres_datawarehouse.md
├── 06_api_fastapi.md
└── 07_machine_learning.md

---

## ⚙️ Lancer le projet

### 1️⃣ Lancer les conteneurs Docker

```bash
docker compose up -d

