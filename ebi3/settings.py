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

# ⚠️ CORRECTION CRITIQUE (ALLOWED_HOSTS)
# Liste des hôtes autorisés.
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '::1']

# Configuration spécifique pour Render en mode production (DEBUG=False)
if not DEBUG:
    # Récupère le nom d'hôte externe fourni par Render via la variable d'environnement
    RENDER_HOST = env.str("RENDER_EXTERNAL_HOSTNAME", default="")

    # Ajout du domaine Render et du wildcard '.onrender.com'
    if RENDER_HOST:
        ALLOWED_HOSTS.append(RENDER_HOST)

    # Ajoute le domaine Render pour tous les services sous .onrender.com
    ALLOWED_HOSTS.append('.onrender.com')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Vos applications seront ajoutées ici
    'annonces',
    'whitenoise.runserver_nostatic',  # Recommandé pour le développement local si vous utilisez whitenoise

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
        'DIRS': [BASE_DIR / 'templates'],  # Si vous avez un dossier 'templates' à la racine de votre projet
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
DATABASES = {
    'default': env.db()
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'fr-fr'

TIME_ZONE = 'Europe/Paris'

USE_I18N = True

USE_TZ = True

# --- CONFIGURATION DES FICHIERS STATIQUES ---
STATIC_URL = env("STATIC_URL")
STATIC_ROOT = BASE_DIR / env("STATIC_ROOT")

# ⚠️ CORRECTION N°2 : STATICFILES_DIRS
# Cette ligne est cruciale pour que Django sache où chercher les fichiers statiques
# non associés à une application (ex: fichiers dans votre dossier 'static' à la racine du projet).
# Elle élimine aussi l'avertissement "No directory at: /usr/src/app/staticfiles/".
STATICFILES_DIRS = []
# Si vous avez des fichiers statiques non rattachés à une app (ex: dans un dossier 'static' au même niveau que ebi3/):
# STATICFILES_DIRS = [BASE_DIR / 'static']


# Fichiers médias (images d'annonces, etc.)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuration WhiteNoise
# Utiliser le stockage compressé pour la production (optionnel, mais recommandé)
if not DEBUG:
    WHITENOISE_MANIFEST_STRICT = False
    WHITENOISE_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'