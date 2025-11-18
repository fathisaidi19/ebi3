# Utiliser une image Python officielle et légère
FROM python:3.12-slim

# ===============================================
# 1. Configuration de l'environnement
# ===============================================
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Remarque : La variable DATABASE_URL n'est PAS définie ici,
# elle doit être fournie par Render (External Database URL)
# dans les variables d'environnement du service web.

# Définir le répertoire de travail
WORKDIR /usr/src/app

# ===============================================
# 2. Installation des dépendances
# ===============================================
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# ===============================================
# 3. Copie du code et Préparation
# ===============================================
COPY . .

# 🛑 NOUVEAU : Exécuter les migrations.
# C'est l'étape qui était manquante et causait l'erreur 500.
# Elle utilise la DATABASE_URL fournie par Render.
RUN python manage.py migrate --noinput

# Collecter les fichiers statiques
RUN python manage.py collectstatic --noinput

# ===============================================
# 4. Commande de lancement du serveur
# ===============================================
# Lancer Gunicorn pour servir l'application
CMD gunicorn ebi3.wsgi:application --bind 0.0.0.0:$PORT --workers 2