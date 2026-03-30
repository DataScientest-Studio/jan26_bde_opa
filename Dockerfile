# Image Python officielle
FROM python:3.11

# Dossier de travail dans le container
WORKDIR /app

# Copier les dépendances
COPY requirements.txt .

# Installer les dépendances système (cron pour le service scheduler)
RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*

# Installer les dépendances python
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le projet
COPY . .
