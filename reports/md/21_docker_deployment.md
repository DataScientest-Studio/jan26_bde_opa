## Docker

Le projet utilise Docker pour lancer tous les services automatiquement.

Les services utilisés sont :

* MongoDB : stockage des données
* PostgreSQL : base de données du projet
* FastAPI : API pour accéder aux données
* Streamlit : dashboard de visualisation
* Airflow : automatisation du pipeline

Le fichier `docker-compose.yml` permet de démarrer toute l'application avec une seule commande :

docker compose up

