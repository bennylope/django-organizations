from django.test import TestCase
from django.core.urlresolvers import reverse


class BaseAccountURLsTest(TestCase):

    def test_account_list(self):
        reverse("base_account_list")

    def test_account_add(self):
        reverse("base_account_add")

    def test_account_detail(self):
        reverse("base_account_detail", kwargs={"account_pk": 1})

    def test_account_update(self):
        reverse("base_account_edit", kwargs={"account_pk": 1})

    def test_account_delete(self):
        reverse("base_account_delete", kwargs={"account_pk": 1})


class BaseAccountUserURLsTest(TestCase):

    def test_accountuser_list(self):
        reverse("base_accountuser_list", kwargs={"account_pk": 1})

    def test_accountuser_add(self):
        reverse("base_accountuser_add", kwargs={"account_pk": 1})

    def test_accountuser_detail(self):
        reverse("base_accountuser_detail", kwargs={"account_pk": 1,
            "accountuser_pk": 1})

    def test_accountuser_update(self):
        reverse("base_accountuser_edit", kwargs={"account_pk": 1,
            "accountuser_pk": 1})

    def test_accountuser_delete(self):
        reverse("base_accountuser_delete", kwargs={"account_pk": 1,
            "accountuser_pk": 1})

