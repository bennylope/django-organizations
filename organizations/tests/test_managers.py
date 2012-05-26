from django.test import TestCase
from django.contrib.auth.models import User

from organizations.managers import OrganizationManager



class OrgManagerTests(TestCase):

    fixtures = ['users.json', 'orgs.json']

    def test_nada(self):
        self.assertFalse(True)

    def test_setup(self):
        self.assertEqual(3, User.objects.all().count())
