#!/bin/bash

echo "🛑 On ferme les anciens serveurs (si jamais ils tournent déjà)..."
pkill -f uvicorn 2>/dev/null
pkill -f streamlit 2>/dev/null

sleep 2

echo "🚀 Lancement de l'API FastAPI (port 8000)..."
python -m uvicorn src.api.main:app --reload &

sleep 3

echo "📊 Lancement du Dashboard Streamlit (port 8501)..."
python -m streamlit run dashboard/app.py