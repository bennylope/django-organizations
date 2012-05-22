from django.contrib import admin

from accounts.models import Account, AccountUser, AccountOwner


class OwnerInline(admin.StackedInline):
    model = AccountOwner


class AccountAdmin(admin.ModelAdmin):
    inlines = [OwnerInline]


class AccountUserAdmin(admin.ModelAdmin):
    pass


class AccountOwnerAdmin(admin.ModelAdmin):
    pass


admin.site.register(Account, AccountAdmin)
admin.site.register(AccountUser, AccountUserAdmin)
admin.site.register(AccountOwner, AccountOwnerAdmin)
