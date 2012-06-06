from django.contrib.auth.models import User
from django.http import Http404
from django.test import TestCase
from django.test.client import RequestFactory

from organizations.models import Organization, OrganizationUser
from organizations.tests.utils import request_factory_login
from organizations.mixins import (OrganizationMixin, OrganizationUserMixin,
        MembershipRequiredMixin, AdminRequiredMixin, OwnerRequiredMixin)


class ViewStub(object):
    def __init__(self, **kwargs):
        self.kwargs = kwargs


class ObjectMixinTests(TestCase):

    fixtures = ['users.json', 'orgs.json']

    def setUp(self):
        self.foo = Organization.objects.get(name='Foo Fighters')
        self.dave = OrganizationUser.objects.get(user__username='dave',
                organization=self.foo)

    def test_get_org_object(self):
        class OrgView(OrganizationMixin, ViewStub):
            pass
        view = OrgView(organization_pk=self.foo.pk)
        self.assertEqual(view.get_object(), self.foo)

    def test_get_user_object(self):
        class UserView(OrganizationUserMixin, ViewStub):
            pass
        view = UserView(organization_pk=self.foo.pk, user_pk=self.dave.pk)
        self.assertEqual(view.get_object(), self.dave)
        self.assertEqual(view.get_organization(), self.foo)


class AccessMixinTests(TestCase):

    fixtures = ['users.json', 'orgs.json']

    def setUp(self):
        # add users (add them to request in methods)
        pass

    def test_member_access(self):
        pass

    def test_admin_access(self):
        pass

    def test_owner_access(self):
        pass


