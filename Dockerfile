# Utilise une image Python légère comme base
FROM python:3.11-slim

# Met en place des variables d'environnement
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE ebi3.settings
ENV SECRET_KEY une_cle_par_defaut
ENV PORT 10000

# Crée un répertoire de travail dans l'image
WORKDIR /usr/src/app

# Copie les fichiers de dépendances et les installe
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie le reste du code de l'application
COPY . .

# Définition de l'utilisateur root pour les commandes de déploiement (comme migrate)
# Cette commande sera remplacée par le Docker Command de Render
CMD ["python", "manage.py", "migrate", "&&", "gunicorn", "ebi3.wsgi:application", "--bind", "0.0.0.0:$PORT"]