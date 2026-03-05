# Entraînement du modèle Machine Learning

## Objectif

Dans cette étape, nous entraînons un modèle de Machine Learning afin de prédire l'évolution du prix d'une cryptomonnaie.

Les données utilisées proviennent de l'API Binance et ont été préparées dans l'étape précédente grâce au script :

src/features/build_features.py

Ce script a permis de créer un dataset contenant :

* le prix d'ouverture
* le prix le plus haut
* le prix le plus bas
* le prix de clôture
* le volume
* un label indiquant une stratégie possible : **Acheter, Vendre ou Attendre**

Le fichier généré est :

src/data/dataset_with_labels.csv

---

## Modèle utilisé

Pour ce projet nous utilisons un modèle simple et efficace :

RandomForestClassifier

Ce modèle est souvent utilisé pour les projets d’apprentissage car :

* il est facile à utiliser
* il fonctionne bien avec les données tabulaires
* il donne rapidement de bons résultats

Le script d'entraînement se trouve ici :

src/models/train_model.py

---

## Étapes réalisées

Le script réalise les opérations suivantes :

1. Charger le dataset contenant les données et les labels
2. Séparer les variables d'entrée (features) et la variable cible (label)
3. Diviser les données en deux parties :

   * données d'entraînement
   * données de test
4. Entraîner le modèle RandomForest
5. Tester les performances du modèle

---

## Résultats obtenus

Après l'entraînement, le modèle obtient une **accuracy d'environ 98 %**.

Cela signifie que le modèle arrive très souvent à prédire correctement la stratégie.

Exemple de prédictions :

* Acheter
* Vendre
* Attendre

---

## Capture de l'entraînement du modèle

![Entraînement du modèle RandomForest](figures/09_train_model_randomforest.png)

Cette capture montre :

* le lancement du script d'entraînement
* les résultats du modèle
* les métriques de performance

---

## Sauvegarde du modèle

Une fois l'entraînement terminé, le modèle est sauvegardé dans le projet :

models/model.pkl

Ce fichier permet de **réutiliser le modèle sans devoir le réentraîner**.

Il sera ensuite utilisé par l'API **FastAPI** pour générer des prédictions.

---
## Intégration dans le pipeline

Cette étape fait partie du pipeline complet du projet :

Binance API
↓
Collecte des données
↓
ETL
↓
Feature Engineering
↓
Dataset Machine Learning
↓
Entraînement du modèle
↓
API FastAPI
↓
Dashboard Streamlit

