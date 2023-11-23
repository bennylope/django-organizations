from django.contrib import admin

from .models import Account
from .models import AccountOwner
from .models import AccountUser

admin.site.register(Account)
admin.site.register(AccountUser)
admin.site.register(AccountOwner)
