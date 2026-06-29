"""
Tests for the asynchronous (``a``-prefixed) API.

These mirror the synchronous model/util tests in ``test_models.py`` but exercise
the real asyncio code paths (Django's async ORM and ``Signal.asend``).
"""

from unittest import skipUnless

from django.contrib.auth.models import User
from django.dispatch import Signal
from django.test import TestCase
from django.test.utils import override_settings

from organizations.models import Organization
from organizations.models import OrganizationUser
from organizations.signals import owner_changed
from organizations.signals import user_added
from organizations.signals import user_removed
from organizations.utils import acreate_organization
from test_accounts.models import Account
from test_accounts.models import AccountInvitation

# Async signal dispatch (``Signal.asend``) requires Django 5.0+. The async API
# is not supported on the (end-of-life) Django 4.2 series.
requires_async_signals = skipUnless(
    hasattr(Signal, "asend"), "Async API requires Django 5.0+ (Signal.asend)"
)


@requires_async_signals
@override_settings(USE_TZ=True)
class AsyncOrgModelTests(TestCase):
    fixtures = ["users.json", "orgs.json"]

    def setUp(self):
        self.kurt = User.objects.get(username="kurt")
        self.dave = User.objects.get(username="dave")
        self.krist = User.objects.get(username="krist")
        self.duder = User.objects.get(username="duder")
        self.nirvana = Organization.objects.get(name="Nirvana")
        self.foo = Organization.objects.get(name="Foo Fighters")

    async def test_ais_member(self):
        self.assertTrue(await self.nirvana.ais_member(self.kurt))
        self.assertTrue(await self.nirvana.ais_member(self.dave))
        self.assertTrue(await self.foo.ais_member(self.dave))
        self.assertFalse(await self.foo.ais_member(self.kurt))

    async def test_ais_admin(self):
        self.assertTrue(await self.nirvana.ais_admin(self.kurt))
        self.assertTrue(await self.nirvana.ais_admin(self.krist))
        self.assertFalse(await self.nirvana.ais_admin(self.dave))
        self.assertTrue(await self.foo.ais_admin(self.dave))

    async def test_ais_owner(self):
        self.assertTrue(await self.nirvana.ais_owner(self.kurt))
        self.assertTrue(await self.foo.ais_owner(self.dave))
        self.assertFalse(await self.nirvana.ais_owner(self.dave))
        self.assertFalse(await self.nirvana.ais_owner(self.krist))

    async def test_aadd_user(self):
        received = []

        def receiver(sender, user, **kwargs):
            received.append(user)

        user_added.connect(receiver, weak=False)
        try:
            new_guy = await self.foo.aadd_user(self.krist)
        finally:
            user_added.disconnect(receiver)
        self.assertTrue(isinstance(new_guy, OrganizationUser))
        self.assertEqual(new_guy.organization_id, self.foo.pk)
        self.assertEqual(received, [self.krist])

    async def test_aadd_user_first_user_is_owner(self):
        org = await Organization.objects.acreate(name="Empty", slug="empty")
        org_user = await org.aadd_user(self.duder)
        self.assertTrue(org_user.is_admin)
        self.assertTrue(await org.ais_owner(self.duder))

    async def test_aremove_user(self):
        received = []

        def receiver(sender, user, **kwargs):
            received.append(user)

        await self.foo.aadd_user(self.krist)
        user_removed.connect(receiver, weak=False)
        try:
            await self.foo.aremove_user(self.krist)
        finally:
            user_removed.disconnect(receiver)
        self.assertFalse(await self.foo.users.filter(pk=self.krist.pk).aexists())
        self.assertEqual(received, [self.krist])

    async def test_aget_or_add_user(self):
        new_guy, created = await self.foo.aget_or_add_user(self.duder)
        self.assertTrue(isinstance(new_guy, OrganizationUser))
        self.assertEqual(new_guy.organization_id, self.foo.pk)
        self.assertTrue(created)

        existing, created = await self.foo.aget_or_add_user(self.dave)
        self.assertTrue(isinstance(existing, OrganizationUser))
        self.assertFalse(created)

    async def test_achange_owner(self):
        received = []

        def receiver(sender, old, new, **kwargs):
            received.append((old, new))

        admin = await OrganizationUser.objects.aget(
            organization=self.nirvana, user=self.krist
        )
        owner_changed.connect(receiver, weak=False)
        try:
            await self.nirvana.achange_owner(admin)
        finally:
            owner_changed.disconnect(receiver)
        owner = await self.nirvana._org_owner_model.objects.aget(
            organization=self.nirvana
        )
        self.assertEqual(owner.organization_user_id, admin.pk)
        self.assertEqual(len(received), 1)
        self.assertEqual(received[0][1], admin)


@requires_async_signals
@override_settings(USE_TZ=True)
class AsyncBaseOrganizationTests(TestCase):
    """Exercise the async API on the lighter ``OrganizationBase`` line."""

    fixtures = ["users.json"]

    def setUp(self):
        self.kurt = User.objects.get(username="kurt")
        self.dave = User.objects.get(username="dave")

    async def test_aadd_user(self):
        account = await Account.objects.acreate(name="Acme")
        received = []

        def receiver(sender, user, **kwargs):
            received.append(user)

        user_added.connect(receiver, weak=False)
        try:
            org_user = await account.aadd_user(self.dave)
        finally:
            user_added.disconnect(receiver)
        self.assertEqual(org_user.organization_id, account.pk)
        self.assertTrue(await account.ais_member(self.dave))
        self.assertEqual(received, [self.dave])

    async def test_aactivate(self):
        account = await Account.objects.acreate(name="InviteCo")
        invitation = await AccountInvitation.objects.acreate(
            invitee_identifier="newbie@example.com",
            invited_by=self.kurt,
            organization=account,
        )
        org_user = await invitation.aactivate(self.dave)
        self.assertEqual(org_user.organization_id, account.pk)
        self.assertTrue(await account.ais_member(self.dave))
        refreshed = await AccountInvitation.objects.aget(pk=invitation.pk)
        self.assertEqual(refreshed.invitee_id, self.dave.pk)


@requires_async_signals
@override_settings(USE_TZ=True)
class AsyncCreateOrganizationTests(TestCase):
    fixtures = ["users.json", "orgs.json"]

    def setUp(self):
        self.dave = User.objects.get(username="dave")

    async def test_acreate_organization(self):
        org = await acreate_organization(self.dave, "Async Org", slug="async-org")
        self.assertTrue(await Organization.objects.filter(name="Async Org").aexists())
        self.assertTrue(await org.ais_owner(self.dave))
        owner_org_user = await OrganizationUser.objects.aget(organization=org)
        self.assertTrue(owner_org_user.is_admin)
