from django.test import TestCase
from django.contrib.auth.models import User

from organizations.models import Organization


class OrgManagerTests(TestCase):

    fixtures = ['users.json', 'orgs.json']

    def test_active(self):
        self.assertEqual(3, Organization.objects.all().count())
        self.assertEqual(2, Organization.objects.active().count())

    def test_by_user(self):
        user = User.objects.get(username="dave")
        self.assertEqual(2, Organization.objects.get_for_user(user).count())
        self.assertEqual(3, Organization.objects.get_for_user(user).active().count())
