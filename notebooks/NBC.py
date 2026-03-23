# import packages
import pandas as pd
import numpy as np
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import loguniform

# creation du dataset
df = pd.read_csv("../dataset_with_labels.csv")

# changer la colonne date
df["date"] = pd.to_datetime(df["date"])

# splitting the data
X = df.drop(['label','date'], axis=1)
Y = df['label']

split_index = int(len(df) * 0.8)

X_train = X.iloc[:split_index]
X_test = X.iloc[split_index:]

y_train = Y.iloc[:split_index]
y_test = Y.iloc[split_index:]

# encodage de label
le = LabelEncoder()
y_train = le.fit_transform(y_train)
y_test = le.transform(y_test)

# fitting and evaluating
gnb = GaussianNB()

gnb.fit(X_train, y_train)

print("Score train:", gnb.score(X_train, y_train))
print("Score test:", gnb.score(X_test, y_test))

y_pred = gnb.predict(X_test)

print(pd.crosstab(y_test, y_pred, rownames=['Réel'], colnames=['Prédit']))
print(classification_report(y_test, y_pred))


# hyperparameter tuning

param_dist = {
    "var_smoothing": loguniform(1e-12, 1e-6)
}

gnb1 = GaussianNB()

search = RandomizedSearchCV(
    gnb1,
    param_dist,
    n_iter=20,
    cv=5,
    scoring="accuracy",
    n_jobs=-1,
    random_state=42
)

search.fit(X_train, y_train)

print("Best params:", search.best_params_)

print("Score train:", search.score(X_train, y_train))
print("Score test:", search.score(X_test, y_test))

y_pred = search.predict(X_test)

print(pd.crosstab(y_test, y_pred, rownames=['Réel'], colnames=['Prédit']))
print(classification_report(y_test, y_pred))

import joblib
joblib.dump(search.best_estimator_, "model_ML_NBC.pkl")
joblib.dump(le, "label_encoder.pkl")