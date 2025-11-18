FROM python:3.12-slim

# ===============================================
# 1. Configuration de l'environnement
# ===============================================
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Ajoutez une base de données temporaire pour que collectstatic ne plante pas
ENV DATABASE_URL="sqlite:///temp.db"
ENV PORT 10000

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

# 🛑 RETRAIT DE L'ÉTAPE MIGRATE (elle se fera au runtime)

# Collecter les fichiers statiques (utilise la DB temporaire)
RUN python manage.py collectstatic --noinput

# ===============================================
# 4. Commande de lancement du serveur
# ===============================================
# Cette commande sera remplacée par le Start Command sur Render
# CMD gunicorn ebi3.wsgi:application --bind 0.0.0.0:$PORT --workers 2