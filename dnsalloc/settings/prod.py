from .common import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    (os.environ.pop('ADMIN', ''), os.environ.pop('ADMIN_EMAIL', '')),
)
MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.pop('MYSQL_DATABASE', ''),
        'USER': os.environ.pop('MYSQL_USERNAME', ''),
        'PASSWORD': os.environ.pop('MYSQL_PASSWORD', ''),
        'HOST': '',
        'PORT': '',
        'OPTIONS': {
            'init_command': 'SET storage_engine=INNODB; SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;',
        }
    }
}

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.cache.RedisCache',
        'LOCATION': os.environ.pop('REDIS_CACHE_BACKEND', ''),
    }
}

BROKER_URL = os.environ.pop('REDIS_CELERY_BACKEND', '')
CELERY_RESULT_BACKEND = BROKER_URL

ALLOWED_HOSTS = [os.environ.pop('SERVER', '')]
DEFAULT_FROM_EMAIL = os.environ.pop('SERVER_EMAIL', '')

SECRET_KEY = os.environ.pop('SECRET_KEY', None)

GOOGLE_APPENGINE_CONSUMER_KEY = os.environ.pop('GOOGLE_APPENGINE_CONSUMER_KEY', None)
GOOGLE_APPENGINE_CONSUMER_SECRET = os.environ.pop('GOOGLE_APPENGINE_CONSUMER_SECRET', None)

GOOGLE_OAUTH2_CLIENT_ID = os.environ.pop('GOOGLE_OAUTH2_CLIENT_ID', None)
GOOGLE_OAUTH2_CLIENT_SECRET = os.environ.pop('GOOGLE_OAUTH2_CLIENT_SECRET', None)
