import requests
import pandas as pd


# RÉCUPÉRER LES DONNÉES DE L'API BINANCE

url = "https://api.binance.com/api/v3/klines"

params = {
    "symbol": "BTCUSDT",
    "interval": "1h",
    "limit": 1000
}

response = requests.get(url, params=params)

# vérifier si l'API répond correctement
if response.status_code != 200:
    print("Erreur API :", response.status_code)
    exit()

data = response.json()


# TRANSFORMER LES DONNÉES EN DATAFRAME

columns = [
    "open_time",
    "open",
    "high",
    "low",
    "close",
    "volume",
    "close_time",
    "quote_asset_volume",
    "number_of_trades",
    "taker_buy_base_asset_volume",
    "taker_buy_quote_asset_volume",
    "ignore"
]

df = pd.DataFrame(data, columns=columns)


#  NETTOYER ET TRANSFORMER LES DONNÉES

# convertir les timestamps en date
df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")
df["close_time"] = pd.to_datetime(df["close_time"], unit="ms")

# supprimer la colonne inutile
df = df.drop(columns=["ignore"])

# convertir certaines colonnes en nombres
for col in ["open", "high", "low", "close", "volume"]:
    df[col] = df[col].astype(float)

# utiliser open_time comme date principale
df["date"] = df["open_time"]

# trier les données par date
df = df.sort_values("date")


#  CRÉER UNE STRATÉGIE SIMPLE (PRÉDICTION SUR 5 JOURS)

horizon = 120      # 5 jours = 120 heures
threshold = 0.02   # variation de 2 %

# calcul du rendement futur
df["future_return"] = (df["close"].shift(-horizon) - df["close"]) / df["close"]

# création des labels
labels = []

for value in df["future_return"]:
    
    if value > threshold:
        labels.append("Acheter")
        
    elif value < -threshold:
        labels.append("Vendre")
        
    else:
        labels.append("Attendre")

df["label"] = labels

# supprimer les lignes avec valeurs manquantes
df = df.dropna()


#  CRÉER LE DATASET FINAL

df = df[[
    "date",
    "open",
    "high",
    "low",
    "close",
    "volume",
    "future_return",
    "label"
]]


# sauvegarder le dataset
df.to_csv("dataset_with_labels.csv", index=False)


# afficher quelques informations
print("Dataset créé avec succès")
print("Nombre de lignes :", len(df))
print("Distribution des classes :")
print(df["label"].value_counts())
print(df.head())