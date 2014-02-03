# Django settings for brisket project.
import os

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

TEMPLATE_DEBUG = True

DATABASE_ENGINE = ''           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = ''             # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'
STATIC_URL = '/static/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '(1yv=vnhqrvj%qjr%zd)fe*cr4785a#7$ju8km4%+tnscm&p_r'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'data.middleware.DataRedirectMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'influence.context_processors.custom_context',
    'dryrub.context_processors.custom_context',
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.contrib.messages.context_processors.messages',
)

ROOT_URLCONF = 'brisket.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_ROOT, 'templates')
)

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.sites',
    'django.contrib.humanize', #format numbers in templates
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',
    #'mediasync',
    'brisket.influence',
    'brisket.util',
    'django_nose',
    'indexer',
    'paging',
    'gunicorn',
    'feedinator',
    'compressor',
    'dryrub',
    'data',
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

#DATABASE_ROUTERS = ['db_router.BrisketDBRouter']

# use file-backed sessions while in development. the default location
# for file-backed sessions is tempfile.gettempdir(), most likely /tmp.
# this can be customized with the SESSION_FILE_PATH variable either
# here or in local_settings.py.
SESSION_ENGINE = 'django.contrib.sessions.backends.file'
MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

EMAIL_SUBJECT_PREFIX = '[Brisket] '

FIRST_CYCLE = 1990
LATEST_CYCLE = 2014
TOP_LISTS_CYCLE = 2012

SESSION_COOKIE_NAME = 'brisket_session'

SIMPLEPAY_COMPLETE_REDIRECT = '/postcard/thanks'

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

SELENIUM_HOST = '0.0.0.0'
SELENIUM_PORT = 4444 # default
SELENIUM_BROWSER_COMMAND = 'firefox'
SELENIUM_URL_ROOT = 'http://localhost:8001'
#FORCE_SELENIUM_TESTS = False # default

DOCKETWRENCH_URL = "http://docketwrench.sunlightfoundation.com/"

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# this will get overwritten either in local_settings or below
DEFAULT_CYCLE = None

from local_settings import *

import re
IGNORABLE_404_URLS = (
    re.compile(r'\.php$'),
)

from influenceexplorer import InfluenceExplorer, DEFAULT_CYCLE
api = InfluenceExplorer(API_KEY, AGGREGATES_API_BASE_URL)

if not DEFAULT_CYCLE:
    DEFAULT_CYCLE = ALL_CYCLES
