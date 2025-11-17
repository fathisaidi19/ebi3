# Utiliser une image Python officielle
FROM python:3.12-slim

# Définir les variables d'environnement
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Définir le répertoire de travail
WORKDIR /usr/src/app

# Copier les fichiers de dépendance
COPY requirements.txt .

# Installer les dépendances
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copier le reste du code de l'application
COPY . .

# Collecter les fichiers statiques (étape essentielle pour WhiteNoise)
RUN python manage.py collectstatic --noinput

# Exécuter l'application en utilisant Gunicorn (référence le Procfile)
# ENTRYPOINT est déjà géré par Render