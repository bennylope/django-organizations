from django.contrib import admin

from accounts.models import Account, AccountUser, AccountOwner


class OwnerInline(admin.StackedInline):
    model = AccountOwner


class AccountAdmin(admin.ModelAdmin):
    inlines = [OwnerInline]
    list_display = ['name', 'is_active']


class AccountUserAdmin(admin.ModelAdmin):
    list_filter = ['account']
    list_display = ['user', 'is_admin']


class AccountOwnerAdmin(admin.ModelAdmin):
    list_filter = ['account']


admin.site.register(Account, AccountAdmin)
admin.site.register(AccountUser, AccountUserAdmin)
admin.site.register(AccountOwner, AccountOwnerAdmin)
