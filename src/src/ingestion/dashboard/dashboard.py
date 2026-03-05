import streamlit as st
import pandas as pd

st.set_page_config(page_title="CryptoBot Dashboard", layout="wide")

st.title("📊 CryptoBot Dashboard")

st.write("Pipeline Data Engineering :")
st.write("Binance API → MongoDB → ETL → PostgreSQL → FastAPI → Streamlit")

# Exemple de données
data = {
    "Crypto": ["BTC", "ETH", "BNB"],
    "Price": [65000, 3500, 600]
}

df = pd.DataFrame(data)

st.subheader("Prix des cryptos")

st.dataframe(df)

st.subheader("Graphique")

st.bar_chart(df.set_index("Crypto"))