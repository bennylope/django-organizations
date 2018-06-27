from django.contrib import admin

from test_accounts.models import Account
from test_accounts.models import AccountInvitation
from test_accounts.models import AccountOwner
from test_accounts.models import AccountUser

admin.site.register(Account)
admin.site.register(AccountInvitation)
admin.site.register(AccountUser)
admin.site.register(AccountOwner)
