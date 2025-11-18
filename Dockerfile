# Utiliser une image Python officielle et légère
FROM python:3.12-slim

# ===============================================
# 1. Configuration de l'environnement
# ===============================================

# Variables d'environnement pour Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Définir le répertoire de travail dans le conteneur.
# Toutes les commandes suivantes seront exécutées à partir de ce chemin.
WORKDIR /usr/src/app

# Variable d'environnement pour la base de données.
# Nous utilisons une URL SQLite factice ici pour permettre à Django de charger
# les paramètres (settings.py) sans base de données réelle pendant le build.
ENV DATABASE_URL="sqlite:///temp.db"

# ===============================================
# 2. Installation des dépendances
# ===============================================

# Copier uniquement le fichier de dépendances pour tirer parti du cache Docker
COPY requirements.txt .

# Mettre à jour pip et installer toutes les dépendances
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# ===============================================
# 3. Copie du code et Préparation
# ===============================================

# Copier le reste du code source de l'application (y compris manage.py)
# Le point source est votre répertoire local (context), le point destination est le WORKDIR (/usr/src/app)
COPY . .

# Collecter les fichiers statiques (étape essentielle pour WhiteNoise et les déploiements)
# Cette étape est désormais possible car manage.py est présent dans le WORKDIR.
RUN python manage.py collectstatic --noinput

# ===============================================
# 4. Commande de lancement du serveur
# ===============================================

# La commande finale pour exécuter Gunicorn, en utilisant le module WSGI de votre projet.
# Remplacez 'ebi3.wsgi:application' par le chemin réel si différent (par exemple, mon_projet.wsgi:application).
CMD gunicorn ebi3.wsgi:application --bind 0.0.0.0:10000 --workers 2