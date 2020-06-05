# Third-Party
# Standard Libary
import os

# Django
from django.contrib.messages import constants as messages
# First-Party
from environ import Env, Path

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

# Datetime
USE_TZ = True
DATE_FORMAT = 'Y-m-d'
TIME_FORMAT = 'H:i:s'
DATETIME_FORMAT = 'Y-m-d H:i:s'

# Authentication
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]
LOGIN_URL = 'admin:login'
LOGIN_REDIRECT_URL = 'admin:index'
LOGOUT_REDIRECT_URL = 'admin:login'


# Database
DATABASES = {
    'default': env.db()
}

# Redis
RQ_QUEUES = {
    'default': {
        'URL': env("REDIS_URL"),
    },
}
RQ_SHOW_ADMIN_LINK = True

# Email
EMAIL_CONFIG = env.email_url('EMAIL_URL')
vars().update(EMAIL_CONFIG)

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
MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
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
    'app',
]
