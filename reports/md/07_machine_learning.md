# Machine Learning – Préparation de l’environnement

## Ajout des dépendances ML

Le fichier requirements.txt a été mis à jour afin d’ajouter les bibliothèques nécessaires à l’entraînement du modèle de machine learning.

Bibliothèques ajoutées :

- pandas
- numpy
- scikit-learn
- joblib

Ces dépendances permettent de préparer l’environnement pour entraîner un modèle RandomForest sur les données crypto.

## Pipeline du projet

Binance API  
↓  
MongoDB (raw data)  
↓  
ETL  
↓  
PostgreSQL (candles)  
↓  
Machine Learning