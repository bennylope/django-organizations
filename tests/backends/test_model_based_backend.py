# -*- coding: utf-8 -*-

"""
Tests for the model based invitation backend
"""

from django.conf import settings
from django.contrib.auth.models import User
from django.core import mail

import pytest

from organizations.backends.defaults import InvitationBackend
from organizations.backends.modeled import ModelInvitation
from organizations.base import OrganizationInvitationBase
from organizations.utils import create_organization
from test_abstract.models import CustomOrganization
from test_accounts.models import Account
from test_accounts.models import AccountInvitation
from test_vendors.models import Vendor

pytestmark = pytest.mark.django_db


@pytest.fixture
def account_user():
    yield User.objects.create(username="AccountUser", email="akjdkj@kjdk.com")


@pytest.fixture
def account_account(account_user):
    vendor = create_organization(account_user, "Acme", org_model=Account)
    yield vendor


@pytest.fixture
def invitee_user():
    yield User.objects.create_user(
        "newmember", email="jd@123.com", password="password123"
    )


@pytest.fixture
def invitation_backend():
    yield ModelInvitation(org_model=Account)


@pytest.fixture
def email_invitation(invitation_backend, account_account, account_user, invitee_user):
    yield invitation_backend.invite_by_email(
        invitee_user.email, user=account_user, organization=account_account
    )


class TestCustomModelBackend:
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


class TestInvitationModelBackend:
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

    def test_account_invitation_is_org_invitation_base(self, email_invitation):
        assert isinstance(email_invitation, OrganizationInvitationBase)

    def test_send_invitation_anon_user(
        self, invitation_backend, account_user, account_account, client
    ):
        """Integration test with anon user"""

        outbox_count = len(mail.outbox)
        invitation = invitation_backend.invite_by_email(
            "bob@newuser.com", user=account_user, organization=account_account
        )

        assert len(mail.outbox) > outbox_count

        response = client.get(invitation.get_absolute_url())
        assert response.status_code == 200

    def test_new_user_accepts_invitation(
        self, invitation_backend, account_user, account_account, client
    ):
        invitation = invitation_backend.invite_by_email(
            "heehaw@hello.com", user=account_user, organization=account_account
        )
        response = client.post(
            invitation.get_absolute_url(),
            data={
                "username": "heehaw",
                "email": "heehaw@hello.com",
                "password1": "aksjdf83k1j!!",
                "password2": "aksjdf83k1j!!",
            },
        )
        assert response.status_code == 302

    def test_that_the_inviting_user_cannot_access(
        self, email_invitation, invitee_user, account_user, account_account, client
    ):
        client.force_login(account_user)
        response = client.get(email_invitation.get_absolute_url())
        assert response.status_code == 403

    def test_existing_user_is_not_linked_as_invitee_at_invitation_time(
        self, email_invitation, invitee_user, account_user, account_account, client
    ):
        assert email_invitation.invitee is None
        assert email_invitation.invitee_identifier == invitee_user.email

    def test_existing_user_can_view_the_invitation(
        self, email_invitation, invitee_user, client
    ):
        client.force_login(invitee_user)
        response = client.get(email_invitation.get_absolute_url())
        assert response.status_code == 200

    def test_existing_user_activating_invitation(
        self, email_invitation, invitee_user, client
    ):
        # Need an org with an invite to a user who is logged in
        client.force_login(invitee_user)
        client.post(email_invitation.get_absolute_url())
        email_invitation.refresh_from_db()
        assert email_invitation.invitee == invitee_user

    def test_accessing_invitation_once_it_has_been_used(
        self, invitee_user, account_user, account_account, client
    ):
        invitation = AccountInvitation.objects.create(
            invitee_identifier=invitee_user.email,
            invitee=invitee_user,
            invited_by=account_user,
            organization=account_account,
        )
        client.force_login(invitee_user)
        response = client.get(invitation.get_absolute_url())
        assert response.status_code == 302
