from django.core import mail
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden, QueryDict
from django.test import TestCase
from django.test.client import RequestFactory
from django.test.utils import override_settings

from test_vendors.models import Vendor

from organizations.backends.defaults import (BaseBackend, InvitationBackend,
        RegistrationBackend)
from organizations.backends.tokens import RegistrationTokenGenerator
from organizations.models import Organization
from .utils import request_factory_login


@override_settings(USE_TZ=True)
class BaseTests(TestCase):

    def test_generate_username(self):
        self.assertTrue(BaseBackend().get_username())


@override_settings(USE_TZ=True)
class InvitationTests(TestCase):

    fixtures = ['users.json', 'orgs.json']

    def setUp(self):
        mail.outbox = []
        self.factory = RequestFactory()
        self.tokenizer = RegistrationTokenGenerator()
        self.user = User.objects.get(username="krist")
        self.pending_user = User.objects.create_user(username="theresa",
                email="t@example.com", password="test")
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
        reverse('invitations_register', kwargs={
            'user_id': self.pending_user.id,
            'token': self.tokenizer.make_token(self.pending_user)})

    def test_activate_user(self):
        request = self.factory.request()
        with self.assertRaises(HttpResponseForbidden):
            InvitationBackend().activate_view(request, self.user.id,
                    self.tokenizer.make_token(self.user))
        self.assertEqual(200, InvitationBackend().activate_view(request,
            self.pending_user.id,
            self.tokenizer.make_token(self.pending_user)).status_code)


@override_settings(USE_TZ=True)
class RegistrationTests(TestCase):

    fixtures = ['users.json', 'orgs.json']

    def setUp(self):
        mail.outbox = []
        self.factory = RequestFactory()
        self.tokenizer = RegistrationTokenGenerator()
        self.user = User.objects.get(username="krist")
        self.pending_user = User.objects.create_user(username="theresa",
                email="t@example.com", password="test")
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
        reverse('registration_register', kwargs={
            'user_id': self.pending_user.id,
            'token': self.tokenizer.make_token(self.pending_user)})

    def test_activate_user(self):
        request = self.factory.request()
        with self.assertRaises(HttpResponseForbidden):
            RegistrationBackend().activate_view(request, self.user.id,
                    self.tokenizer.make_token(self.user))
        self.assertEqual(200, RegistrationBackend().activate_view(request,
            self.pending_user.id,
            self.tokenizer.make_token(self.pending_user)).status_code)

    def test_activate_orgs(self):
        """Ensure method activates organizations and w/o specified org_model"""
        org = Organization.objects.create(name="Test", slug="kjadkjkaj", is_active=False)
        org.add_user(self.user)
        self.assertFalse(org.is_active)
        backend = InvitationBackend()
        backend.activate_organizations(self.user)
        refreshed_org = Organization.objects.get(pk=org.pk)
        self.assertTrue(refreshed_org.is_active)


class CustomModelBackend(TestCase):
    """
    The default backend should provide the same basic functionality
    irrespective of the organization model.
    """

    def test_activate_orgs(self):
        """Ensure no errors raised because correct relation name used"""
        user = User.objects.create(username="183jkjd", email="akjdkj@kjdk.com")
        backend = InvitationBackend(org_model=Vendor)
        backend.activate_organizations(user)
