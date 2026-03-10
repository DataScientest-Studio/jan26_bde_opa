# import packages
import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import randint

# creation du dataset
df = pd.read_csv("../dataset_with_labels.csv")
#print(df.info())

# changer la colonne date
df["date"] = pd.to_datetime(df["date"])
#print(df.info())

# splitting the data
X = df.drop(['label','date'], axis=1)
Y = df['label']

split_index = int(len(df) * 0.8)
X_train = X.iloc[:split_index]
X_test = X.iloc[split_index:]
y_train = Y.iloc[:split_index]
y_test = Y.iloc[split_index:]

#encodage de label (que ça le reste est numérique)
le = LabelEncoder()
y_train = le.fit_transform(y_train)
y_test = le.transform(y_test)

#normalisation
scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# fitting and evaluating
knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X_train_scaled, y_train)

print("Score train:", knn.score(X_train_scaled, y_train))
print("Score test:", knn.score(X_test_scaled, y_test))

y_pred = knn.predict(X_test_scaled)

print(pd.crosstab(y_test, y_pred, rownames=['Réel'], colnames=['Prédit']))
print(classification_report(y_test, y_pred))

# evaluating with the best k
param_dist = {
    "n_neighbors": randint(3, 30),
    "weights": ["uniform", "distance"],
    "p": [1, 2]  # Manhattan ou Euclidean
}

knn1 = KNeighborsClassifier()

search = RandomizedSearchCV(
    knn1,
    param_dist,
    n_iter=20,
    cv=5,
    scoring="accuracy",
    n_jobs=-1
)

search.fit(X_train_scaled, y_train)

print("Best params:", search.best_params_)

print("Score train:", search.score(X_train_scaled, y_train))
print("Score test:", search.score(X_test_scaled, y_test))

y_pred = search.predict(X_test_scaled)

print(pd.crosstab(y_test, y_pred, rownames=['Réel'], colnames=['Prédit']))
print(classification_report(y_test, y_pred))