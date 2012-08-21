from django.contrib.auth.models import User
from django.http import Http404
from django.test import TestCase
from django.test.client import RequestFactory
from django.test.utils import override_settings

from organizations.models import Organization
from organizations.tests.utils import request_factory_login
from organizations.views import (BaseOrganizationList, BaseOrganizationDetail,
        BaseOrganizationCreate, BaseOrganizationUpdate, BaseOrganizationDelete,
        BaseOrganizationUserList, BaseOrganizationUserDetail,
        BaseOrganizationUserCreate, BaseOrganizationUserUpdate,
        BaseOrganizationUserDelete, OrganizationSignup)


@override_settings(USE_TZ=True)
class BaseViewTests(TestCase):

    fixtures = ['users.json', 'orgs.json']

    def setUp(self):
        self.kurt = User.objects.get(username="kurt")
        self.dave = User.objects.get(username="dave")
        self.dummy = User.objects.create_user("dummy",
                email="dummy@example.com", password="test")
        self.nirvana = Organization.objects.get(name="Nirvana")
        self.factory = RequestFactory()
        self.kurt_request = request_factory_login(self.factory, self.kurt)
        self.dave_request = request_factory_login(self.factory, self.dave)
        self.anon_request = request_factory_login(self.factory)

    def test_org_list(self):
        """Ensure that the status code 200 is returned"""
        self.assertEqual(200, BaseOrganizationList(
                request=self.kurt_request).get(self.kurt_request).status_code)
        self.assertEqual(200, BaseOrganizationList(
                request=self.dave_request).get(self.dave_request).status_code)

    def test_org_list_queryset(self):
        """Ensure only active organizations belonging to the user are listed"""
        self.assertEqual(1, BaseOrganizationList(
                request=self.kurt_request).get_queryset().count())
        self.assertEqual(2, BaseOrganizationList(
                request=self.dave_request).get_queryset().count())

    def test_org_detail(self):
        kwargs = {'organization_pk': self.nirvana.pk}
        self.assertEqual(200, BaseOrganizationDetail(
            request=self.kurt_request, kwargs=kwargs).get(self.kurt_request,
                **kwargs).status_code)

    def test_org_create(self):
        self.assertEqual(200, BaseOrganizationCreate(
            request=self.kurt_request).get(self.kurt_request).status_code)

    def test_org_update(self):
        kwargs = {'organization_pk': self.nirvana.pk}
        self.assertEqual(200, BaseOrganizationUpdate(
            request=self.kurt_request, kwargs=kwargs).get(self.kurt_request,
                **kwargs).status_code)

    def test_org_delete(self):
        kwargs = {'organization_pk': self.nirvana.pk}
        self.assertEqual(200, BaseOrganizationDelete(
            request=self.kurt_request, kwargs=kwargs).get(self.kurt_request,
                **kwargs).status_code)

    def test_user_list(self):
        kwargs = {'organization_pk': self.nirvana.pk}
        self.assertEqual(200, BaseOrganizationUserList(
            request=self.kurt_request, kwargs=kwargs).get(self.kurt_request,
                **kwargs).status_code)

    def test_user_detail(self):
        kwargs = {'organization_pk': self.nirvana.pk, 'user_pk': self.kurt.pk}
        self.assertEqual(200, BaseOrganizationUserDetail(
            request=self.kurt_request, kwargs=kwargs).get(self.kurt_request,
                **kwargs).status_code)

    def test_bad_user_detail(self):
        kwargs = {'organization_pk': self.nirvana.pk, 'user_pk': self.dummy.pk}
        self.assertRaises(Http404, BaseOrganizationUserDetail(
            request=self.kurt_request, kwargs=kwargs).get, self.kurt_request,
                **kwargs)

    def test_user_create(self):
        kwargs = {'organization_pk': self.nirvana.pk}
        self.assertEqual(200, BaseOrganizationUserCreate(
            request=self.kurt_request, kwargs=kwargs).get(self.kurt_request,
                **kwargs).status_code)

    def test_user_update(self):
        kwargs = {'organization_pk': self.nirvana.pk, 'user_pk': self.kurt.pk}
        self.assertEqual(200, BaseOrganizationUserUpdate(
            request=self.kurt_request, kwargs=kwargs).get(self.kurt_request,
                **kwargs).status_code)

    def test_user_delete(self):
        kwargs = {'organization_pk': self.nirvana.pk, 'user_pk': self.kurt.pk}
        self.assertEqual(200, BaseOrganizationUserDelete(
            request=self.kurt_request, kwargs=kwargs).get(self.kurt_request,
                **kwargs).status_code)

    def test_signup(self):
        """Ensure logged in users are redirected"""
        self.assertEqual(302,
                OrganizationSignup(request=self.kurt_request).dispatch(
                self.kurt_request).status_code)
        self.assertEqual(200,
                OrganizationSignup(request=self.anon_request).dispatch(
                self.anon_request).status_code)
