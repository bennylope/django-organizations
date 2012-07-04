from django.test import TestCase
from django.contrib.auth.models import User

from organizations.models import Organization
from organizations.utils import create_organization


class OrgManagerTests(TestCase):

    fixtures = ['users.json', 'orgs.json']

    def test_create_organization(self):
        user = User.objects.get(username="dave")
        acme = create_organization(user, "Acme", "acme")
        self.assertTrue(isinstance(acme, Organization))
        self.assertEqual(user, acme.owner.organization_user.user)
