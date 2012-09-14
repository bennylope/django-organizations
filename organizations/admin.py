from django.contrib import admin

from organizations.models import (Organization, OrganizationUser,
        OrganizationOwner)


class OwnerInline(admin.StackedInline):
    model = OrganizationOwner


class OrganizationAdmin(admin.ModelAdmin):
    inlines = [OwnerInline]
    list_display = ['name', 'is_active']
    prepopulated_fields = {"slug": ("name",)}

class OrganizationUserAdmin(admin.ModelAdmin):
    list_filter = ['organization']
    list_display = ['user', 'organization', 'is_admin']


class OrganizationOwnerAdmin(admin.ModelAdmin):
    list_filter = ['organization']


admin.site.register(Organization, OrganizationAdmin)
admin.site.register(OrganizationUser, OrganizationUserAdmin)
admin.site.register(OrganizationOwner, OrganizationOwnerAdmin)
