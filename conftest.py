"""
Configuration file for py.test
"""

import django
import os.path


def pytest_configure():
    from django.conf import settings
    settings.configure(
        DEBUG=True,
        USE_TZ=True,
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": "test.sqlite3",
            }
        },
        INSTALLED_APPS=[
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sites",
            # The ordering here, the apps using the organization base models
            # first and *then* the organizations app itself is an implicit test
            # that the organizations app need not be installed in order to use
            # its base models.
            "test_accounts",
            "test_abstract",
            "test_vendors",
            "organizations",
            "test_custom",
        ],
        MIDDLEWARE_CLASSES=[],
        SITE_ID=1,
        FIXTURE_DIRS=['tests/fixtures'],
        ORGS_SLUGFIELD='django_extensions.db.fields.AutoSlugField',
        ROOT_URLCONF="tests.urls",
        TEMPLATES = [
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'APP_DIRS': True,
            },
        ]
    )
    django.setup()
