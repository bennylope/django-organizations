# -*- coding: utf-8 -*-

from functools import partial

from django.contrib.auth.models import User
from django.db import IntegrityError
from django.test import TestCase
from django.test.utils import override_settings

from organizations.models import Organization
from organizations.models import OrganizationInvitation
from organizations.models import OrganizationOwner
from organizations.models import OrganizationUser
from organizations.utils import create_organization
from test_abstract.models import CustomOrganization
from test_accounts.models import Account
from test_accounts.models import AccountInvitation
from test_custom.models import Team


@override_settings(USE_TZ=True)
class ActiveManagerTests(TestCase):

    fixtures = ["users.json", "orgs.json"]

    def test_active(self):
        self.assertEqual(3, Organization.objects.all().count())
        self.assertEqual(2, Organization.active.all().count())

    def test_by_user(self):
        user = User.objects.get(username="dave")
        self.assertEqual(3, Organization.objects.get_for_user(user).count())
        self.assertEqual(2, Organization.active.get_for_user(user).count())


@override_settings(USE_TZ=True)
class OrgModelTests(TestCase):

    fixtures = ["users.json", "orgs.json"]

    def setUp(self):
        self.kurt = User.objects.get(username="kurt")
        self.dave = User.objects.get(username="dave")
        self.krist = User.objects.get(username="krist")
        self.duder = User.objects.get(username="duder")
        self.nirvana = Organization.objects.get(name="Nirvana")
        self.foo = Organization.objects.get(name="Foo Fighters")

    def test_invitation_model(self):
        assert Organization.invitation_model == OrganizationInvitation

    def test_org_string_representation(self):
        """Ensure that models' string representation are error free"""
        self.foo.name = "Föö Fíghterß"
        self.assertTrue("{0}".format(self.foo))
        self.assertTrue("{0}".format(self.foo.owner))
        self.assertTrue("{0}".format(self.foo.owner.organization_user))

    def test_relation_name(self):
        """Ensure user-related name is accessible from common attribute"""
        self.assertEqual(self.foo.user_relation_name, "organizations_organization")

    def test_duplicate_members(self):
        """Ensure that a User can only have one OrganizationUser object"""
        self.assertRaises(IntegrityError, self.nirvana.add_user, self.dave)

    def test_is_member(self):
        self.assertTrue(self.nirvana.is_member(self.kurt))
        self.assertTrue(self.nirvana.is_member(self.dave))
        self.assertTrue(self.foo.is_member(self.dave))
        self.assertFalse(self.foo.is_member(self.kurt))

    def test_is_admin(self):
        self.assertTrue(self.nirvana.is_admin(self.kurt))
        self.assertTrue(self.nirvana.is_admin(self.krist))
        self.assertFalse(self.nirvana.is_admin(self.dave))
        self.assertTrue(self.foo.is_admin(self.dave))

    def test_is_owner(self):
        self.assertTrue(self.nirvana.is_owner(self.kurt))
        self.assertTrue(self.foo.is_owner(self.dave))
        self.assertFalse(self.nirvana.is_owner(self.dave))
        self.assertFalse(self.nirvana.is_owner(self.krist))

    def test_add_user(self):
        new_guy = self.foo.add_user(self.krist)
        self.assertTrue(isinstance(new_guy, OrganizationUser))
        self.assertEqual(new_guy.organization, self.foo)

    def test_remove_user(self):
        new_guy = self.foo.add_user(self.krist)
        self.foo.remove_user(self.krist)
        self.assertFalse(self.foo.users.filter(pk=self.krist.pk).exists())

    def test_get_or_add_user(self):
        """Ensure `get_or_add_user` adds a user IFF it exists"""
        new_guy, created = self.foo.get_or_add_user(self.duder)
        self.assertTrue(isinstance(new_guy, OrganizationUser))
        self.assertEqual(new_guy.organization, self.foo)
        self.assertTrue(created)

        new_guy, created = self.foo.get_or_add_user(self.dave)
        self.assertTrue(isinstance(new_guy, OrganizationUser))
        self.assertFalse(created)

    def test_delete_owner(self):
        from organizations.exceptions import OwnershipRequired

        owner = self.nirvana.owner.organization_user
        self.assertRaises(OwnershipRequired, owner.delete)

    def test_change_owner(self):
        admin = self.nirvana.organization_users.get(user__username="krist")
        self.nirvana.change_owner(admin)
        owner = self.nirvana.owner.organization_user
        self.assertEqual(owner, admin)

    def test_delete_missing_owner(self):
        """Ensure an org user can be deleted when there is no owner"""
        org = Organization.objects.create(name="Some test", slug="some-test")
        # Avoid the Organization.add_user method which would make an owner
        org_user = OrganizationUser.objects.create(user=self.kurt, organization=org)
        # Just make sure it doesn't raise an error
        org_user.delete()

    def test_nonmember_owner(self):
        from organizations.exceptions import OrganizationMismatch

        foo_user = self.foo.owner
        self.nirvana.owner = foo_user
        self.assertRaises(OrganizationMismatch, self.nirvana.owner.save)


@override_settings(USE_TZ=True)
class OrgDeleteTests(TestCase):

    fixtures = ["users.json", "orgs.json"]

    def test_delete_account(self):
        """Ensure Users are not deleted on the cascade"""
        self.assertEqual(3, OrganizationOwner.objects.all().count())
        self.assertEqual(4, User.objects.all().count())
        scream = Organization.objects.get(name="Scream")
        scream.delete()
        self.assertEqual(2, OrganizationOwner.objects.all().count())
        self.assertEqual(4, User.objects.all().count())

    def test_delete_orguser(self):
        """Ensure the user is not deleted on the cascade"""
        krist = User.objects.get(username="krist")
        org_user = OrganizationUser.objects.filter(
            organization__name="Nirvana", user=krist
        )
        org_user.delete()
        self.assertTrue(krist.pk)


class CustomModelTests(TestCase):

    # Load the world as we know it.
    fixtures = ["users.json", "orgs.json"]

    def setUp(self):
        self.kurt = User.objects.get(username="kurt")
        self.dave = User.objects.get(username="dave")
        self.krist = User.objects.get(username="krist")
        self.duder = User.objects.get(username="duder")
        self.red_account = Account.objects.create(
            name="Red Account", monthly_subscription=1200
        )

    def test_invitation_model(self):
        assert Account.invitation_model == AccountInvitation

    def test_org_string(self):
        self.assertEqual(self.red_account.__str__(), "Red Account")

    def test_relation_name(self):
        """Ensure user-related name is accessible from common attribute"""
        self.assertEqual(self.red_account.user_relation_name, "test_accounts_account")

    def test_change_user(self):
        """Ensure custom organizations validate in owner change"""
        create_team = partial(create_organization, model=Team)
        hometeam = create_team(self.dave, "Hometeam")
        duder_org_user = hometeam.add_user(self.duder)
        hometeam.owner.organization_user = duder_org_user
        hometeam.owner.save()

    def test_abstract_change_user(self):
        """
        Ensure custom organizations inheriting abstract model
        validate in owner change
        """
        create_org = partial(create_organization, model=CustomOrganization)
        org1 = create_org(self.dave, "Org1")
        duder_org_user = org1.add_user(self.duder)
        org1.owner.organization_user = duder_org_user
        org1.owner.save()
