import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="CryptoBot Dashboard",
    layout="wide"
)

# Style
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
st.sidebar.header("Paramètres")

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

refresh = st.sidebar.button("Refresh")

if refresh:
    st.rerun()

params = {
    "symbol": crypto,
    "interval": interval,
    "period": period
}

# API
try:
    stats = requests.get(f"{API_URL}/stats", params=params).json()
    chart_data = requests.get(f"{API_URL}/charts", params=params).json()
    signal_data = requests.get(f"{API_URL}/signals", params=params).json()
except:
    st.error("API non accessible")
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

colA, colB, colC = st.columns(3)
colA.metric("EMA 20", signal_data["ema_20"])
colB.metric("RSI", signal_data["rsi"])
colC.metric("Close", signal_data["close"])

st.divider()

# Data
df = pd.DataFrame(chart_data)
df["date"] = pd.to_datetime(df["date"])

# GRAPH 
st.subheader(f"Prix de {crypto}")

fig_price = px.line(
    df,
    x="date",
    y="close"
)

# Prix (close)
fig_price.data[0].name = "Prix (close)"
fig_price.data[0].line.color = "#3b82f6"
fig_price.data[0].line.width = 2
fig_price.data[0].showlegend = True  

#  EMA (Tendance moyenne)
fig_price.add_scatter(
    x=df["date"],
    y=df["ema_20"],
    mode="lines",
    name="EMA 20 (tendance)",
    line=dict(color="#ef4444", width=2)
)

# Légende à droite
fig_price.update_layout(
    legend=dict(
        orientation="v",
        y=1,
        x=1.02
    ),
    plot_bgcolor="white",
    paper_bgcolor="white"
)

st.plotly_chart(fig_price, use_container_width=True)

# RSI
st.subheader("RSI")

fig_rsi = px.line(df, x="date", y="rsi")

fig_rsi.add_hline(y=70, line_dash="dash")
fig_rsi.add_hline(y=30, line_dash="dash")

st.plotly_chart(fig_rsi, use_container_width=True)

# Table
st.subheader("Dernières données")
st.dataframe(df.tail(50))
