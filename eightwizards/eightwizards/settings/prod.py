from .base import *
from os import environ


DEBUG = TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': environ.get('DB_NAME', 'eightwizards'),
        'USER': environ.get('DB_USER', 'root'),
        'PASSWORD': environ.get('DB_PASSWORD', ''),
        'HOST': environ.get('DB_HOST', 'localhost'),
        'PORT': environ.get('DB_PORT', '3306'),
    }
}

CONN_MAX_AGE = 8
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379