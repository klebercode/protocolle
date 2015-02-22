# coding: utf-8
"""
Django settings for protocolle project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# import os
# BASE_DIR = os.path.dirname(os.path.dirname(__file__))
from decouple import config
from dj_database_url import parse as db_url
from unipath import Path
BASE_DIR = Path(__file__).parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = [
    '.localhost',
    '127.0.0.1',
    '.herokuapp.com',
    '.ow7.com.br',
    '.protocolle.com',
    '.protocolo.com',
]


# Application definition

SHARED_APPS = (
    'tenant_schemas',  # mandatory
    'customers',  # you must list the app where your tenant model resides in

    'grappelli_extensions',
    'grappelli.dashboard',
    'grappelli',
    # 'filebrowser',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'flexselect',
    'autocomplete_light',
    'storages',

    # your tenant-specific apps
    'protocolle.core',
    'protocolle.auxiliar',
    'protocolle.protocolo',
)

TENANT_APPS = (
    # The following Django contrib apps must be in TENANT_APPS
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # your tenant-specific apps
    'protocolle.core',
    'protocolle.auxiliar',
    'protocolle.protocolo',
)

INSTALLED_APPS = SHARED_APPS + TENANT_APPS

TENANT_MODEL = "customers.Client"

MIDDLEWARE_CLASSES = (
    'tenant_schemas.middleware.TenantMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'protocolle.current_user.CurrentUserMiddleware',
)

# Template context
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
)

ROOT_URLCONF = 'protocolle.urls'

WSGI_APPLICATION = 'protocolle.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

# import dj_database_url

# DATABASES = {}
# DATABASES['default'] = dj_database_url.config(
#     default='postgres://postgres:123@localhost/protocolle')
# DATABASES['default']['ENGINE'] = 'tenant_schemas.postgresql_backend'

DATABASES = {
    'default': config(
        'DATABASE_URL',
        default='postgres://postgres:123@localhost/protocolle',
        cast=db_url),
}
DATABASES['default']['ENGINE'] = 'tenant_schemas.postgresql_backend'


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Recife'

USE_I18N = True

USE_L10N = True

USE_TZ = True


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# DEFAULT_FROM_EMAIL = 'Polpa Canaa <no-reply@polpacanaa.com.br>'
# EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=False, cast=bool)
# EMAIL_PORT = config('EMAIL_PORT', default=25, cast=int)
# EMAIL_HOST = config('EMAIL_HOST', default='localhost')
# EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
# EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')


# Templates
TEMPLATE_DIRS = (
    BASE_DIR.child('core', 'templates'),
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

# Grappelli settings
GRAPPELLI_EXTENSIONS_NAVBAR = 'protocolle.extensions.Navbar'

# GRAPPELLI_EXTENSIONS_SIDEBAR = 'protocolle.extensions.Sidebar'

GRAPPELLI_INDEX_DASHBOARD = 'protocolle.dashboard.CustomIndexDashboard'

GRAPPELLI_AUTOCOMPLETE_SEARCH_FIELDS = {
    "auxiliar": {
        "instituicao": ("nome__icontains",),
        "setor": ("nome__icontains",),
        "pessoa": ("nome__icontains",),
    },
    # "protocolo": {
    #     "documento": ("protocolo__icontains",),
    # },
}

GRAPPELLI_ADMIN_TITLE = 'Protocolle'

FLEXSELECT = {
    'include_jquery': True,
}

AUTH_PROFILE_MODULE = 'auxiliar.Instituicao_User'


# Amazon S3 settings
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
# os.environ['AWS_STORAGE_BUCKET_NAME']
AWS_STORAGE_BUCKET_NAME = 'ow7-protocolle'
# os.environ['AWS_ACCESS_KEY_ID']
AWS_ACCESS_KEY_ID = 'AKIAJNKUAC3QKH3MWSNQ'
# os.environ['AWS_SECRET_ACCESS_KEY']
AWS_SECRET_ACCESS_KEY = '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'

# STATICFILES_STORAGE = 'protocolle.s3utils.StaticRootS3BotoStorage'

# STATIC_ROOT = BASE_DIR.child('staticfiles')

# STATIC_URL = 'http://protocolle.s3-website-us-west-1.amazonaws.com/static/'

DEFAULT_FILE_STORAGE = 'protocolle.s3utils.MediaRootS3BotoStorage'

MEDIA_ROOT = BASE_DIR.child('media')

MEDIA_URL = 'http://ow7-protocolle.s3-website-us-west-1.amazonaws.com/media/'


STATIC_ROOT = BASE_DIR.child('staticfiles')
STATIC_URL = '/static/'

# MEDIA_ROOT = BASE_DIR.child('media')
# MEDIA_URL = '/media/'
