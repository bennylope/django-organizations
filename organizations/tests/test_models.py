from django.test import TestCase
from django.contrib.auth.models import User
from django.db import IntegrityError

from organizations.models import (Organization, OrganizationUser,
        OrganizationOwner)


class ActiveManagerTests(TestCase):

    fixtures = ['users.json', 'orgs.json']

    def test_active(self):
        self.assertEqual(3, Organization.objects.all().count())
        self.assertEqual(2, Organization.active.all().count())

    def test_by_user(self):
        user = User.objects.get(username="dave")
        self.assertEqual(3, Organization.objects.get_for_user(user).count())
        self.assertEqual(2, Organization.active.get_for_user(user).count())


class OrgModelTests(TestCase):

    fixtures = ['users.json', 'orgs.json']

    def setUp(self):
        self.kurt = User.objects.get(username="kurt")
        self.dave = User.objects.get(username="dave")
        self.krist = User.objects.get(username="krist")
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

    def test_delete_owner(self):
        from organizations.exceptions import OwnershipRequired
        owner = self.nirvana.owner.organization_user
        self.assertRaises(OwnershipRequired, owner.delete)

    def test_nonmember_owner(self):
        from organizations.exceptions import OrganizationMismatch
        foo_user = self.foo.owner
        self.nirvana.owner = foo_user
        self.assertRaises(OrganizationMismatch, self.nirvana.owner.save)
