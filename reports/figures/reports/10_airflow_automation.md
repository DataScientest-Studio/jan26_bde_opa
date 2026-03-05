# Automatisation du pipeline avec Apache Airflow

## Lancement d’Airflow avec Docker

Dans cette étape, nous avons lancé Apache Airflow afin d’automatiser l’exécution du pipeline de données.

Pour simplifier l’installation, Airflow est exécuté dans un conteneur Docker grâce au fichier :

docker-compose.airflow.yml

Ce fichier permet de :

- démarrer Airflow
- installer les librairies nécessaires (pandas, scikit-learn, requests)
- initialiser la base de données Airflow
- créer un utilisateur administrateur
- lancer le scheduler et l’interface web

Commande utilisée :

docker compose -f docker-compose.airflow.yml up -d

Une fois lancé, Airflow télécharge l’image officielle et crée le conteneur.

Interface accessible sur :

http://localhost:8080

Identifiants :

username : airflow  
password : airflow

Cette interface permet de visualiser et exécuter les pipelines automatisés appelés DAG (Directed Acyclic Graph).

Dans notre projet, le DAG **cryptobot_pipeline** orchestre les étapes suivantes :

1. build_features → création du dataset Machine Learning
2. train_model → entraînement du modèle RandomForest

Cette automatisation permet d’exécuter le pipeline complet sans intervention manuelle.