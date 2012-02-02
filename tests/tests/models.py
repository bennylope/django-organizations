from django.test import TestCase

from testing_utils import AccountUserTestingMixin


class AccountModelsTest(TestCase, AccountUserTestingMixin):
    """
    Verify that the objects are created as intended, and that the managers
    return querysets as intended.
    """
    def setUp(self):
        from django.contrib.auth.models import User
        self.user = User.objects.create_user(
            username="tester",
            email="test@example.com"
        )

    def test_account_model(self):
        """Ensure that creating account w/ specific attributes doesn't fail"""
        from accounts.models import Account
        account = Account.objects.create(name="My test account")

    def test_create_account(self):
        """create_account method should create an account and an owner user"""
        from accounts.models import Account
        from accounts.utils import create_account
        new_account = create_account(
                name="My test account",
                owner=self.user)
        self.assertTrue(isinstance(new_account, Account))

        self.assertRaises(TypeError, 'create_user()',
                create_account, name="No owner")

    def test_active_manager(self):
        """Only return active accounts"""
        from accounts.models import Account
        account1 = Account.objects.create(name="My test account")
        account2 = Account.objects.create(name="My test account")
        account3 = Account.objects.create(name="My test account",
                is_active=False)
        self.assertEqual(2, len(Account.objects.active()))


class UserAccountRelationships(TestCase, AccountUserTestingMixin):
    """
    Test the expected relationship constraints between the Users, Accounts and
    AccountUsers. Should be able to get a queryset of all Accounts based on a
    single User object.
    """

    def setUp(self):
        from django.contrib.auth.models import User
        self.user = User.objects.create_user("user", "none",
                "user@example.com")
        self.seconduser = User.objects.create_user("jerk", "none",
        "second@example.com")

    def test_multiple_account_ownership(self):
        """Ensure that a User can be a member of and own multiple accounts"""
        from accounts.models import AccountUser
        from accounts.utils import create_account
        account1 = create_account(name="one", owner=self.user)
        account2 = create_account(name="two", owner=self.user)
        account3 = create_account(name="three", owner=self.seconduser)
        additional_account = AccountUser.objects.create(account=account3,
                user=self.user)


class AccountOwnership(TestCase, AccountUserTestingMixin):
    """
    Test the constraints on account ownership, ensure that a user can own
    multiple accounts, and make sure that ownership can be transferred, and
    that an account can't become an orphan. Make sure that only account users
    for the given account can be owners.
    """

    def setUp(self):
        from django.contrib.auth.models import User
        self.user = User.objects.create_user("user", "none",
                "user@example.com")
        self.seconduser = User.objects.create_user("lucy", "none",
                "second@example.com")
        self.thirduser = User.objects.create_user("bob", "none",
                "third@example.com")

    def test_manual_creation(self):
        """Just ensure no errors arise"""
        from accounts.models import Account, AccountUser, AccountOwner
        second_account = Account.objects.create(name="second")
        second_account_user = AccountUser.objects.create(
                account=second_account,
                user=self.seconduser,
        )
        second_account_owner = AccountOwner.objects.create(
                account=second_account,
                account_user=second_account_user
        )

    def test_one_account_owner(self):
        """Ensure only one account owner exists"""
        from django.db import IntegrityError
        from accounts.models import Account, AccountUser, AccountOwner
        from accounts.utils import create_account
        new_account = create_account(
                name="My test account",
                owner=self.user)
        # Account object creation is implied by owernship creation
        self.assertEqual(new_account.owner.account_user.user, self.user)

        new_account_user = AccountUser.objects.create(
                account=new_account,
                user=self.seconduser,
        )
        self.assertRaises(IntegrityError,
                AccountOwner.objects.create, **{
                    'account': new_account,
                    'account_user': new_account_user
                })

    def test_switch_account_owner(self):
        """Ensure that the account owner can be cleanly switched"""
        from accounts.models import AccountUser
        from accounts.utils import create_account, change_owner
        account = create_account(name="mytest", owner=self.user)
        secondary_user = AccountUser.objects.create(account=account,
                user=self.seconduser)
        new_owner = change_owner(account, secondary_user)
        self.assertEqual(new_owner.account_user, account.owner.account_user)

    def test_account_owner_is_member(self):
        """Ensure that the account owner must be a member of the group"""
        from accounts.models import AccountUser, AccountOwner
        from accounts.exceptions import AccountMismatch
        from accounts.utils import create_account

        account = create_account(name="mytest", owner=self.user)
        second_account = create_account(name="blah", owner=self.seconduser)
        second_account_user = AccountUser.objects.create(
                account=second_account, user=self.thirduser)

        first_owner = AccountOwner.objects.get(account=account)
        first_owner.account_user = second_account_user
        self.assertRaises(AccountMismatch, first_owner.save)

    def test_no_orphans(self):
        """Ensure that the account owner cannot be deleted"""
        from accounts.models import AccountUser
        from accounts.exceptions import OwnershipRequired
        from accounts.utils import create_account
        account = create_account(name="mytest", owner=self.user)
        secondary_user = AccountUser.objects.create(account=account,
                user=self.seconduser)
        owner_user = AccountUser.objects.get(account=account, user=self.user)
        self.assertRaises(OwnershipRequired, owner_user.delete)

    def test_account_user_delete(self):
        """Ensure special exceptions don't prohibit normal delete"""
        from accounts.models import AccountUser
        from accounts.utils import create_account
        account = create_account(name="mytest", owner=self.user)
        secondary_user = AccountUser.objects.create(account=account,
                user=self.seconduser)
        secondary_user.delete()

    def test_account_removal(self):
        """Ensure that deleting account removes account users"""
        from accounts.models import Account, AccountUser, AccountOwner
        from accounts.utils import create_account
        # Create an account
        account = create_account(name="mytest", owner=self.user)
        secondary_user = AccountUser.objects.create(account=account,
                user=self.seconduser)
        self.assertEqual(2, len(AccountUser.objects.filter(account=account)))

        account.delete()
        self.assertEqual(0, len(AccountUser.objects.filter(account=account)))


