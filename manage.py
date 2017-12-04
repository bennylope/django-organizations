#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Management command entry point for working with migrations
"""

import sys
import django
from django.conf import settings

INSTALLED_APPS = [
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
]

settings.configure(
    DEBUG=True,
    USE_TZ=True,
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": "test.sqlite3",
        }
    },
    MIDDLEWARE_CLASSES=(),  # Silence Django 1.7 warnings
    SITE_ID=1,
    FIXTURE_DIRS=['tests/fixtures'],
    ORGS_SLUGFIELD='django_extensions.db.fields.AutoSlugField',
    INSTALLED_APPS=INSTALLED_APPS,
    ROOT_URLCONF="tests.urls",
)

django.setup()


if __name__ == '__main__':
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
