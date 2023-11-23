"""
Tests that migrations are not missing
"""

from django.core.management import call_command

import pytest


@pytest.mark.django_db
def test_no_missing_migrations():
    """Verify that no changes are detected in the migrations."""
    call_command("makemigrations", check=True, dry_run=True)
