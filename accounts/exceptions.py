class OwnershipRequired(Exception):
    """
    Exception to raise if the account owner is being removed before the
    account.
    """
    pass


class AccountMismatch(Exception):
    """
    Exception to raise if an account user from a different account is assigned
    to be an account's owner.
    """
    pass
