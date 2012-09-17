from django.contrib import admin

from organizations.models import (Organization, OrganizationUser,
        OrganizationOwner)


class OwnerInline(admin.StackedInline):
    model = OrganizationOwner

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "organization_user" and request._obj_:
            kwargs["queryset"] = OrganizationUser.objects.filter(organization=request._obj_)
        return super(OwnerInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

class OrganizationAdmin(admin.ModelAdmin):
    inlines = [OwnerInline]
    list_display = ['name', 'is_active']
    prepopulated_fields = {"slug": ("name",)}

    def get_form(self, request, obj=None, **kwargs):
        # just save obj reference for future processing in Inline
        request._obj_ = obj
        return super(OrganizationAdmin, self).get_form(request, obj, **kwargs)
        
class OrganizationUserAdmin(admin.ModelAdmin):
    list_filter = ['user', 'organization']
    list_display = ['user', 'organization', 'is_admin']
    search_fields = ['user__username', 'organization__name']

class OrganizationOwnerAdmin(admin.ModelAdmin):
    list_filter = ['organization']


admin.site.register(Organization, OrganizationAdmin)
admin.site.register(OrganizationUser, OrganizationUserAdmin)
admin.site.register(OrganizationOwner, OrganizationOwnerAdmin)
