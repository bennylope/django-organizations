from os.path import dirname, join


TEST_ROOT = dirname(__file__)

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.auth',
    'django.contrib.sessions',
    'organizations',
    'tests',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'dev.db',
    }
}

DATABASE_ENGINE = 'sqlite3' # older Django versions

SITE_ID = 1

MEDIA_URL = '/media/'
MEDIA_ROOT = join(TEST_ROOT, 'media')

STATIC_URL = '/static/'
STATIC_ROOT = MEDIA_ROOT

ROOT_URLCONF = 'tests.urls'

#TEMPLATE_DIRS = (join(TEST_ROOT, 'templates'),)

