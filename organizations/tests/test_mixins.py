from django.contrib.auth.models import User
from django.http import HttpResponse
from django.test import TestCase
from django.test.client import RequestFactory
from django.test.utils import override_settings

from organizations.models import Organization, OrganizationUser
from organizations.tests.utils import request_factory_login
from organizations.mixins import (OrganizationMixin, OrganizationUserMixin,
        MembershipRequiredMixin, AdminRequiredMixin, OwnerRequiredMixin)
from django.conf.locale import tr


class ViewStub(object):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def get_context_data(self, **kwargs):
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        return HttpResponse("Success")


class OrgView(OrganizationMixin, ViewStub):
    """A testing view class"""
    pass


class UserView(OrganizationUserMixin, ViewStub):
    """A testing view class"""
    pass


@override_settings(USE_TZ=True)
class ObjectMixinTests(TestCase):

    fixtures = ['users.json', 'orgs.json']

    def setUp(self):
        self.foo = Organization.objects.get(name='Foo Fighters')
        self.dave = OrganizationUser.objects.get(user__username='dave',
                organization=self.foo)

    def test_get_org_object(self):
        view = OrgView(organization_pk=self.foo.pk)
        self.assertEqual(view.get_object(), self.foo)

    def test_get_user_object(self):
        view = UserView(organization_pk=self.foo.pk, user_pk=self.dave.pk)
        self.assertEqual(view.get_object(), self.dave)
        self.assertEqual(view.get_organization(), self.foo)

    def test_get_model(self):
        """Ensure that the method returns the class object"""
        self.assertEqual(Organization, OrganizationMixin().get_org_model())
        self.assertEqual(Organization, OrganizationUserMixin().get_org_model())
        self.assertEqual(OrganizationUser,
                OrganizationUserMixin().get_user_model())

@override_settings(USE_TZ=True)
class AccessMixinTests(TestCase):

    fixtures = ['users.json', 'orgs.json']

    def setUp(self):
        self.nirvana = Organization.objects.get(name="Nirvana")
        self.kurt = User.objects.get(username="kurt")
        self.krist = User.objects.get(username="krist")
        self.dave = User.objects.get(username="dave")
        self.dummy = User.objects.create_user("dummy",
                email="dummy@example.com", password="test")
        self.factory = RequestFactory()
        self.kurt_request = request_factory_login(self.factory, self.kurt)
        self.krist_request = request_factory_login(self.factory, self.krist)
        self.dave_request = request_factory_login(self.factory, self.dave)
        self.dummy_request = request_factory_login(self.factory, self.dummy)

    def test_member_access(self):
        class MemberView(MembershipRequiredMixin, OrgView):
            pass
        self.assertEqual(200, MemberView().dispatch(self.kurt_request,
            organization_pk=self.nirvana.pk).status_code)
        self.assertEqual(200, MemberView().dispatch(self.krist_request,
            organization_pk=self.nirvana.pk).status_code)
        self.assertEqual(200, MemberView().dispatch(self.dave_request,
            organization_pk=self.nirvana.pk).status_code)
        self.assertEqual(403, MemberView().dispatch(self.dummy_request,
            organization_pk=self.nirvana.pk).status_code)

    def test_admin_access(self):
        class AdminView(AdminRequiredMixin, OrgView):
            pass
        self.assertEqual(200, AdminView().dispatch(self.kurt_request,
            organization_pk=self.nirvana.pk).status_code)
        self.assertEqual(200, AdminView().dispatch(self.krist_request,
            organization_pk=self.nirvana.pk).status_code)
        # Superuser
        self.assertEqual(200, AdminView().dispatch(self.dave_request,
            organization_pk=self.nirvana.pk).status_code)
        self.assertEqual(403, AdminView().dispatch(self.dummy_request,
            organization_pk=self.nirvana.pk).status_code)

    def test_owner_access(self):
        class OwnerView(OwnerRequiredMixin, OrgView):
            pass
        self.assertEqual(200, OwnerView().dispatch(self.kurt_request,
            organization_pk=self.nirvana.pk).status_code)
        self.assertEqual(403, OwnerView().dispatch(self.krist_request,
            organization_pk=self.nirvana.pk).status_code)
        # Superuser
        self.assertEqual(200, OwnerView().dispatch(self.dave_request,
            organization_pk=self.nirvana.pk).status_code)
        self.assertEqual(403, OwnerView().dispatch(self.dummy_request,
            organization_pk=self.nirvana.pk).status_code)


