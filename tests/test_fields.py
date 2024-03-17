"""
Tests for configurable fields
"""

import importlib

from django.core.exceptions import ImproperlyConfigured

import pytest

from organizations import fields


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
