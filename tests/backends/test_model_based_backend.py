# -*- coding: utf-8 -*-

"""

"""

import pytest
from django.contrib.auth.models import User
from django.core import mail

from organizations.backends.defaults import InvitationBackend
from organizations.backends.modeled import ModelInvitation
from organizations.base import OrganizationInvitationBase
from organizations.utils import create_organization
from test_abstract.models import CustomOrganization
from test_accounts.models import Account
from test_vendors.models import Vendor

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

    def test_send_invitation_anon_user(self, account_user, account_account, client):
        """Integration test with anon user"""
        from django.conf import settings

        outbox_count = len(mail.outbox)
        backend = ModelInvitation(org_model=Account)
        invitation = backend.invite_by_email(
            "bob@newuser.com", user=account_user, organization=account_account
        )

        assert isinstance(invitation, OrganizationInvitationBase)
        assert len(mail.outbox) > outbox_count
        assert list(settings.MIDDLEWARE)

        response = client.get(invitation.get_absolute_url())
        assert response.status_code == 200
