Le dashboard présenté ci-dessus illustre le système de monitoring mis en place dans le projet CryptoBot.

Il repose sur l’utilisation de Prometheus pour la collecte des métriques et de Grafana pour leur visualisation.

La métrique principale exploitée est up, qui permet de vérifier la disponibilité du service FastAPI.

Ce dashboard présente trois indicateurs clés :

Le statut des services, indiquant si l’API est active
Le nombre de services actifs, permettant de suivre l’état global du système
La disponibilité dans le temps, offrant une vision historique du fonctionnement

Les seuils de couleur configurés permettent une lecture rapide :

Vert : service opérationnel
Rouge : service indisponible

Ce dispositif de monitoring permet d’assurer une supervision continue du système et de détecter rapidement toute anomalie.
