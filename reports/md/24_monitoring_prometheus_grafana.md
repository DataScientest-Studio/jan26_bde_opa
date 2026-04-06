# 24. Monitoring avec Prometheus et Grafana

Dans le cadre du projet CryptoBot, une solution de monitoring a été mise en place à l’aide de Prometheus et Grafana.

## Prometheus

Prometheus est utilisé pour collecter les métriques du système et superviser l’état des services.

L’interface est accessible via :
http://localhost:9090

## Grafana

Grafana permet de visualiser les métriques collectées dans des tableaux de bord interactifs.

L’interface est accessible via :
http://localhost:3000

## Intégration

Grafana est connecté à Prometheus comme source de données via l’URL interne Docker :

http://prometheus:9090

Cette configuration permet de superviser le système en temps réel.

## Conclusion

L’ajout de Prometheus et Grafana permet d’introduire une couche d’observabilité dans l’architecture, renforçant ainsi le caractère professionnel du projet.

**Figure : Monitoring du projet avec Prometheus et Grafana**
