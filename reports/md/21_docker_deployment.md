## Déploiement avec Docker

Afin de garantir la reproductibilité du projet, l'application est conteneurisée avec Docker.

Le fichier `docker-compose.yml` permet de lancer l'ensemble des services nécessaires au fonctionnement du pipeline.

Les services déployés sont :

* MongoDB : stockage des données brutes
* PostgreSQL : data warehouse
* FastAPI : exposition de l'API
* Streamlit : dashboard de visualisation
* Airflow : orchestration et automatisation du pipeline

L'ensemble de l'application peut être lancé avec la commande :

docker compose up --build
