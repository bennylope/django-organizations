"""
Tests that migrations are not missing
"""

import pytest

from django.core.management import call_command


@pytest.mark.django_db
def test_no_missing_migrations():
    """Check no model changes have been made since the last `./manage.py makemigrations`.
    """
    call_command('makemigrations', check=True, dry_run=True)
