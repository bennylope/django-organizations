from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.test import TestCase
from django.test.client import RequestFactory
from django.test.utils import override_settings
from django.urls import reverse

import pytest

from organizations.models import Organization
from organizations.models import OrganizationUser
from organizations.utils import create_organization
from organizations.views import base
from test_accounts.models import Account
from test_accounts.models import AccountUser
from tests.utils import request_factory_login


@pytest.fixture
def account_user():
    yield User.objects.create(username="AccountUser", email="akjdkj@kjdk.com")


@pytest.fixture
def account_account(account_user):
    yield create_organization(account_user, "Acme", org_model=Account)


@pytest.fixture
def org_organization(account_user):
    yield create_organization(account_user, "Acme", org_model=Organization)


@pytest.fixture
def extra_org_user(org_organization):
    new_user = User.objects.create(username="NotYou", email="not@you.com")
    org_organization.add_user(new_user)
    yield new_user


@pytest.fixture
def invitee_user():
    yield User.objects.create_user(
        "newmember", email="jd@123.com", password="password123"
    )


class TestUserReminderView:
    @pytest.mark.parametrize("method", [("get"), ("post")])
    def test_bad_request_for_active_user(
        self, rf, account_account, account_user, invitee_user, method
    ):
        class OrgUserReminderView(base.BaseOrganizationUserRemind):
            org_model = Account
            user_model = AccountUser

        request = getattr(rf, method)("/", user=account_user)
        kwargs = {"organization_pk": account_account.pk, "user_pk": account_user.pk}
        response = OrgUserReminderView.as_view()(request, **kwargs)
        assert response.status_code == 410

    def test_organization_user_reminder(
        self, rf, account_account, account_user, invitee_user
    ):
        class OrgUserReminderView(base.BaseOrganizationUserRemind):
            org_model = Account
            user_model = AccountUser

        invitee_user.is_active = False
        invitee_user.save()
        account_account.add_user(invitee_user)
        request = rf.get("/", user=account_user)
        kwargs = {"organization_pk": account_account.pk, "user_pk": invitee_user.pk}
        response = OrgUserReminderView.as_view()(request, **kwargs)
        assert response.status_code == 200

        request = rf.post("/")
        request.user = account_user
        response = OrgUserReminderView.as_view()(request, **kwargs)
        assert response.status_code == 302


class TestSignupView:
    def test_anon_user_can_access_signup_view(self, rf):
        """"""
        request = request_factory_login(rf)
        assert base.OrganizationSignup.as_view()(request).status_code == 200

    def test_authenticated_user_is_redirected_from_signup_view(self, rf, account_user):
        request = request_factory_login(rf, account_user)
        assert base.OrganizationSignup.as_view()(request).status_code == 302

    def test_anon_user_signup_base_class_has_no_success_url(self, rf):
        """"""
        request = request_factory_login(
            rf,
            method="post",
            path="/",
            data={
                "name": "An Association of Very Interesting People",
                "slug": "people",
                "email": "hey@people.org",
            },
        )
        with pytest.raises(ImproperlyConfigured):
            base.OrganizationSignup.as_view()(request)

    def test_anon_user_can_signup(self, rf):
        """"""

        class SignupView(base.OrganizationSignup):
            success_url = "/"

        request = request_factory_login(
            rf,
            method="post",
            path="/",
            data={
                "name": "An Association of Very Interesting People",
                "slug": "people",
                "email": "hey@people.org",
            },
        )
        response = SignupView.as_view()(request)
        assert response.status_code == 302

        # Verify its in the database
        Organization.objects.get(
            slug="an-association-of-very-interesting-people", is_active=False
        )


class TestBaseCreateOrganization:
    def test_get_org_create_view(self, rf):
        request = request_factory_login(rf)
        assert base.BaseOrganizationCreate.as_view()(request).status_code == 200

    def test_create_new_org(self, rf, account_user):
        request = request_factory_login(
            rf,
            user=account_user,
            method="post",
            path="/",
            data={"name": "Vizsla Club", "slug": "vizsla", "email": "hey@woof.org"},
        )
        response = base.BaseOrganizationCreate.as_view()(request)
        assert response.status_code == 302
        assert response["Location"] == reverse("organization_list")
        assert Organization.objects.get(slug="vizsla-club")


class TestBaseOrganizationDelete:
    def test_get_org_delete(self, rf, org_organization, account_user):
        request = request_factory_login(rf, user=account_user)
        kwargs = {"organization_pk": org_organization.pk}
        response = base.BaseOrganizationDelete.as_view()(request, **kwargs)
        assert response.status_code == 200

    def test_delete_organization_with_post(self, rf, org_organization, account_user):
        request = request_factory_login(rf, user=account_user, method="post", path="/")
        kwargs = {"organization_pk": org_organization.pk}
        response = base.BaseOrganizationDelete.as_view()(request, **kwargs)
        assert response.status_code == 302
        with pytest.raises(ObjectDoesNotExist):
            org_organization.refresh_from_db()


