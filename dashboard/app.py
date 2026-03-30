import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import joblib
from pathlib import Path

API_URL = "http://opa_app:8000"

st.set_page_config(
    page_title="CryptoBot Dashboard",
    layout="wide"
)

# STYLE
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

# SIDEBAR
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

params = {
    "symbol": crypto,
    "interval": interval,
    "period": period
}

#onglets
tab_dashboard, tab_ml = st.tabs(["Dashboard", "Machine Learning"])

#onglet dashboard
with tab_dashboard:
    # API CALL
    try:
        stats = requests.get(f"{API_URL}/stats", params=params).json()
        chart_data = requests.get(f"{API_URL}/charts", params=params).json()
        signal_data = requests.get(f"{API_URL}/signals", params=params).json()
    except:
        st.error("API non accessible")
        st.stop()

    # METRICS
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Last Price", round(stats["last_price"], 2))
    col2.metric("Max Price", round(stats["max_price"], 2))
    col3.metric("Min Price", round(stats["min_price"], 2))
    col4.metric("Average Volume", round(stats["avg_volume"], 2))

    st.divider()

    # SIGNAL
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

    # DATA
    df = pd.DataFrame(chart_data)
    df["date"] = pd.to_datetime(df["date"])

    # GRAPH PRIX
    st.subheader(f"Prix de {crypto}")

    fig_price = px.line(
        df,
        x="date",
        y="close"
    )

    # COURBE de prix 
    fig_price.data[0].name = "Prix (close)"
    fig_price.data[0].line.color = "#3b82f6"
    fig_price.data[0].line.width = 2

    # EMA 
    fig_price.add_scatter(
        x=df["date"],
        y=df["ema_20"],
        mode="lines",
        name="EMA 20",
        line=dict(color="#ef4444", width=2)
    )

    fig_price.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        legend=dict(x=1.02, y=1)
    )

    st.plotly_chart(fig_price, use_container_width=True)

    # RSI
    st.subheader("RSI")

    fig_rsi = px.line(df, x="date", y="rsi")

    fig_rsi.add_hline(y=70, line_dash="dash")
    fig_rsi.add_hline(y=30, line_dash="dash")

    st.plotly_chart(fig_rsi, use_container_width=True)

    # TABLE
    st.subheader("Dernières données")
    st.dataframe(df.tail(50))

# onglet ML
with tab_ml:
    st.header("Machine Learning (ML)")

    # Stats 
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Last Price", round(stats["last_price"], 2))
    col2.metric("Max Price", round(stats["max_price"], 2))
    col3.metric("Min Price", round(stats["min_price"], 2))
    col4.metric("Average Volume", round(stats["avg_volume"], 2))

    st.divider()

    # modèle ML
    @st.cache_resource
    def load_ml():
        BASE_DIR = Path(__file__).resolve().parent
        model = joblib.load(BASE_DIR / "model_ML_NBC.pkl")
        le = joblib.load(BASE_DIR / "label_encoder.pkl")
        return model, le

    model, le = load_ml()

    # récupère les données via l'API
    try:
        chart_data = requests.get(f"{API_URL}/charts", params=params, timeout=15).json()
    except Exception:
        st.error("Erreur API")
        st.stop()

    df = pd.DataFrame(chart_data)
    df["date"] = pd.to_datetime(df["date"])

    # nettoyage
    feature_cols = [
        "open",
        "high",
        "low",
        "close",
        "volume",
        "return_1h",
        "ma_24",
        "volatility_24"
    ]

    X_live = df[feature_cols].dropna()

    # prédiction et décodage
    preds = model.predict(X_live)
    preds_labels = le.inverse_transform(preds)

    df["prediction"] = None
    df.loc[X_live.index, "prediction"] = preds_labels

    # premier affichage
    last_pred = df["prediction"].dropna().iloc[-1]

    if last_pred == "Acheter":
        st.success(f"Signal Machine Learning : BUY")
    elif last_pred == "Vendre":
        st.error(f"Signal Machine Learning : SELL")
    else:
        st.warning(f"Signal Machine Learning : HOLD")

    # graphique
    st.subheader("Signaux du modèle Naive Bayes Classifier")

    fig = px.line(df, x="date", y="close", title="Prix")

    try:
        proba = model.predict_proba(X_live)
        df.loc[X_live.index, "confidence"] = proba.max(axis=1)
    except:
        df["confidence"] = 0.5  # fallback si modèle sans proba

    buy_df = df[df["prediction"] == "Acheter"]
    sell_df = df[df["prediction"] == "Vendre"]
    wait_df = df[df["prediction"] == "Attendre"]

    fig.add_scatter(
        x=buy_df["date"],
        y=buy_df["close"],
        mode="markers",
        name="Acheter",
        marker=dict(symbol="triangle-up", size=buy_df["confidence"] * 20 + 5)
    )

    fig.add_scatter(
        x=sell_df["date"],
        y=sell_df["close"],
        mode="markers",
        name="Vendre",
        marker=dict(symbol="triangle-down", size=sell_df["confidence"] * 20 + 5)
    )

    fig.add_scatter(
        x=wait_df["date"],
        y=wait_df["close"],
        mode="markers",
        name="Attendre",
        marker=dict(symbol="circle", size=wait_df["confidence"] * 15 + 5)
    )

    fig.update_layout(legend_title="Signaux",hovermode="x unified")

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    ### Légende des signaux
    **Taille des points** = niveau de confiance du modèle  
    Plus le point est grand, plus la prédiction est jugée fiable.
    """)

    st.divider()

    # répartition des signaux
    counts = df["prediction"].value_counts()
    percentages = (counts / counts.sum() * 100).round(2)    
    st.markdown("### Répartition (%)")
    for label in counts.index:
        st.write(f"{label} : {counts[label]} ({percentages[label]}%)")

    st.divider()

    # explication du modèle de ML choisit
    st.subheader("Comprendre le modèle ?")
    st.markdown("""
    ##### Objectif
    Cette application prédit un signal de trading (Acheter, Vendre ou Attendre) à partir des données du marché.

    ##### Modèles testés
    - Naive Bayes
    - K-Nearest Neighbors (KNN)
    - Random Forest

    ##### Modèle retenu
    Le modèle **Naive Bayes** a été sélectionné car il offre les meilleures performances :
    - Accuracy : 0.73
    - F1-score : 0.74

    ##### Fonctionnement
    Le modèle utilise plusieurs indicateurs :
    - variation du prix
    - tendance (moyenne mobile)
    - volatilité

    ##### Limites
    Les prédictions ne garantissent pas les résultats futurs. Le marché reste incertain.
    """)
