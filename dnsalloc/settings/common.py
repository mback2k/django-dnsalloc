import djcelery
djcelery.setup_loader()

from .base import *
import os

ROOT_URLCONF = 'dnsalloc.urls'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'djcelery',

    'social.apps.django_app.default',
    'social_appengine_auth',

    'dnsalloc.libs.yamlcss',
    'dnsalloc.libs.jdatetime',

    'dnsalloc.apps.dnsalloc',

    'django.contrib.admin',
    'django.contrib.admindocs',

    'compressor',
)

AUTHENTICATION_BACKENDS = (
    'social.backends.google.GoogleOAuth2',
    'social_appengine_auth.backends.GoogleAppEngineOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

LOGIN_BACKEND = 'google-appengine-oauth2'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_ERROR_URL = LOGIN_REDIRECT_URL
LOGIN_URL = '/login/%s/' % LOGIN_BACKEND
LOGOUT_URL = '/logout/?next=%s' % LOGOUT_REDIRECT_URL

CELERY_RESULT_BACKEND = 'djcelery.backends.database.DatabaseBackend'
CELERY_TRACK_STARTED = True
CELERY_SEND_EVENTS = True
CELERY_SEND_TASK_SENT_EVENT = True
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = CELERY_TASK_SERIALIZER
CELERY_ACCEPT_CONTENT = [CELERY_TASK_SERIALIZER]

CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'

SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'social_appengine_auth.pipelines.associate_by_user_id',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details',
)

SOCIAL_AUTH_GOOGLE_OAUTH2_USE_UNIQUE_USER_ID = True
SOCIAL_AUTH_GOOGLE_OAUTH2_AUTH_EXTRA_ARGUMENTS = {'access_type': 'offline', 'approval_prompt': 'force'}

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.environ.get('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY', '')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ.get('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET', '')

SOCIAL_AUTH_GOOGLE_APPENGINE_OAUTH2_USE_UNIQUE_USER_ID = SOCIAL_AUTH_GOOGLE_OAUTH2_USE_UNIQUE_USER_ID

SOCIAL_AUTH_GOOGLE_APPENGINE_OAUTH2_KEY = SOCIAL_AUTH_GOOGLE_OAUTH2_KEY
SOCIAL_AUTH_GOOGLE_APPENGINE_OAUTH2_SECRET = SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'
