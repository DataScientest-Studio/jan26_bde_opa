# 🚀 OPA – CryptoBot

## 📌 Objectif du projet

CryptoBot  projet de trading crypto.

L’objectif est de construire un pipeline complet :

1. Collecte des données depuis l’API Binance
2. Stockage brut dans MongoDB
3. Transformation via un ETL Python
4. Chargement dans PostgreSQL
5. Exposition des données via une API FastAPI

---

## 🏗️ Architecture

Binance API  
⬇  
MongoDB (raw_binance_klines)  
⬇  
ETL (Python)  
⬇  
PostgreSQL (table candles)  
⬇  
FastAPI (API REST)

---

## 🗄️ Technologies utilisées

- Python
- MongoDB
- PostgreSQL
- Docker & Docker Compose
- FastAPI
- Uvicorn

---

## ⚙️ Lancer le projet

### 1️⃣ Lancer les conteneurs

```bash
docker compose up
