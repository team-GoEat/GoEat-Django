from pathlib import Path
import os
import json
import sys
from datetime import timedelta
from types import TracebackType
import firebase_admin
from firebase_admin import credentials
import pymysql

pymysql.install_as_MySQLdb()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

ROOT_DIR = os.path.dirname(BASE_DIR)

SECRET_BASE_FILE = os.path.join(BASE_DIR, 'secrets.json')

# SECRET_KEY = '_8fp6^rssql@$81(z3b17_=vo3ayy^1dajsgtsco^6m+2%84x^'
cred_path = os.path.join(BASE_DIR, "serviceAccountKey.json")
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)

secrets = json.loads(open(SECRET_BASE_FILE).read())
for key, value in secrets.items():
    setattr(sys.modules[__name__], key, value)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
if os.environ.get('DJANGO_DEBUG', False):
    DEBUG = False
else:
    DEBUG = True

if DEBUG:
    ALLOWED_HOSTS = ['*']
else:
    ALLOWED_HOSTS = ['goeat.kr']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.humanize',
    # 'django_extensions',

    'restaurant',
    'notice',
    'accounts',

    #django-rest-framework
    'rest_framework',
    'django_hosts',
    'app_owner',
    'rest_framework_simplejwt.token_blacklist',
    # django-allauth
    'allauth',
    'allauth.account',
]

AUTH_USER_MODEL = 'accounts.User'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
        # 'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

ACCOUNT_AUTHENTICATION_METHOD = 'username'
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_USER_MODEL_USERNAME_FIELD = 'username'

#JWT
REST_USE_JWT = True
JWT_AUTH_COOKIE = 'my-app-auth'

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=2),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=365),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
}

MIDDLEWARE = [
    'django_hosts.middleware.HostsRequestMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_hosts.middleware.HostsResponseMiddleware',
    'app_owner.middleware.login_session.session_check',
]

####### HOSTS SETTING ( 변경 금지 )
ROOT_HOSTCONF = 'goeat.hosts'
ROOT_URLCONF = 'goeat.urls'
DEFAULT_HOST = 'www'

if DEBUG:
    PARENT_HOST = 'test.me:8000'
else:
    PARENT_HOST = 'goeat.kr'

SITE_ID = 1

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'goeat.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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

if not DEBUG:
    LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'django.server': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[{server_time}] {message}',
            'style': '{',
        },
        'verbose': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'django.server': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'django.server',
        },
        'error_file': {
            'level': 'INFO',
            'filters': ['require_debug_false'],
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR /'logs/goeat_error.log',
            'maxBytes': 1024*1024*5,  # 5 MB
            'backupCount': 5,
            'formatter': 'verbose', 
        },
        'collect_file': {
            'level': 'INFO',
            'filters': ['require_debug_false'],
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': BASE_DIR/'logs/collection/data.log',
            'formatter': 'verbose',
            'when': 'midnight',
        },
        'sql_test_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filters': ['require_debug_true'],
            'filename': BASE_DIR /'logs/sql_test.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'error_file'],
            'level': 'INFO',
        },
        'django.server': {
            'handlers': ['django.server'],
            'level': 'INFO',
            'propagate': False,
        },
        'collection': {
            'handlers': ['console', 'collect_file'],
            'level': 'INFO',
        },
        'django.db.backends': {
            'handlers': ['sql_test_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'ko'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# owner static version
VERSION = 1.0

# owner Json Result
RESULT = {
    'result': 'fail',
    'msg': '',
    'value': []
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = ''
STATICFILES_DIRS = (os.path.join('static'), )
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# 레스토랑 요일별 기본 데이터
RES_DAYS = {
    'week_0':{
        'name':'월요일',
        'state':False
    },
    'week_1':{
        'name':'화요일',
        'state':False
    },
    'week_2':{
        'name':'수요일',
        'state':False
    },
    'week_3':{
        'name':'목요일',
        'state':False
    },
    'week_4':{
        'name':'금요일',
        'state':False
    },
    'week_5':{
        'name':'토요일',
        'state':False
    },
    'week_6':{
        'name':'일요일',
        'state':False
    }
}