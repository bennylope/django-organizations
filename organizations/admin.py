from django.contrib import admin
from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelChoiceField
from django.forms import ModelForm
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.translation import ugettext_lazy as _

from organizations.exceptions import OwnershipRequired
from organizations.models import (Organization, OrganizationUser,
        OrganizationOwner)

class OrganizationForm(ModelForm):
    class Meta:
        model = Organization

    organization_owner = forms.ModelChoiceField(queryset=User.objects.all())
    organization_users = forms.ModelMultipleChoiceField(queryset=User.objects.all(),
                                           widget=FilteredSelectMultiple(_('Users'),False,),
                                           help_text="Select users that will be members of this organization.")
    
    organization_admins = forms.ModelMultipleChoiceField(queryset=User.objects.all(),
                                           widget=FilteredSelectMultiple(_('Users'),False,),
                                           help_text="Select users that will be administrators of this organization. \
                                           Administrators are able to add and remove users.")

    def __init__(self, *args, **kwargs):
        super(OrganizationForm, self).__init__(*args, **kwargs)
        try:
            self.fields['organization_owner'].initial = self.instance.owner.organization_user.user
        except:
            pass
        try:           
            self.fields['organization_users'].initial = [x.user for x in self.instance.organization_users.filter(is_admin=False)]
        except:
            pass
        try:
            self.fields['organization_admins'].initial = [x.user for x in self.instance.organization_users.filter(is_admin=True)]
        except:
            pass
    
    def clean(self):
        import pdb
        pdb.set_trace()
        cleaned_data = super(OrganizationForm, self).clean()
        organization_owner = cleaned_data.get('organization_owner')
        organization_users = set(cleaned_data.get('organization_users', ''))    
        organization_admins = set(cleaned_data.get('organization_admins', ''))
        all_users = organization_users.union(organization_admins)
        if organization_owner not in all_users:
            raise forms.ValidationError("%s is the owner of this group. Assign a new owner before removing this user." % self.instance.owner.organization_user.user )
        return cleaned_data
 
    def save(self, *args, **kwargs):
        #save owner
        organization_user, created = OrganizationUser.objects.get_or_create(organization=self.instance, user=self.cleaned_data['organization_owner'])
        try:
            organization_owner = OrganizationOwner.objects.get(organization=self.instance)
            organization_owner.organization_user = organization_user
        except OrganizationOwner.DoesNotExist:
            organization_owner = OrganizationOwner(organization=self.instance, organization_user=organization_user)
        organization_owner.save()
        
        #save users
        form_users = set(self.cleaned_data['organization_users'])
        form_admins = set(self.cleaned_data['organization_admins'])
        form_all = form_users.union(form_admins)
        db_users = set([x.user for x in OrganizationUser.objects.filter(organization=self.instance, is_admin=False)])  
        db_admins = set([x.user for x in OrganizationUser.objects.filter(organization=self.instance, is_admin=True)])  
        db_all = db_users.union(db_admins)
        deleted_users = db_all.difference(form_all)
        new_or_changed_users = form_users.difference(db_users)
        new_or_changed_admins = form_admins.difference(db_admins)
        
        for user in deleted_users:
            OrganizationUser.objects.delete(organization=self.instance, user=user)

        for user in new_or_changed_users:
            try:
                organization_user = OrganizationUser.objects.get(organization=self.instance, user=user)
                organization_user.is_admin = False
                organization_user.save()
            except:
                organization_user = OrganizationUser.objects.create(organization=self.instance, user=user, is_admin=False)
        for user in new_or_changed_admins:
            try:
                organization_user = OrganizationUser.objects.get(organization=self.instance, user=user)
                organization_user.is_admin = True
                organization_user.save()
            except:
                organization_user = OrganizationUser.objects.create(organization=self.instance, user=user, is_admin=True)
        return super(OrganizationForm, self).save(*args, **kwargs)
        
class OrganizationAdmin(admin.ModelAdmin):
    form= OrganizationForm
    list_display = ['name', 'is_active']
    prepopulated_fields = {"slug": ("name",)}
    
class OrganizationUserAdmin(admin.ModelAdmin):
    list_filter = ['user', 'organization']
    list_display = ['user', 'organization', 'is_admin']
    search_fields = ['user__username', 'organization__name']

class OrganizationOwnerAdmin(admin.ModelAdmin):
    list_filter = ['organization']


admin.site.register(Organization, OrganizationAdmin)
admin.site.register(OrganizationUser, OrganizationUserAdmin)
admin.site.register(OrganizationOwner, OrganizationOwnerAdmin)
