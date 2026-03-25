# import packages
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
from sklearn.tree import export_graphviz
import graphviz
from sklearn.model_selection import TimeSeriesSplit

from scipy.stats import randint

# creation du dataset
df = pd.read_csv("dataset_with_labels.csv")
#print(df.info())

# changer la colonne date
df["date"] = pd.to_datetime(df["date"])
#print(df.info())

# splitting the data (pas besoin de normaliser pour ce modèle)
X = df.drop(['label','date','volume','return_1h','high','ma_24'], axis=1)
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

# fitting 
rf = RandomForestClassifier(random_state=42,class_weight="balanced")
rf.fit(X_train, y_train)

print('Score sur ensemble train', rf.score(X_train, y_train))
print('Score sur ensemble test', rf.score(X_test, y_test))

y_pred = rf.predict(X_test)

#evaluating
print(pd.crosstab(y_test, y_pred, rownames=['Réel'], colnames=['Prédit']))

print(classification_report(y_test, y_pred, ))

#feature importance
'''feat_importances = pd.DataFrame(rf.feature_importances_, index=X.columns, columns=["Importance"])
feat_importances.sort_values(by='Importance', ascending=False, inplace=True)
feat_importances.plot(kind='bar', figsize=(8,6))
plt.title("Importance des features")
plt.ylabel("Importance")
plt.tight_layout()
plt.savefig("feature_importance.png", dpi=300) '''

# visualizing the results
'''for i in range(3):
    tree = rf.estimators_[i]
    dot_data = export_graphviz(tree,
                               feature_names=X_train.columns,  
                               filled=True,  
                               max_depth=2, 
                               impurity=False, 
                               proportion=True)
    graph = graphviz.Source(dot_data)
    print(graph)'''

# hyperparameter tuning
param_dist = {
  'n_estimators': randint(100, 500),
  'max_depth': randint(3, 15),
  'min_samples_split': randint(2, 10),
  'min_samples_leaf': randint(1, 5)
}


# Create a random forest classifier
rf1 = RandomForestClassifier(random_state=42, n_jobs=-1)

# Use random search to find the best hyperparameters
tscv = TimeSeriesSplit(n_splits=5)
rand_search = RandomizedSearchCV(
  rf1, param_distributions=param_dist,
  n_iter=10, cv=tscv, scoring='accuracy',
  n_jobs=-1, random_state=42)

#entraînement
rand_search.fit(X_train, y_train)
print("Best parameters:", rand_search.best_params_)

#meilleur modèle
best_rf = rand_search.best_estimator_
print('Score sur ensemble train', best_rf.score(X_train, y_train))
print('Score sur ensemble test', best_rf.score(X_test, y_test))
y_pred = best_rf.predict(X_test)

print(classification_report(y_test, y_pred))