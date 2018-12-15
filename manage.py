#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Management command entry point for working with migrations
"""

import os
import sys
import django
from django.conf import settings


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.admin",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
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
]

settings.configure(
    DEBUG=True,
    USE_TZ=True,
    DATABASES={
        "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": "test.sqlite3"}
    },
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
    ORGS_SLUGFIELD="autoslugged.AutoSlugField",
    INSTALLED_APPS=INSTALLED_APPS,
    ROOT_URLCONF="tests.urls",
    # STATIC_URL='/static/',
    # STATIC_ROOT=os.path.join(BASE_DIR),
    # STATICFILES_DIRS = [
    #     os.path.join(BASE_DIR, "static"),
    # ],
    # SESSION_ENGINE='django.contrib.sessions.backends.db',
)

django.setup()


if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
