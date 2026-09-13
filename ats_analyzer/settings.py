from pathlib import Path
import os

import dj_database_url


# ==========================================
# BASE DIRECTORY
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent


# ==========================================
# SECURITY
# ==========================================

SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'django-insecure-change-this'
)

DEBUG = (
    os.environ.get(
        'DEBUG',
        'False'
    ).lower()
    == 'true'
)


ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '.vercel.app',
]


# ==========================================
# APPLICATIONS
# ==========================================

INSTALLED_APPS = [

    'django.contrib.admin',

    'django.contrib.auth',

    'django.contrib.contenttypes',

    'django.contrib.sessions',

    'django.contrib.messages',

    'django.contrib.staticfiles',

    'analyzer',

]


# ==========================================
# MIDDLEWARE
# ==========================================

MIDDLEWARE = [

    'django.middleware.security.SecurityMiddleware',

    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.common.CommonMiddleware',

    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',

    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]


# ==========================================
# URLS
# ==========================================

ROOT_URLCONF = 'ats_analyzer.urls'


# ==========================================
# TEMPLATES
# ==========================================

TEMPLATES = [

    {
        'BACKEND':
            'django.template.backends.django.DjangoTemplates',

        'DIRS': [
            BASE_DIR / 'templates'
        ],

        'APP_DIRS':
            True,

        'OPTIONS': {

            'context_processors': [

                'django.template.context_processors.request',

                'django.contrib.auth.context_processors.auth',

                'django.contrib.messages.context_processors.messages',

            ],

        },

    },

]


# ==========================================
# WSGI
# ==========================================

WSGI_APPLICATION = 'ats_analyzer.wsgi.application'


# ==========================================
# DATABASE
# ==========================================

DATABASE_URL = (
    os.environ.get(
        'DATABASE_URL',
        ''
    )
    .strip()
    .strip('"')
    .strip("'")
)


if DATABASE_URL:

    DATABASES = {

        'default': dj_database_url.parse(

            DATABASE_URL,

            conn_max_age=0,

            ssl_require=True

        )

    }

else:

    # Local development only
    DATABASES = {

        'default': {

            'ENGINE':
                'django.db.backends.sqlite3',

            'NAME':
                BASE_DIR / 'db.sqlite3',

        }

    }


# ==========================================
# STATIC FILES
# ==========================================

STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR / 'staticfiles'


STORAGES = {

    'default': {

        # IMPORTANT:
        # No uploaded resume is stored here.
        # Resume files are processed temporarily.
        'BACKEND':
            'django.core.files.storage.FileSystemStorage',

    },

    'staticfiles': {

        'BACKEND':
            'whitenoise.storage.CompressedManifestStaticFilesStorage',

    },

}


# ==========================================
# MEDIA
# ==========================================

MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'media'


# ==========================================
# DJANGO
# ==========================================

DEFAULT_AUTO_FIELD = (
    'django.db.models.BigAutoField'
)


# ==========================================
# AUTHENTICATION
# ==========================================

LOGIN_URL = '/accounts/login/'

LOGIN_REDIRECT_URL = '/dashboard/'

LOGOUT_REDIRECT_URL = '/'


# ==========================================
# VERCEL / CSRF
# ==========================================

CSRF_TRUSTED_ORIGINS = [
    'https://*.vercel.app'
]


SECURE_PROXY_SSL_HEADER = (
    'HTTP_X_FORWARDED_PROTO',
    'https'
)


USE_X_FORWARDED_HOST = True


# ==========================================
# GEMINI
# ==========================================

GEMINI_API_KEY = (
    os.environ.get(
        'GEMINI_API_KEY',
        ''
    ).strip()
)


GEMINI_MODEL = (
    os.environ.get(
        'GEMINI_MODEL',
        'gemini-2.5-flash'
    ).strip()
)


# ==========================================
# PRODUCTION SECURITY
# ==========================================

if not DEBUG:

    SESSION_COOKIE_SECURE = True

    CSRF_COOKIE_SECURE = True

    SECURE_CONTENT_TYPE_NOSNIFF = True

    X_FRAME_OPTIONS = 'DENY'
