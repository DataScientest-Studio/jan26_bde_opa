#!/bin/sh
set -e

echo " Création du dossier logs..."
mkdir -p /app/logs

echo " Installation de la crontab..."
crontab /app/crontab.docker

echo " Contenu de la crontab :"
crontab -l

echo " Démarrage du service cron..."
cron -f

