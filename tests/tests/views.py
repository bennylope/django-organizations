from django.test import TestCase
from django.core.urlresolvers import reverse

from testing_utils import AccountUserTestingMixin


class AccountUnauthViewTest(TestCase, AccountUserTestingMixin):
    """
    For unauthenticated users.

    Verify GET requests on all views. This does not cover updates via POST
    requests.
    """
    def setUp(self):
        self.get_fixtures()

    def test_account_list(self):
        response = self.client.get(reverse("account_list"))
        self.assertEqual(response.status_code, 302)

    def test_account_add(self):
        response = self.client.get(reverse("account_add"))
        self.assertEqual(response.status_code, 302)

    def test_account_detail(self):
        response = self.client.get(reverse("account_detail",
            kwargs={"account_pk": self.account1.pk}))
        self.assertEqual(response.status_code, 302)

    def test_account_update(self):
        response = self.client.get(reverse("account_edit",
            kwargs={"account_pk": self.account1.pk}))
        self.assertEqual(response.status_code, 302)

    def test_account_delete(self):
        response = self.client.get(reverse("account_delete",
            kwargs={"account_pk": self.account1.pk}))
        self.assertEqual(response.status_code, 302)

    def test_accountuser_list(self):
        response = self.client.get(reverse("accountuser_list",
            kwargs={"account_pk": self.account1.pk}))
        self.assertEqual(response.status_code, 302)

    def test_accountuser_add(self):
        response = self.client.get(reverse("accountuser_add",
            kwargs={"account_pk": self.account1.pk}))
        self.assertEqual(response.status_code, 302)

    def test_accountuser_detail(self):
        response = self.client.get(reverse("accountuser_detail", kwargs={
            "account_pk": self.account1.pk,
            "accountuser_pk": self.accountuser_1.pk}))
        self.assertEqual(response.status_code, 302)

    def test_accountuser_update(self):
        response = self.client.get(reverse("accountuser_edit", kwargs={
            "account_pk": self.account1.pk,
            "accountuser_pk": self.accountuser_1.pk}))
        self.assertEqual(response.status_code, 302)

    def test_accountuser_delete(self):
        response = self.client.get(reverse("accountuser_delete", kwargs={
            "account_pk": self.account1.pk,
            "accountuser_pk": self.accountuser_1.pk}))
        self.assertEqual(response.status_code, 302)


class AccountViewTest(TestCase, AccountUserTestingMixin):
    """
    For the account owner

    Verify GET requests on all views. This does not cover updates via POST
    requests.
    """
    def setUp(self):
        self.get_fixtures()
        self.client.login(username="user", password="pass")

    def test_account_list(self):
        response = self.client.get(reverse("account_list"))
        self.assertEqual(response.status_code, 200)

    def test_account_add(self):
        response = self.client.get(reverse("account_add"))
        self.assertEqual(response.status_code, 200)

    def test_account_detail(self):
        response = self.client.get(reverse("account_detail",
            kwargs={"account_pk": self.account1.pk}))
        self.assertEqual(response.status_code, 200)

    def test_account_update(self):
        response = self.client.get(reverse("account_edit",
            kwargs={"account_pk": self.account1.pk}))
        self.assertEqual(response.status_code, 200)

    def test_account_delete(self):
        response = self.client.get(reverse("account_delete",
            kwargs={"account_pk": self.account1.pk}))
        self.assertEqual(response.status_code, 200)

    def test_accountuser_list(self):
        response = self.client.get(reverse("accountuser_list",
            kwargs={"account_pk": self.account1.pk}))
        self.assertEqual(response.status_code, 200)

    def test_accountuser_add(self):
        response = self.client.get(reverse("accountuser_add",
            kwargs={"account_pk": self.account1.pk}))
        self.assertEqual(response.status_code, 200)

    def test_accountuser_detail(self):
        response = self.client.get(reverse("accountuser_detail", kwargs={
            "account_pk": self.account1.pk,
            "accountuser_pk": self.accountuser_1.pk}))
        self.assertEqual(response.status_code, 200)

    def test_accountuser_update(self):
        response = self.client.get(reverse("accountuser_edit", kwargs={
            "account_pk": self.account1.pk,
            "accountuser_pk": self.accountuser_1.pk}))
        self.assertEqual(response.status_code, 200)

    def test_accountuser_delete(self):
        response = self.client.get(reverse("accountuser_delete", kwargs={
            "account_pk": self.account1.pk,
            "accountuser_pk": self.accountuser_1.pk}))
        self.assertEqual(response.status_code, 200)


class AccountCreationViewsTest(TestCase, AccountUserTestingMixin):
    """
    Test the views for creating accounts and account users
    """
    def setUp(self):
        self.get_fixtures()


class AccountUpdateViewsTest(TestCase, AccountUserTestingMixin):
    """
    Test the views for updating accounts and account users
    """
    def setUp(self):
        self.get_fixtures()


class AccountDeletionViewsTest(TestCase, AccountUserTestingMixin):
    """
    Test the views for deleting accounts and account users
    """
    def setUp(self):
        self.get_fixtures()

