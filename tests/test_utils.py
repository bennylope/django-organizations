from functools import partial

from django.test import TestCase
from django.contrib.auth.models import User
from django.test.utils import override_settings

from organizations.models import Organization
from organizations.utils import create_organization, model_field_attr
from test_accounts.models import Account
from test_abstract.models import CustomOrganization


@override_settings(USE_TZ=True)
class CreateOrgTests(TestCase):

    fixtures = ['users.json', 'orgs.json']

    def setUp(self):
        self.user = User.objects.get(username="dave")

    def test_create_organization(self):
        acme = create_organization(self.user, "Acme", org_defaults={"slug": "acme-slug"})
        self.assertTrue(isinstance(acme, Organization))
        self.assertEqual(self.user, acme.owner.organization_user.user)
        self.assertTrue(acme.owner.organization_user.is_admin)

    def test_create_custom_org(self):
        custom = create_organization(self.user, "Custom", model=Account)
        self.assertTrue(isinstance(custom, Account))
        self.assertEqual(self.user, custom.owner.organization_user.user)

    def test_create_custom_org_from_abstract(self):
        custom = create_organization(self.user, "Custom", model=CustomOrganization)
        self.assertTrue(isinstance(custom, CustomOrganization))
        self.assertEqual(self.user, custom.owner.organization_user.user)

    def test_defaults(self):
        """Ensure models are created with defaults as specified"""
        # Default models
        org = create_organization(self.user, "Is Admin",
                org_defaults={"slug": "is-admin-212", "is_active": False},
                org_user_defaults={"is_admin": False})
        self.assertFalse(org.is_active)
        self.assertFalse(org.owner.organization_user.is_admin)

        # Custom models
        create_account = partial(create_organization, model=Account,
                org_defaults={'monthly_subscription': 99},
                org_user_defaults={'user_type': 'B'})
        myaccount = create_account(self.user, name="My New Account")
        self.assertEqual(myaccount.monthly_subscription, 99)

    def test_backwards_compat(self):
        """Ensure old optional arguments still work"""
        org = create_organization(self.user, "Is Admin", "my-slug", is_active=False)
        self.assertFalse(org.is_active)

        custom = create_organization(self.user, "Custom org", org_model=Account)
        self.assertTrue(isinstance(custom, Account))


class AttributeUtilTests(TestCase):

    def test_present_field(self):
        self.assertTrue(model_field_attr(User, 'username', 'max_length'))

    def test_absent_field(self):
        self.assertRaises(KeyError, model_field_attr, User, 'blahblah',
            'max_length')

    def test_absent_attr(self):
        self.assertRaises(AttributeError, model_field_attr, User, 'username',
            'mariopoints')
