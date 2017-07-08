"""
Tests that migrations are not missing
"""

try:
    from io import StringIO
except ImportError:
    from StringIO import StringIO

import pytest

from django.core.management import call_command


@pytest.mark.django_db
def test_no_missing_migrations():
    """Check no model changes have been made since the last `./manage.py makemigrations`.

    Pulled from mozilla/treeherder #dd53914, subject to MPL
    """
    with pytest.raises(SystemExit) as e:
        # Replace with `check_changes=True` once we're using a Django version that includes:
        # https://code.djangoproject.com/ticket/25604
        # https://github.com/django/django/pull/5453
        call_command('makemigrations', interactive=False, dry_run=True, exit_code=True)
    assert str(e.value) == '1'
