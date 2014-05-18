from django.contrib import admin

from .models import Organization, OrganizationUser, OrganizationOwner


class OwnerInline(admin.StackedInline):
    model = OrganizationOwner
    raw_id_fields = ('organization_user',)


class OrganizationAdmin(admin.ModelAdmin):
    inlines = [OwnerInline]
    list_display = ['name', 'is_active']
    prepopulated_fields = {"slug": ("name",)}


class OrganizationUserAdmin(admin.ModelAdmin):
    list_display = ['user', 'organization', 'is_admin']
    raw_id_fields = ('user', 'organization')


class OrganizationOwnerAdmin(admin.ModelAdmin):
    raw_id_fields = ('organization_user', 'organization')


admin.site.register(Organization, OrganizationAdmin)
admin.site.register(OrganizationUser, OrganizationUserAdmin)
admin.site.register(OrganizationOwner, OrganizationOwnerAdmin)
