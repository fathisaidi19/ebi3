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

# ⚠️ CORRECTION N°1 : ALLOWED_HOSTS
# On ne met pas ALLOWED_HOSTS en dur ici. On le gère via la variable d'environnement ou la logique ci-dessous.
# Si DEBUG=True, on permet l'accès local.
if DEBUG:
    ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '::1', '.render.com']
else:
    # En production, on utilise la logique Render recommandée.
    # L'adresse Render 'ebi3-jii8.onrender.com' sera automatiquement acceptée
    # via la configuration des ALLOWED_HOSTS.
    ALLOWED_HOSTS = ['ebi3-jii8.onrender.com', '.render.com']


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
        'DIRS': [BASE_DIR / 'templates'], # Si vous avez un dossier 'templates' à la racine de votre projet
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

# ⚠️ CORRECTION N°2 : Ajout de STATICFILES_DIRS
# Permet à Django de trouver les fichiers statiques qui ne sont pas dans une application spécifique (ex: un dossier 'static' à la racine du projet).
# Si vous n'avez pas de dossier 'static' à la racine, vous pouvez laisser la liste vide.
STATICFILES_DIRS = []
# Exemple si vous avez un dossier 'static' à la racine :
# STATICFILES_DIRS = [BASE_DIR / 'static']

# Fichiers médias (images d'annonces, etc.)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuration WhiteNoise pour la compression des statiques (optionnel, mais recommandé)
# Desactivez si vous utilisez un CDN
# WHITENOISE_MANIFEST_STRICT = False
# WHITENOISE_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'