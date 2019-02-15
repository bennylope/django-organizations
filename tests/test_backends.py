
import uuid

import pytest
from django.contrib.auth.models import User
from django.core import mail
from django.http import Http404
from django.http import QueryDict
from django.test import TestCase
from django.test.client import RequestFactory
from django.test.utils import override_settings

from organizations.backends.defaults import BaseBackend
from organizations.backends.defaults import InvitationBackend
from organizations.backends.defaults import RegistrationBackend
from organizations.backends.modeled import ModelInvitation
from organizations.backends.tokens import RegistrationTokenGenerator
from organizations.base import OrganizationInvitationBase
from organizations.compat import reverse
from organizations.models import Organization
from organizations.utils import create_organization
from test_abstract.models import CustomOrganization
from test_accounts.models import Account
from test_vendors.models import Vendor
from tests.utils import request_factory_login

pytestmark = pytest.mark.django_db

# @pytest.fixture(scope="module")
@pytest.fixture
def account_user():
    yield User.objects.create(username="183jkjd", email="akjdkj@kjdk.com")


# @pytest.fixture(scope="module")
@pytest.fixture
def account_account(account_user):
    vendor = create_organization(account_user, "Acme", org_model=Account)
    yield vendor


@override_settings(USE_TZ=True)
class BaseTests(TestCase):

    def test_generate_username(self):
        self.assertTrue(BaseBackend().get_username())


@override_settings(
    INSTALLED_APPS=[
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sites",
        "test_accounts",
    ],
    USE_TZ=True,
)
class TestSansOrganizations(TestCase):

    def test_verify_the_world(self):
        """Verify the test environment is set up correctly"""
        from django.conf import settings

        self.assertFalse("organizations" in settings.INSTALLED_APPS)

    def test_generate_username(self):
        self.assertTrue(BaseBackend().get_username())

    def test_backend_urls(self):
        self.assertTrue(InvitationBackend().get_urls())


@override_settings(USE_TZ=True)
class InvitationTests(TestCase):

    fixtures = ["users.json", "orgs.json"]

    def setUp(self):
        mail.outbox = []
        self.factory = RequestFactory()
        self.tokenizer = RegistrationTokenGenerator()
        self.user = User.objects.get(username="krist")
        self.pending_user = User.objects.create_user(
            username="theresa", email="t@example.com", password="test"
        )
        self.pending_user.is_active = False
        self.pending_user.save()

    def test_backend_definition(self):
        from organizations.backends import invitation_backend

        self.assertTrue(isinstance(invitation_backend(), InvitationBackend))

    def test_create_user(self):
        invited = InvitationBackend().invite_by_email("sedgewick@example.com")
        self.assertTrue(isinstance(invited, User))
        self.assertFalse(invited.is_active)
        self.assertEqual(1, len(mail.outbox))
        mail.outbox = []

    def test_create_existing_user(self):
        invited = InvitationBackend().invite_by_email(self.user.email)
        self.assertEqual(self.user, invited)
        self.assertEqual(0, len(mail.outbox))  # User is active

    def test_send_reminder(self):
        InvitationBackend().send_reminder(self.pending_user)
        self.assertEqual(1, len(mail.outbox))
        InvitationBackend().send_reminder(self.user)
        self.assertEqual(1, len(mail.outbox))  # User is active
        mail.outbox = []

    def test_urls(self):
        """Ensure no error is raised"""
        reverse(
            "invitations_register",
            kwargs={
                "user_id": self.pending_user.pk,
                "token": self.tokenizer.make_token(self.pending_user),
            },
        )

    def test_activate_user(self):
        request = self.factory.request()
        with self.assertRaises(Http404):
            InvitationBackend().activate_view(
                request, self.user.pk, self.tokenizer.make_token(self.user)
            )
        self.assertEqual(
            200,
            InvitationBackend().activate_view(
                request,
                self.pending_user.pk,
                self.tokenizer.make_token(self.pending_user),
            ).status_code,
        )

    def test_send_notification_inactive_user(self):
        """
        This test verifies that calling the send_notification function
        from the OrganizationsCoreInvitationBackend with an inactive Django
        user causes the function to return False without sending an email.
        """
        org = Organization.objects.create(name="Test Organization")
        result = InvitationBackend().send_notification(
            self.pending_user, domain="example.com", organization=org, sender=self.user
        )
        self.assertEqual(result, False)
        self.assertEquals(0, len(mail.outbox))

    def test_send_notification_active_user(self):
        """
        This test verifies that calling the send_notification function
        from the OrganizationsCoreInvitationBackend with an active Django
        user causes the function send an email to that user.
        """
        org = Organization.objects.create(name="Test Organization")
        InvitationBackend().send_notification(
            self.user, domain="example.com", organization=org, sender=self.pending_user
        )
        self.assertEquals(1, len(mail.outbox))
        self.assertEquals(
            mail.outbox[0].subject, u"You've been added to an organization"
        )


