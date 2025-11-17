# ebi3/settings.py

import os
from pathlib import Path
import environ

# Initialisation de django-environ
env = environ.Env(
    # Définition des types par défaut pour les variables
    DEBUG=(bool, False)
)

# Construit les chemins à l'intérieur du projet comme ceci : BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# LECTURE DU FICHIER .env
# Tente de lire le fichier .env si il existe (pour le développement local)
if os.path.exists(BASE_DIR / ".env"):
    environ.Env.read_env(BASE_DIR / ".env")
# Sinon, on suppose que les variables sont déjà dans l'environnement (Render)


# --- PARAMÈTRES DE BASE IMPORTÉS DE .env ---
SECRET_KEY = env("SECRET_KEY")
DEBUG = env("DEBUG")

# ⚠️ GESTION DES HÔTES AUTORISÉS (CRITIQUE POUR LA PROD)
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '::1']

# Configuration spécifique pour Render en mode production (DEBUG=False)
if not DEBUG:
    # RENDER_EXTERNAL_HOSTNAME est défini par Render
    RENDER_HOST = env.str("RENDER_EXTERNAL_HOSTNAME", default="")

    # 1. Ajout de l'hôte récupéré (meilleure pratique)
    if RENDER_HOST:
        ALLOWED_HOSTS.append(RENDER_HOST)

    # 2. Ajout du domaine de base de Render (wildcard)
    ALLOWED_HOSTS.append('.onrender.com')

    # 3. Ajout explicite du domaine de l'application
    ALLOWED_HOSTS.append('ebi3-jii8.onrender.com')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Vos applications
    'annonces',
    'messagerie',
    'comptes',
    'transporteurs',
    'stockages',
    'widget_tweaks',

    # Librairies tierces nécessaires
    'django_filters',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # Middleware pour les fichiers statiques de production (WhiteNoise)
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ebi3.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ebi3.wsgi.application'

# --- CONFIGURATION DE LA BASE DE DONNÉES (DB) ---
# Utilise la variable d'environnement DATABASE_URL (par Render) ou l'utilise du .env (local)
DATABASES = {
    'default': env.db()
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'fr-fr'

TIME_ZONE = 'Europe/Paris'

USE_I18N = True

USE_TZ = True

# --- CONFIGURATION DES FICHIERS STATIQUES ---
# Utilisation de env() pour l'URL et le ROOT des statics (assure la compatibilité local/prod)
STATIC_URL = env("STATIC_URL", default='/static/')
STATIC_ROOT = BASE_DIR / env("STATIC_ROOT", default='staticfiles')

# Fichiers statiques supplémentaires du projet
STATICFILES_DIRS = [
    BASE_DIR / 'static',  # S'il y a un dossier 'static' à la racine du projet
]

# Fichiers médias (images d'annonces, etc.)
MEDIA_URL = '/media/'
# IMPORTANT: Render ne supporte pas le stockage de fichiers médias permanents sur le disque local de l'application.
# Pour le déploiement réel, vous devrez utiliser un service externe (AWS S3, Cloudinary, etc.) et une librairie comme django-storages.
# Pour l'instant, nous laissons la configuration MEDIA_ROOT pour le développement local.
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuration WhiteNoise
# Utiliser le stockage compressé pour la production (recommandé)
if not DEBUG:
    WHITENOISE_MANIFEST_STRICT = False
    WHITENOISE_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# URL de redirection après une connexion réussie
LOGIN_REDIRECT_URL = '/'

# URL vers laquelle un utilisateur non authentifié est redirigé
LOGIN_URL = 'login'

# URL de redirection après une déconnexion réussie
LOGOUT_REDIRECT_URL = '/'