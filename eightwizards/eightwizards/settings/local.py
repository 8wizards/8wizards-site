from .base import *
from os import environ

DEBUG = TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'eightwizards',
        'USER': 'root',
        'PASSWORD': '123asd3d',
        'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    }
}

CONN_MAX_AGE = 8
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379

EMAIL_HOST_USER = environ.get('EMAIL_HOST_USER', 'eightwizards'),
EMAIL_HOST_PASSWORD = environ.get('EMAIL_HOST_PASSWORD', 'password')
