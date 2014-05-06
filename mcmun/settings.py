"""
Django settings for ssuns_2014 project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

import django.conf.global_settings as DEFAULT_SETTINGS
import djcelery
import logging
import os
from mcmun import conf

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DEBUG = conf.DEBUG
TEMPLATE_DEBUG = DEBUG

INTERNAL_IPS = (
    '127.0.0.1',
)

ALLOWED_HOSTS = conf.ALLOWED_HOSTS

ADMINS = (
    ('lh', 'it@ssuns.org'),
)

ADMIN_URL = 'http://www.ssuns.org/%s/' % conf.ADMIN_PREFIX
MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': conf.DB_ENGINE,
        'NAME': conf.DB_NAME,
        'USER': conf.DB_USER,
        'PASSWORD': conf.DB_PASSWORD,
        'HOST': conf.DB_HOST,
        'PORT': conf.DB_PORT,
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = None

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = conf.MEDIA_ROOT

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = conf.STATIC_ROOT

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'



# Make this unique, and don't share it with anybody.
SECRET_KEY = conf.SECRET_KEY

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'cms.context_processors.menu',
    'committees.context_processors.committees',
)


ROOT_URLCONF = 'mcmun.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'mcmun.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.markup',
    'djcelery',
    'djcelery.transport',
    'mcmun',
    'committees',
    'cms',
    'signups',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'it@ssuns.org'
EMAIL_HOST_PASSWORD = conf.EMAIL_PASSWORD

IT_EMAIL = 'it@ssuns.org'
CHARGE_EMAIL = 'schools@ssuns.org'
FINANCE_EMAIL = 'finance@ssuns.org'
CSRF_COOKIE_DOMAIN = conf.COOKIE_DOMAIN
DEFAULT_FROM_EMAIL = 'it@ssuns.org'
logging.getLogger('xhtml2pdf')

djcelery.setup_loader()
BROKER_URL = 'django://'
CELERY_RESULT_BACKEND = "database"
CELERY_RESULT_DBURI = "sqlite:///db.sqlite"

LOGIN_URL = '/login'
LOGOUT_URL = '/logout'
LOGIN_REDIRECT_URL = '/dashboard'
