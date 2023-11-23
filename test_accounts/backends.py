from organizations.backends.defaults import RegistrationBackend
from test_accounts.models import Account


class AccountRegistration(RegistrationBackend):
    def __init__(self, namespace=None):
        super().__init__(org_model=Account, namespace=namespace)
