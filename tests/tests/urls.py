from django.test import TestCase
from django.core.urlresolvers import reverse


class AccountURLsTest(TestCase):

    def test_account_list(self):
        reverse("account_list")

    def test_account_add(self):
        reverse("account_add")

    def test_account_detail(self):
        reverse("account_detail", kwargs={"account_pk": 1})

    def test_account_update(self):
        reverse("account_edit", kwargs={"account_pk": 1})

    def test_account_delete(self):
        reverse("account_delete", kwargs={"account_pk": 1})


class AccountUserURLsTest(TestCase):

    def test_accountuser_list(self):
        reverse("accountuser_list", kwargs={"account_pk": 1})

    def test_accountuser_add(self):
        reverse("accountuser_add", kwargs={"account_pk": 1})

    def test_accountuser_detail(self):
        reverse("accountuser_detail", kwargs={"account_pk": 1,
            "accountuser_pk": 1})

    def test_accountuser_update(self):
        reverse("accountuser_edit", kwargs={"account_pk": 1,
            "accountuser_pk": 1})

    def test_accountuser_delete(self):
        reverse("accountuser_delete", kwargs={"account_pk": 1,
            "accountuser_pk": 1})

