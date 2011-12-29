from accounts.models import Account, AccountUser, AccountOwner


def create_account(name, owner, subdomain=None, domain=None):
    """
    Returns a new account, also creating an initial account user who is the
    owner.
    """
    account = Account.objects.create(name=name)
    new_user = AccountUser.objects.create(account=account, user=owner)
    new_owner = AccountOwner.objects.create(account=account, account_user=new_user)
    return account


def change_owner(account, owner):
    """
    Switches the account ownership to the new account user
    """
    account.owner.account_user = owner
    account.owner.save()
    return account.owner
