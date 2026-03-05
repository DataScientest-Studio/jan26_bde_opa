## Détection du DAG dans l’interface Airflow

![Airflow DAG](figures/11_airflow_dag_visible.png)

Cette capture montre l’interface web d’Apache Airflow accessible sur http://localhost:8080.

Le pipeline nommé **cryptobot_pipeline** est automatiquement détecté par Airflow grâce au fichier placé dans le dossier **dags/**.

Airflow permet de :
- visualiser les pipelines de données
- planifier leur exécution
- automatiser les différentes étapes du projet

Dans notre projet CryptoBot, ce pipeline orchestre plusieurs tâches du traitement des données, notamment :
- la préparation des features
- l'entraînement du modèle de Machine Learning

Airflow est lancé en mode standalone. 
Dans ce mode, un utilisateur administrateur est créé automatiquement lors du premier démarrage. 
Les identifiants sont générés dans les logs du conteneur Docker.