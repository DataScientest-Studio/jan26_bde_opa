# Préparation du dataset pour la Machine Learning

Cette étape consiste à préparer les données pour entraîner le modèle de Machine Learning.

Le script utilisé est :

src/features/build_features.py

Ce script lit les données issues du pipeline (MongoDB → ETL → PostgreSQL) puis crée un dataset utilisable par le modèle.

## Création du dataset

Le script génère un dataset contenant les informations du marché BTC :

* date
* open
* high
* low
* close
* volume

Ces données proviennent de l’API Binance et ont été stockées dans PostgreSQL après transformation.

Le dataset généré contient :

Nombre de lignes : 880

Chaque ligne correspond à une observation du marché.

## Création de la variable cible (label)

Pour entraîner le modèle, une variable cible est créée :

future_return

Elle représente la variation du prix dans le futur.

À partir de cette valeur, une étiquette (label) est générée :

* Acheter → si le prix va augmenter
* Vendre → si le prix va baisser
* Attendre → si la variation est faible

Distribution des labels :

Vendre : 437
Attendre : 281
Acheter : 162

Cela permet de transformer le problème en **classification pour le modèle de Machine Learning**.

## Aperçu du dataset

Le dataset final contient les colonnes suivantes :

* date
* open
* high
* low
* close
* volume
* future_return
* label

Ces données seront utilisées pour entraîner le modèle RandomForest dans l’étape suivante du projet.
