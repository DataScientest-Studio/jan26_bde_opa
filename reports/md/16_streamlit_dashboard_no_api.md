# Dashboard Streamlit sans API

Cette capture montre le dashboard Streamlit lorsque l’API du projet n’est pas encore lancée.

Dans ce cas, le dashboard ne peut pas récupérer les données.

Les informations affichées apparaissent donc comme :

N/A

et le graphique ne s’affiche pas.

Un message indique également que l’endpoint `/charts` ne renvoie pas encore les colonnes nécessaires (`date` et `close`).

Cela signifie simplement que le dashboard attend les données provenant de l’API.

Pour que les données apparaissent correctement, il faut d’abord lancer l’API FastAPI du projet.

Une fois l’API démarrée, le dashboard peut récupérer les données et afficher :

* les statistiques du marché
* les graphiques du prix
* l’aperçu des données.

