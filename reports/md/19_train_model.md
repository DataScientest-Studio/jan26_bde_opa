# Entraînement du modèle Machine Learning

Dans cette étape, nous entraînons un modèle de Machine Learning pour prédire l’évolution du prix du Bitcoin.

Le script utilisé est :

src/models/train_model.py

## Objectif

Le modèle apprend à prédire trois actions possibles sur le marché :

* Acheter
* Attendre
* Vendre

Ces décisions sont basées sur les données du marché (prix, volume, etc.).

## Entraînement du modèle

Le modèle utilisé est :

RandomForest

Il est entraîné sur les données préparées lors de l’étape précédente.

Commande utilisée :

python src/models/train_model.py

## Résultat

Après l’entraînement, le modèle affiche un score appelé **accuracy**.

Accuracy obtenue :

1.0

Cela signifie que le modèle a correctement prédit les données du jeu de test.

## Sauvegarde du modèle

Une fois entraîné, le modèle est sauvegardé dans le fichier :

models/model.pkl

Ce fichier sera utilisé plus tard par l’API pour faire des prédictions.
