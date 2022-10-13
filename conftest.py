"""
Configuration file for py.test
"""

import django
import pytest


def pytest_configure():
    from django.conf import settings

    settings.configure(
        DEBUG=True,
        USE_TZ=True,
        DATABASES={
            "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": "test.sqlite3"}
        },
        INSTALLED_APPS=[
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sites",
            "django.contrib.admin",
            "django.contrib.sessions",
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
        MIDDLEWARE=[
            "django.middleware.security.SecurityMiddleware",
            "django.contrib.sessions.middleware.SessionMiddleware",
            "django.middleware.common.CommonMiddleware",
            "django.middleware.csrf.CsrfViewMiddleware",
            "django.contrib.auth.middleware.AuthenticationMiddleware",
            "django.contrib.messages.middleware.MessageMiddleware",
            "django.middleware.clickjacking.XFrameOptionsMiddleware",
        ],
        TEMPLATES=[
            {
                "BACKEND": "django.template.backends.django.DjangoTemplates",
                "APP_DIRS": True,
                "OPTIONS": {
                    "context_processors": [
                        "django.contrib.auth.context_processors.auth",
                        "django.template.context_processors.debug",
                        "django.template.context_processors.i18n",
                        "django.template.context_processors.media",
                        "django.template.context_processors.static",
                        "django.template.context_processors.request",
                        "django.contrib.messages.context_processors.messages",
                    ],
                    "debug": True,
                },
            }
        ],
        SITE_ID=1,
        FIXTURE_DIRS=["tests/fixtures"],
        ORGS_SLUGFIELD="django_extensions.db.fields.AutoSlugField",
        ROOT_URLCONF="tests.urls",
        STATIC_URL="/static/",
        SECRET_KEY="ThisIsHorriblyInsecure",
    )
    django.setup()

@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass
