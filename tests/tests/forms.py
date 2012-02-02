from django.test import TestCase

from testing_utils import AccountUserTestingMixin


class AccountFormTest(TestCase, AccountUserTestingMixin):
    """
    The AccountForm should allow a user to easily create or edit an existing
    account. That includes updating or creating an account user.
    """
    def setUp(self):
        self.user, self.seconduser, self.thirduser = self.create_users()

    def test_duplicate_subdomain(self):
        """Subdomains must be unique or form is not valid"""
        from accounts.forms import AccountForm
        from accounts.utils import create_account
        account = create_account("First", self.user, subdomain="first")
        form = AccountForm(initial={
            "name": "My test",
            "subdomain": "first",
        })
        self.assertFalse(form.is_valid())

    def test_duplicate_domain(self):
        """Full domains must be unique or form is not valid"""
        from accounts.forms import AccountForm
        from accounts.utils import create_account
        account = create_account("First", self.user,
                domain="sub.example.com")
        form = AccountForm(initial={
            "name": "My test",
            "domain": "sub.example.com",
        })
        self.assertFalse(form.is_valid())

    def test_create_account_new_user(self):
        """Ensure valid when all fresh information"""
        pass

    def test_create_account_exist_user(self):
        """Ensure valid for existing user"""
        pass


class AccountUserFormTest(TestCase, AccountUserTestingMixin):
    """
    The AccountUserForm should allow a user to easily create or edit existing
    user. This includes underlying User information.
    """
    def setUp(self):
        pass

    def test_duplicate_user(self):
        """A form creating a duplicate User should not be valid"""
        pass
