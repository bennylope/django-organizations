
class AccountUserTestingMixin(object):
    """
    Common setup required for testing accounts
    """

    def create_users(self):
        from django.contrib.auth.models import User
        user = User.objects.create_user("user", "pass",
                "user@example.com")
        seconduser = User.objects.create_user("lucy", "pass",
                "second@example.com")
        thirduser = User.objects.create_user("bob", "pass",
                "third@example.com")
        fourthuser = User.objects.create_user("sue", "pass",
                "fourth@example.com")
        return user, seconduser, thirduser, fourthuser

    def create_accounts(self):
        from accounts.models import Account
        accountone = Account.objects.create(name="one")
        accounttwo= Account.objects.create(name="two")
        return accountone, accounttwo

    def get_fixtures(self):
        from accounts.models import AccountUser, AccountOwner
        users = self.create_users()
        self.account1, self.account2 = self.create_accounts()
        self.accountuser_1 = AccountUser.objects.create(
                user=users[0],
                account=self.account1)
        self.accountuser_2 = AccountUser.objects.create(
                user=users[1],
                account=self.account1)
        self.accountuser_3 = AccountUser.objects.create(
                user=users[2],
                account=self.account2)
        self.owner = AccountOwner.objects.create(
                account=self.account1,
                account_user=self.accountuser_1)

