"""
Configuration file for py.test
"""

import django


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
            "test_vendors",
            "organizations",
            "test_custom",
        ],
        MIDDLEWARE_CLASSES=(),  # Silence Django 1.7 warnings
        SITE_ID=1,
        FIXTURE_DIRS=['tests/fixtures'],
        ORGS_TIMESTAMPED_MODEL='django_extensions.db.models.TimeStampedModel',
        ROOT_URLCONF="tests.urls",
    )
    django.setup()
