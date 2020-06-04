# Local
from .base import *

# Core
ALLOWED_HOSTS = [
    '.letdistrictsdecide.com',
    '.districtsdecide.com',
    '.herokuapp.com',
]

SECURE_SSL_REDIRECT = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'ERROR',
        },
    },
}
