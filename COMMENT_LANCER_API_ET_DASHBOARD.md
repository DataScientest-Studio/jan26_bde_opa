Guide pour lancer l'API et le Dashboard

Ce guide explique comment lancer l’API FastAPI et le dashboard Streamlit du projet sur votre ordinateur.

Le projet est composé de deux éléments principaux :

1. Une API développée avec FastAPI
2. Un dashboard interactif développé avec Streamlit

Pour simplifier le lancement du projet, un script appelé **start.sh** a été créé.  
Ce script permet de lancer automatiquement l’API et le dashboard avec une seule commande.

--------------------------------------------------

Architecture du projet

Le fonctionnement du projet est le suivant :

FastAPI (API REST) - Port 8000  
↓  
Streamlit (Dashboard) - Port 8501  
↓  
Visualisation des données dans le navigateur

--------------------------------------------------

Étape 1 : Cloner le projet depuis GitHub

Ouvrez un terminal sur votre ordinateur.

Tapez la commande suivante pour télécharger le projet :

```
git clone https://github.com/DataScientest-Studio/jan26_bde_opa.git
```

Ensuite, entrez dans le dossier du projet :

```
cd jan26_bde_opa
```

--------------------------------------------------

Étape 2 : Installer les dépendances

Avant de lancer le projet, il faut installer les bibliothèques Python nécessaires.

Dans le terminal, tapez :

```
pip install -r requirements.txt
```

Cette commande va installer toutes les dépendances nécessaires pour faire fonctionner le projet.

--------------------------------------------------

Étape 3 : Lancer l’API et le Dashboard

Pour éviter d’avoir à lancer plusieurs commandes, un script a été créé.

Dans le terminal, tapez simplement :

```
./start.sh
```

Ce script va automatiquement :

- fermer les anciens serveurs si nécessaire
- lancer l’API FastAPI sur le port **8000**
- lancer le dashboard Streamlit sur le port **8501**

--------------------------------------------------

Étape 4 : Accéder au Dashboard

Une fois le script lancé, le dashboard sera accessible dans votre navigateur.

Ouvrez le lien suivant :

```
http://localhost:8501
```

Vous pourrez alors visualiser les graphiques et les données du projet.

--------------------------------------------------

Étape 5 : Accéder à l’API

L’API FastAPI est accessible à l’adresse suivante :

```
http://localhost:8000
```

La documentation interactive de l’API est disponible ici :

```
http://localhost:8000/docs
```

--------------------------------------------------

Étape 6 : Relancer le projet après avoir éteint l’ordinateur

Lorsque vous éteignez votre ordinateur, les serveurs s’arrêtent automatiquement.

Pour relancer le projet, il suffit simplement de refaire les deux commandes suivantes :

```
cd jan26_bde_opa
```

Puis :

```
./start.sh
```

Cela relancera automatiquement :

- l’API FastAPI
- le dashboard Streamlit

--------------------------------------------------


Grâce au script **start.sh**, il n’est plus nécessaire de lancer plusieurs commandes manuellement.

Une seule commande permet de lancer tout le projet.
