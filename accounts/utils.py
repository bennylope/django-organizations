from accounts.models import Account, AccountUser, AccountOwner

# TODO: manager method? override `create` or add this one
def create_account(name, owner):
    """
    Returns a new account, also creating an initial account user who is the
    owner.
    """
    account = Account.objects.create(name=name)
    new_user = AccountUser.objects.create(account=account, user=owner,
            is_admin=True)
    AccountOwner.objects.create(account=account, account_user=new_user)
    return account

