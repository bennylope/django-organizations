
class AccountUserTestingMixin(object):
    """
    Common setup required for testing accounts
    """

    def create_users(self):
        from django.contrib.auth.models import User
        self.user = User.objects.create_user(username="user", email="", password="pass")
        self.seconduser = User.objects.create_user(username="lucy", email="", password="pass")
        self.thirduser = User.objects.create_user(username="bob", email="", password="pass")
        self.fourthuser = User.objects.create_user(username="sue", email="", password="pass")
        return self.user, self.seconduser, self.thirduser, self.fourthuser

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