class TestBaseOrganizationUserDelete:
    def test_get_org_user_delete(
        self, rf, org_organization, account_user, extra_org_user
    ):
        request = request_factory_login(rf, user=account_user)
        kwargs = {"organization_pk": org_organization.pk, "user_pk": extra_org_user.pk}
        response = base.BaseOrganizationUserDelete.as_view()(request, **kwargs)
        assert response.status_code == 200

    def test_delete_organization_user_with_post(
        self, rf, org_organization, account_user, extra_org_user
    ):
        request = request_factory_login(rf, user=account_user, method="post", path="/")
        kwargs = {"organization_pk": org_organization.pk, "user_pk": extra_org_user.pk}
        response = base.BaseOrganizationUserDelete.as_view()(request, **kwargs)
        assert response.status_code == 302
        with pytest.raises(ObjectDoesNotExist):
            OrganizationUser.objects.get(user=extra_org_user)


@override_settings(USE_TZ=True)
class TestBasicOrgViews(TestCase):
    fixtures = ["users.json", "orgs.json"]

    def setUp(self):
        self.kurt = User.objects.get(username="kurt")
        self.dave = User.objects.get(username="dave")
        self.dummy = User.objects.create_user(
            "dummy", email="dummy@example.com", password="test"
        )
        self.nirvana = Organization.objects.get(name="Nirvana")
        self.factory = RequestFactory()
        self.kurt_request = request_factory_login(self.factory, self.kurt)
        self.dave_request = request_factory_login(self.factory, self.dave)
        self.anon_request = request_factory_login(self.factory)

    def test_org_list(self):
        """Ensure that the status code 200 is returned"""
        self.assertEqual(
            200,
            base.BaseOrganizationList(request=self.kurt_request)
            .get(self.kurt_request)
            .status_code,
        )
        self.assertEqual(
            200,
            base.BaseOrganizationList(request=self.dave_request)
            .get(self.dave_request)
            .status_code,
        )

    def test_org_list_queryset(self):
        """Ensure only active organizations belonging to the user are listed"""
        self.assertEqual(
            1,
            base.BaseOrganizationList(request=self.kurt_request).get_queryset().count(),
        )
        self.assertEqual(
            2,
            base.BaseOrganizationList(request=self.dave_request).get_queryset().count(),
        )

    def test_org_detail(self):
        kwargs = {"organization_pk": self.nirvana.pk}
        self.assertEqual(
            200,
            base.BaseOrganizationDetail(request=self.kurt_request, kwargs=kwargs)
            .get(self.kurt_request, **kwargs)
            .status_code,
        )

    def test_org_update(self):
        kwargs = {"organization_pk": self.nirvana.pk}
        self.assertEqual(
            200,
            base.BaseOrganizationUpdate(request=self.kurt_request, kwargs=kwargs)
            .get(self.kurt_request, **kwargs)
            .status_code,
        )

    def test_user_list(self):
        kwargs = {"organization_pk": self.nirvana.pk}
        self.assertEqual(
            200,
            base.BaseOrganizationUserList(request=self.kurt_request, kwargs=kwargs)
            .get(self.kurt_request, **kwargs)
            .status_code,
        )

    def test_user_detail(self):
        kwargs = {"organization_pk": self.nirvana.pk, "user_pk": self.kurt.pk}
        self.assertEqual(
            200,
            base.BaseOrganizationUserDetail(request=self.kurt_request, kwargs=kwargs)
            .get(self.kurt_request, **kwargs)
            .status_code,
        )

    def test_bad_user_detail(self):
        kwargs = {"organization_pk": self.nirvana.pk, "user_pk": self.dummy.pk}
        self.assertRaises(
            Http404,
            base.BaseOrganizationUserDetail(
                request=self.kurt_request, kwargs=kwargs
            ).get,
            self.kurt_request,
            **kwargs,
        )

    def test_user_create_get(self):
        kwargs = {"organization_pk": self.nirvana.pk}
        self.assertEqual(
            200,
            base.BaseOrganizationUserCreate(request=self.kurt_request, kwargs=kwargs)
            .get(self.kurt_request, **kwargs)
            .status_code,
        )

    def test_user_create_post(self):
        request = request_factory_login(
            self.factory,
            self.kurt,
            path="/",
            method="post",
            data={"email": "roadie@yahoo.com"},
        )
        kwargs = {"organization_pk": self.nirvana.pk}
        self.assertEqual(
            302,
            base.BaseOrganizationUserCreate.as_view()(request, **kwargs).status_code,
        )

    def test_user_update(self):
        kwargs = {"organization_pk": self.nirvana.pk, "user_pk": self.kurt.pk}
        self.assertEqual(
            200,
            base.BaseOrganizationUserUpdate(request=self.kurt_request, kwargs=kwargs)
            .get(self.kurt_request, **kwargs)
            .status_code,
        )
