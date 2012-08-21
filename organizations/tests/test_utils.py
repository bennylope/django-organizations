from django.test import TestCase
from django.contrib.auth.models import User
from django.test.utils import override_settings

from organizations.models import Organization
from organizations.utils import create_organization, model_field_attr


@override_settings(USE_TZ=True)
class OrgManagerTests(TestCase):

    fixtures = ['users.json', 'orgs.json']

    def test_create_organization(self):
        user = User.objects.get(username="dave")
        acme = create_organization(user, "Acme", "acme")
        self.assertTrue(isinstance(acme, Organization))
        self.assertEqual(user, acme.owner.organization_user.user)


class AttributeUtilTests(TestCase):

    def test_present_field(self):
        self.assertTrue(model_field_attr(User, 'username', 'max_length'))

    def test_absent_field(self):
        self.assertRaises(KeyError, model_field_attr, User, 'blahblah',
            'max_length')

    def test_absent_attr(self):
        self.assertRaises(AttributeError, model_field_attr, User, 'username',
            'mariopoints')
