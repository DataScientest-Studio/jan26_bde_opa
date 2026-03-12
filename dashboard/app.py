import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="CryptoBot Dashboard",
    layout="wide"
)

#  Style du dashboard 
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fb;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    div[data-testid="stMetric"] {
        background-color: white;
        border: 1px solid #e9ecef;
        padding: 12px;
        border-radius: 12px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("CryptoBot Dashboard")
st.caption("Analyse crypto simple avec EMA, RSI et signal de trading")

# Sidebar 
st.sidebar.header(" Paramètres")

crypto = st.sidebar.selectbox(
    "Choisir une crypto",
    ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "ADAUSDT", "XRPUSDT", "DOGEUSDT"]
)

interval = st.sidebar.selectbox(
    "Intervalle",
    ["1m", "5m", "15m", "1h", "4h", "1d"],
    index=3
)

period = st.sidebar.selectbox(
    "Période",
    ["1D", "1W", "1M", "1Y"],
    index=0
)

refresh = st.sidebar.button(" Refresh")

# Forcer le rerun léger si bouton cliqué
if refresh:
    st.rerun()

params = {
    "symbol": crypto,
    "interval": interval,
    "period": period
}

# Appels API 
try:
    stats = requests.get(f"{API_URL}/stats", params=params, timeout=15).json()
    chart_data = requests.get(f"{API_URL}/charts", params=params, timeout=15).json()
    signal_data = requests.get(f"{API_URL}/signals", params=params, timeout=15).json()
except Exception:
    st.error("Impossible de joindre l’API. Vérifie que FastAPI tourne sur le port 8000.")
    st.stop()

# Stats 
col1, col2, col3, col4 = st.columns(4)
col1.metric("Last Price", round(stats["last_price"], 2))
col2.metric("Max Price", round(stats["max_price"], 2))
col3.metric("Min Price", round(stats["min_price"], 2))
col4.metric("Average Volume", round(stats["avg_volume"], 2))

st.divider()

# Signal 
signal = signal_data["signal"]

if signal == "BUY":
    st.success(f"Signal : {signal} | {signal_data['reason']}")
elif signal == "SELL":
    st.error(f"Signal : {signal} | {signal_data['reason']}")
else:
    st.warning(f"Signal : {signal} | {signal_data['reason']}")

signal_col1, signal_col2, signal_col3 = st.columns(3)
signal_col1.metric("EMA 20", signal_data["ema_20"])
signal_col2.metric("RSI", signal_data["rsi"])
signal_col3.metric("Close", signal_data["close"])

st.divider()

#  DataFrame 
if not isinstance(chart_data, list) or len(chart_data) == 0:
    st.error("Aucune donnée graphique reçue depuis l’API.")
    st.stop()

df = pd.DataFrame(chart_data)
df["date"] = pd.to_datetime(df["date"])

# Graphique prix + EMA 
st.subheader(f" Prix de {crypto}")

fig_price = px.line(
    df,
    x="date",
    y="close",
    title=f"{crypto} - Prix de clôture"
)

fig_price.add_scatter(
    x=df["date"],
    y=df["ema_20"],
    mode="lines",
    name="EMA 20"
)

st.plotly_chart(fig_price, use_container_width=True)

# Graphique RSI
st.subheader(" RSI")

fig_rsi = px.line(
    df,
    x="date",
    y="rsi",
    title="RSI"
)

fig_rsi.add_hline(y=70, line_dash="dash")
fig_rsi.add_hline(y=30, line_dash="dash")

st.plotly_chart(fig_rsi, use_container_width=True)

#  Tableau 
st.subheader("Dernières données")
st.dataframe(
    df[["date", "close", "ema_20", "rsi"]].tail(50),
    use_container_width=True
)
