# Dashboard Streamlit

Le dashboard du projet CryptoBot a été développé avec Streamlit afin de visualiser les données issues du pipeline Data Engineering.

Il constitue la couche de visualisation finale du pipeline.

## Architecture du pipeline

Binance API  
↓  
MongoDB  
↓  
ETL Python  
↓  
PostgreSQL  
↓  
FastAPI  
↓  
Streamlit Dashboard  

## Lancement du dashboard

```bash
streamlit run src/src/ingestion/dashboard/dashboard.py

## Résultat

Capture du dashboard Streamlit :

![Dashboard Streamlit](figures/07_streamlit_dashboard.png)
