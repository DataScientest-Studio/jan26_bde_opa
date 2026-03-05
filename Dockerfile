# Image Python officielle
FROM python:3.11

# Dossier de travail dans le container
WORKDIR /app

# Copier les dépendances
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le projet
COPY . .

# Commande par défaut au lancement
CMD ["python", "src/storage/mongo.py"]