@override_settings(USE_TZ=True)
class RegistrationTests(TestCase):

    fixtures = ["users.json", "orgs.json"]

    def setUp(self):
        mail.outbox = []
        self.factory = RequestFactory()
        self.tokenizer = RegistrationTokenGenerator()
        self.user = User.objects.get(username="krist")
        self.pending_user = User.objects.create_user(
            username="theresa", email="t@example.com", password="test"
        )
        self.pending_user.is_active = False
        self.pending_user.save()

    def test_backend_definition(self):
        from organizations.backends import registration_backend

        self.assertTrue(isinstance(registration_backend(), RegistrationBackend))

    def test_register_authenticated(self):
        """Ensure an already authenticated user is redirected"""
        backend = RegistrationBackend()
        request = request_factory_login(self.factory, self.user)
        self.assertEqual(302, backend.create_view(request).status_code)

    def test_register_existing(self):
        """Ensure that an existing user is redirected to login"""
        backend = RegistrationBackend()
        request = request_factory_login(self.factory)
        request.POST = QueryDict("name=Mudhoney&slug=mudhoney&email=dave@foo.com")
        self.assertEqual(302, backend.create_view(request).status_code)

    def test_create_user(self):
        registered = RegistrationBackend().register_by_email("greenway@example.com")
        self.assertTrue(isinstance(registered, User))
        self.assertFalse(registered.is_active)
        self.assertEqual(1, len(mail.outbox))
        mail.outbox = []

    def test_create_existing_user(self):
        registered = RegistrationBackend().register_by_email(self.user.email)
        self.assertEqual(self.user, registered)
        self.assertEqual(0, len(mail.outbox))  # User is active

    def test_send_reminder(self):
        RegistrationBackend().send_reminder(self.pending_user)
        self.assertEqual(1, len(mail.outbox))
        RegistrationBackend().send_reminder(self.user)
        self.assertEqual(1, len(mail.outbox))  # User is active
        mail.outbox = []

    def test_urls(self):
        reverse(
            "registration_register",
            kwargs={
                "user_id": self.pending_user.pk,
                "token": self.tokenizer.make_token(self.pending_user),
            },
        )

    def test_activate_user(self):
        request = self.factory.request()
        with self.assertRaises(Http404):
            RegistrationBackend().activate_view(
                request, self.user.pk, self.tokenizer.make_token(self.user)
            )
        self.assertEqual(
            200,
            RegistrationBackend().activate_view(
                request,
                self.pending_user.pk,
                self.tokenizer.make_token(self.pending_user),
            ).status_code,
        )

    def test_activate_orgs(self):
        """Ensure method activates organizations and w/o specified org_model"""
        org = Organization.objects.create(
            name="Test", slug="kjadkjkaj", is_active=False
        )
        org.add_user(self.user)
        self.assertFalse(org.is_active)
        backend = InvitationBackend()
        backend.activate_organizations(self.user)
        refreshed_org = Organization.objects.get(pk=org.pk)
        self.assertTrue(refreshed_org.is_active)


class TestBackendNamespacing(object):

    def test_registration_create(self):
        assert reverse("registration_create")
        # assert reverse("index")

        assert reverse(
            "test_accounts:account_invitations:invitations_register",
            kwargs={"guid": str(uuid.uuid4()).replace("-", "")},
        )


class CustomModelBackend(object):
    """
    The default backend should provide the same basic functionality
    irrespective of the organization model.
    """

    def test_activate_orgs_vendor(self, account_user):
        """Ensure no errors raised because correct relation name used"""
        backend = InvitationBackend(org_model=Vendor)
        backend.activate_organizations(account_user)

    def test_activate_orgs_abstract(self, account_user):
        backend = InvitationBackend(org_model=CustomOrganization)
        backend.activate_organizations(account_user)


class TestInvitationModelBackend(object):
    """
    Tests the backend using InvitationModels

    pytest only!
    """

    def test_invite_returns_invitation(self, account_user, account_account):
        backend = ModelInvitation(org_model=Account)
        invitation = backend.invite_by_email(
            "bob@newuser.com", user=account_user, organization=account_account
        )
        assert isinstance(invitation, OrganizationInvitationBase)

    def test_send_invitation_anon_user(self, account_user, account_account, client):
        """Integration test with anon user"""
        outbox_count = len(mail.outbox)
        backend = ModelInvitation(org_model=Account)
        invitation = backend.invite_by_email(
            "bob@newuser.com", user=account_user, organization=account_account
        )

        assert isinstance(invitation, OrganizationInvitationBase)
        assert len(mail.outbox) > outbox_count

        from django.conf import settings

        assert list(settings.MIDDLEWARE)

        response = client.get(invitation.get_absolute_url())
        assert response.status_code == 200
