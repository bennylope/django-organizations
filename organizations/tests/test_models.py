from django.test import TestCase
from django.test.utils import override_settings
from django.contrib.auth.models import User
from django.db import IntegrityError

from organizations.models import (Organization, OrganizationUser,
        OrganizationOwner)


@override_settings(USE_TZ=True)
class ActiveManagerTests(TestCase):

    fixtures = ['users.json', 'orgs.json']

    def test_active(self):
        self.assertEqual(3, Organization.objects.all().count())
        self.assertEqual(2, Organization.active.all().count())

    def test_by_user(self):
        user = User.objects.get(username="dave")
        self.assertEqual(3, Organization.objects.get_for_user(user).count())
        self.assertEqual(2, Organization.active.get_for_user(user).count())


@override_settings(USE_TZ=True)
class OrgModelTests(TestCase):

    fixtures = ['users.json', 'orgs.json']

    def setUp(self):
        self.kurt = User.objects.get(username="kurt")
        self.dave = User.objects.get(username="dave")
        self.krist = User.objects.get(username="krist")
        self.duder = User.objects.get(username="duder")
        self.nirvana = Organization.objects.get(name="Nirvana")
        self.foo = Organization.objects.get(name="Foo Fighters")

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

    def test_add_user(self):
        new_guy = self.foo.add_user(self.krist)
        self.assertTrue(isinstance(new_guy, OrganizationUser))
        self.assertEqual(new_guy.organization, self.foo)

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

    def test_delete_missing_owner(self):
        """Ensure an org user can be deleted when there is no owner"""
        org = Organization.objects.create(name="Some test", slug="some-test")
        # Avoid the Organization.add_user method which would make an owner
        org_user = OrganizationUser.objects.create(user=self.kurt,
                organization=org)
        # Just make sure it doesn't raise an error
        org_user.delete()

    def test_nonmember_owner(self):
        from organizations.exceptions import OrganizationMismatch
        foo_user = self.foo.owner
        self.nirvana.owner = foo_user
        self.assertRaises(OrganizationMismatch, self.nirvana.owner.save)


@override_settings(USE_TZ=True)
class OrgDeleteTests(TestCase):

    fixtures = ['users.json', 'orgs.json']

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
                organization__name="Nirvana", user=krist)
        org_user.delete()
        self.assertTrue(krist.pk)
