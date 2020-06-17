# Third-Party
# Standard Libary
import os

from environ import (
    Env,
    Path,
)

# Django
from django.contrib.messages import constants as messages

# Set Environment
env = Env(
    DEBUG=(bool, False),
    DEFAULT_FROM_EMAIL=(str, 'webmaster@localhost'),
    TIME_ZONE=(str, 'US/Pacific'),
    EMAIL_URL=(str, 'smtp://localhost:1025'),
    REDIS_URL=(str, 'redis://localhost:6379/0'),
)
root = Path(__file__) - 2


# Common
SECRET_KEY = env("SECRET_KEY")
ROOT_URLCONF = 'urls'
WSGI_APPLICATION = 'wsgi.application'
ADMINS = [
    ('admin', env("DEFAULT_FROM_EMAIL")),
]
USE_L10N = True

# Datetime
USE_TZ = True
DATE_FORMAT = 'Y-m-d'
TIME_FORMAT = 'H:i:s'
DATETIME_FORMAT = 'Y-m-d H:i:s'

# Authentication
AUTH_USER_MODEL = 'app.CustomUser'
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'account'
LOGOUT_REDIRECT_URL = 'index'


# Database
DATABASES = {
    'default': env.db()
}

# Cache
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": env("REDIS_URL"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {
                "max_connections": 20,
            },
        }
    },
}


# RQ
RQ_QUEUES = {
    'default': {
        'USE_REDIS_CACHE': 'default',
        'ASYNC': True,
    },
}
RQ_SHOW_ADMIN_LINK = True

# Sessions
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

# Email
EMAIL_CONFIG = env.email_url('EMAIL_URL')
vars().update(EMAIL_CONFIG)

# Mailchimp
MAILCHIMP_API_KEY = env("MAILCHIMP_API_KEY")
MAILCHIMP_AUDIENCE_ID = env("MAILCHIMP_AUDIENCE_ID")

# File Management
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
STATIC_ROOT = root('staticfiles')
MEDIA_ROOT = root('mediafiles')
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATICFILES_DIRS = [
    root('app/static'),
]

# Bootstrap
BOOTSTRAP4 = {
    "css_url": {
        "href": "https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css",
        "integrity": "sha384-9aIt2nRpC12Uk9gS9baDl411NQApFmC26EwAOH8WgZl5MYYxFfc+NcPb1dKGj7Sk",
        "crossorigin": "anonymous",
    },
    "javascript_url": {
        "url": "https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/js/bootstrap.min.js",
        "integrity": "sha384-OgVRvuATP1z7JjHLkuOU7Xw704+h835Lr+6QL9UvYjZE3Ipu6Tp75j7Bh/kR0JKI",
        "crossorigin": "anonymous",
    },
    "jquery_url": {
        "url": "https://code.jquery.com/jquery-3.5.1.min.js",
        "integrity": "sha256-9/aliU8dGd2tb6OSsuzixeV4y/faTqgFtohetphbbj0=",
        "crossorigin": "anonymous",
    },
    "jquery_slim_url": {
        "url": "https://code.jquery.com/jquery-3.5.1.slim.min.js",
        "integrity": "sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj",
        "crossorigin": "anonymous",
    },
    "popper_url": {
        "url": "https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js",
        "integrity": "sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo",
        "crossorigin": "anonymous",
    },
}

# Middleware
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

# Templating
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            root('app/templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
            ],
        },
    },
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_rq',
    'bootstrap4',
    'app',
]
