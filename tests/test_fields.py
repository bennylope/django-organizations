# -*- coding: utf-8 -*-

"""
Tests for configurable fields
"""
import importlib

import pytest
from django.core.exceptions import ImproperlyConfigured

from organizations import fields

pytestmark = pytest.mark.django_db


def test_misconfigured_autoslug_cannot_import(settings):
    settings.ORGS_SLUGFIELD = "not.AModel"
    with pytest.raises(ImproperlyConfigured):
        importlib.reload(fields)


def test_misconfigured_autoslug_incorrect_class(settings):
    settings.ORGS_SLUGFIELD = "autoslug.AutoSlug"
    with pytest.raises(ImproperlyConfigured):
        importlib.reload(fields)


def test_misconfigured_autoslug_bad_notation(settings):
    settings.ORGS_SLUGFIELD = "autoslug.AutoSlugField"
    importlib.reload(fields)
