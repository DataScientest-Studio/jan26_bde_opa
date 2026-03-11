import streamlit as st
import requests
import pandas as pd
import plotly.express as px

import os 
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="BTCUSDT Dashboard", layout="wide")
st.title(" Dashboard Finance — BTCUSDT (Binance)")

# Récupérer les stats
stats = requests.get(f"{API_URL}/stats").json()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Last Price", f"{stats.get('last_price', 'N/A')}")
col2.metric("Max Price", f"{stats.get('max_price', 'N/A')}")
col3.metric("Min Price", f"{stats.get('min_price', 'N/A')}")
col4.metric("Average Volume", f"{stats.get('average_volume', 'N/A')}")

st.divider()

# Récupérer les données pour graphiques 
chart_data = requests.get(f"{API_URL}/charts").json()
if isinstance(chart_data, dict):
    chart_data = [chart_data]

df = pd.DataFrame(chart_data)

# on convertit date 
if "date" in df.columns:
    df["date"] = pd.to_datetime(df["date"])

st.subheader(" Prix BTC (Close)")
if "date" in df.columns and "close" in df.columns:
    fig = px.line(df, x="date", y="close", title="BTCUSDT Close Price")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Le endpoint /charts ne renvoie pas encore les colonnes 'date' et 'close'.")

st.subheader("Aperçu des données")
st.dataframe(df.tail(30), use_container_width=True)