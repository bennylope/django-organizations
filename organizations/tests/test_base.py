from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import RequestFactory

from organizations.tests.utils import request_factory_login
from organizations.views import (BaseOrganizationList,)


class BaseViewTests(TestCase):

    fixtures = ['users.json', 'orgs.json']

    def setUp(self):
        self.kurt = User.objects.get(username="kurt")
        self.dave = User.objects.get(username="dave")
        self.factory = RequestFactory()
        self.kurt_request = request_factory_login(self.factory, self.kurt)
        self.dave_request = request_factory_login(self.factory, self.dave)

    def test_get_org_list(self):

        self.assertEqual(200, BaseOrganizationList(
                request=self.kurt_request).get(self.kurt_request).status_code)
        self.assertEqual(200, BaseOrganizationList(
                request=self.dave_request).get(self.dave_request).status_code)
        self.assertEqual(1, BaseOrganizationList(
                request=self.kurt_request).get_queryset().count())
        self.assertEqual(2, BaseOrganizationList(
                request=self.dave_request).get_queryset().count())

    def test_get_org_detail(self):
        pass

    def test_get_org_create(self):
        pass

    def test_get_org_update(self):
        pass

    def test_get_org_delete(self):
        pass

    def test_get_user_list(self):
        pass

    def test_get_user_detail(self):
        pass

    def test_get_user_create(self):
        pass

    def test_get_user_update(self):
        pass

    def test_get_user_delete(self):
        pass
