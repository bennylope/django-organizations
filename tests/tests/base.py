from django.test import TestCase
from django.core.urlresolvers import reverse

from testing_utils import AccountUserTestingMixin


class BaseAccountUnauthViewTest(TestCase, AccountUserTestingMixin):
    """
    Ensure all views require logged in users
    """
    def setUp(self):
        self.get_fixtures()

    def test_account_list(self):
        response = self.client.get(reverse("base_account_list"))
        self.assertEqual(response.status_code, 302)

    def test_account_add(self):
        response = self.client.get(reverse("base_account_add"))
        self.assertEqual(response.status_code, 302)

    def test_account_detail(self):
        response = self.client.get(reverse("base_account_detail",
            kwargs={"account_pk": self.account1.pk}))
        self.assertEqual(response.status_code, 302)

    def test_account_update(self):
        response = self.client.get(reverse("base_account_edit",
            kwargs={"account_pk": self.account1.pk}))
        self.assertEqual(response.status_code, 302)

    def test_account_delete(self):
        response = self.client.get(reverse("base_account_delete",
            kwargs={"account_pk": self.account1.pk}))
        self.assertEqual(response.status_code, 302)

    def test_accountuser_list(self):
        response = self.client.get(reverse("base_accountuser_list",
            kwargs={"account_pk": self.account1.pk}))
        self.assertEqual(response.status_code, 302)

    def test_accountuser_add(self):
        response = self.client.get(reverse("base_accountuser_add",
            kwargs={"account_pk": self.account1.pk}))
        self.assertEqual(response.status_code, 302)

    def test_accountuser_detail(self):
        response = self.client.get(reverse("base_accountuser_detail", kwargs={
            "account_pk": self.account1.pk,
            "accountuser_pk": self.accountuser_1.pk}))
        self.assertEqual(response.status_code, 302)

    def test_accountuser_update(self):
        response = self.client.get(reverse("base_accountuser_edit", kwargs={
            "account_pk": self.account1.pk,
            "accountuser_pk": self.accountuser_1.pk}))
        self.assertEqual(response.status_code, 302)

    def test_accountuser_delete(self):
        response = self.client.get(reverse("base_accountuser_delete", kwargs={
            "account_pk": self.account1.pk,
            "accountuser_pk": self.accountuser_1.pk}))
        self.assertEqual(response.status_code, 302)


class BaseAccountViewTest(TestCase, AccountUserTestingMixin):
    """
    Verify GET requests on all views. This does not cover updates via POST
    requests.
    """
    def setUp(self):
        self.get_fixtures()
        self.client.login(username="user", password="pass")

    def test_account_list(self):
        response = self.client.get(reverse("base_account_list"))
        self.assertEqual(response.status_code, 200)

    def test_account_add(self):
        response = self.client.get(reverse("base_account_add"))
        self.assertEqual(response.status_code, 200)

    def test_account_detail(self):
        response = self.client.get(reverse("base_account_detail",
            kwargs={"account_pk": self.account1.pk}))
        self.assertEqual(response.status_code, 200)

    def test_account_update(self):
        response = self.client.get(reverse("base_account_edit",
            kwargs={"account_pk": self.account1.pk}))
        self.assertEqual(response.status_code, 200)

    def test_account_delete(self):
        response = self.client.get(reverse("base_account_delete",
            kwargs={"account_pk": self.account1.pk}))
        self.assertEqual(response.status_code, 200)

    def test_accountuser_list(self):
        response = self.client.get(reverse("base_accountuser_list",
            kwargs={"account_pk": self.account1.pk}))
        self.assertEqual(response.status_code, 200)

    def test_accountuser_add(self):
        response = self.client.get(reverse("base_accountuser_add",
            kwargs={"account_pk": self.account1.pk}))
        self.assertEqual(response.status_code, 200)

    def test_accountuser_detail(self):
        response = self.client.get(reverse("base_accountuser_detail", kwargs={
            "account_pk": self.account1.pk,
            "accountuser_pk": self.accountuser_1.pk}))
        self.assertEqual(response.status_code, 200)

    def test_accountuser_update(self):
        response = self.client.get(reverse("base_accountuser_edit", kwargs={
            "account_pk": self.account1.pk,
            "accountuser_pk": self.accountuser_1.pk}))
        self.assertEqual(response.status_code, 200)

    def test_accountuser_delete(self):
        response = self.client.get(reverse("base_accountuser_delete", kwargs={
            "account_pk": self.account1.pk,
            "accountuser_pk": self.accountuser_1.pk}))
        self.assertEqual(response.status_code, 200)


class BaseCreationViewsTest(TestCase, AccountUserTestingMixin):
    """
    Test the views for creating accounts and account users
    """
    def setUp(self):
        self.get_fixtures()
        self.client.login(username="user", password="pass")

    def test_simple_valid_account(self):
        """Ensure that basic creation view works"""
        from accounts.models import Account
        start_count = Account.objects.all().count()
        response = self.client.post(reverse("base_account_add"),
            data={"name": "Da Bears"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Account.objects.all().count(), start_count + 1)

    def test_simple_valid_accountuser(self):
        """Ensure that basic creation view works"""
        from accounts.models import AccountUser
        start_count = AccountUser.objects.all().count()
        post_data = {
            "username": "thedude",
            "first_name": "Jeffrey",
            "last_name": "Lebowski",
            "email": "jeff@bowlorama.com",
            "password": "roll",
        }
        response = self.client.post(reverse("base_accountuser_add",
            kwargs={"account_pk": 1}), data=post_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(AccountUser.objects.all().count(), start_count + 1)


class BaseDeletionViewsTest(TestCase, AccountUserTestingMixin):
    """
    Test the views for updating accounts and account users
    """
    def setUp(self):
        self.get_fixtures()
        self.client.login(username="user", password="pass")

    def test_simple_account_deletion(self):
        """Ensure that the account delete view deletes"""
        from accounts.models import Account
        start_count = Account.objects.all().count()
        response = self.client.post(reverse("base_account_delete",
            kwargs={"account_pk": 2}),data={"pk": 2})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Account.objects.all().count(), start_count - 1)


class BaseUpdateDeletionViewsTest(TestCase, AccountUserTestingMixin):
    """
    Test the views for deleting accounts and account users
    """
    def setUp(self):
        self.get_fixtures()
        self.client.login(username="user", password="pass")

    def test_simple_account_update(self):
        """Ensure that the account delete view deletes"""
        response = self.client.post(reverse("base_account_edit",
            kwargs={"account_pk": 2}),data={"pk": 2})
        self.assertEqual(response.status_code, 302)

    def test_simple_accountuser_update(self):
        """Ensure that the account delete view deletes"""
        response = self.client.post(reverse("base_accountuser_edit",
            kwargs={"account_pk": 2, "accountuser_pk": 1}),data={"pk": 2})
        self.assertEqual(response.status_code, 302)

