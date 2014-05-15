=================================
Cooking with Django Organizations
=================================

This section aims to provide some clear examples of how to use build your
application with Django organizations. The out-of-the-box setup works but is
unlikely to meet your needs without some further customization.

Basic usage with proxy models
=============================

The simplest way to customize an installation of Django organizations is to
modify the Django admin interface to your organizations.

In this example, an organization model is provided in a site but the
organizations require a new name. Site admins should be able to add, edit, and
delete account organizations, as well as users for those accounts.

Proxy models for convenience
----------------------------

This can be accomplished with proxy models in your models module.::

    from organizations.models import Organization, OrganizationUser

    class Account(Organization):
        class Meta:
            proxy = True

    class AccountUser(OrganizationUser):
        class Meta:
            proxy = True

In your own models you could just add `verbose_name` and `verbose_name_plural`
attributes in your class's `Meta` class, but you'd have to extend those classes
here to do that anyhow. The `proxy` attribute ensures that this is just a
wrapper around the class and the database is not changed from the default tables.
Note that the `OrganizationOwner` is absent. In this particular example there's
no need to expose that separately.

User focused admin interface
----------------------------

The admin interface should allow a site admin to modify the organizations and
the site users. We want to avoid requiring site admins to separately manage
users through the `auth.User` or other user interface *and* an organization
interface. It seems convenient as a developer to just let site admins pick
users from the organization's many-to-many `users` field, but this is
cumbersome and doesn't factor in user invitations.

So the strategy here is to take advantage of the explicit through model's
organization foreign key and provide a limited user interface through the
account user form.

The admin definitions
~~~~~~~~~~~~~~~~~~~~~

::

    from django.contrib import admin
    from organizations.models import (Organization, OrganizationUser,
        OrganizationOwner)
    from .forms import UserAdminForm
    from .models import Account, AccountUser

    class AccountUserAdmin(admin.ModelAdmin):
        form = UserAdminForm()

    admin.site.unregsiter(Organization)
    admin.site.unregsiter(OrganizationUser)
    admin.site.unregsiter(OrganizationOwner)
    admin.site.register(Account)
    admin.site.register(AccountUser, AccountUserAdmin)

It's very simle. All it does is ensure that the default Organization model
interfaces are hidden and then substitute the form class on the AccountUser
admin.

That form is where the business all happens

The form class
~~~~~~~~~~~~~~

We'll go through this piece by piece, but here's the full class::

    from django import forms
    from django.conf import settings
    from django.contrib.sites.models import Site
    from .models import AccountUser

    class AccountUserForm(forms.ModelForm):
        """
        Form class for editing OrganizationUsers *and* the linked user model.
        """
        first_name = forms.CharField(max_length=100)
        last_name = forms.CharField(max_length=100)
        email = forms.EmailField()

        class Meta:
            exclude = ('user', 'is_admin')
            model = AccountUser

        def __init__(self, *args, **kwargs):
            super(AccountUserForm, self).__init__(*args, **kwargs)
            if self.instance.pk is not None:
                self.fields['first_name'].initial = self.instance.user.first_name
                self.fields['last_name'].initial = self.instance.user.last_name
                self.fields['email'].initial = self.instance.user.email

        def save(self, *args, **kwargs):
            """
            This method saves changes to the linked user model.
            """
            if self.instance.pk is None:
                site = Site.objects.get(pk=settings.SITE_ID)
                self.instance.user = invitation_backend().invite_by_email(
                        self.cleaned_data['email'],
                        **{'first_name': self.cleaned_data['first_name'],
                            'last_name': self.cleaned_data['last_name'],
                            'organization': self.cleaned_data['organization'],
                            'domain': site})
            self.instance.user.first_name = self.cleaned_data['first_name']
            self.instance.user.last_name = self.cleaned_data['last_name']
            self.instance.user.email = self.cleaned_data['email']
            self.instance.user.save()
            return super(AccountUserForm, self).save(*args, **kwargs)

**This is a model form class but primarily manages a linked model.**

The `AccountUser` model only has three fields: a foreign key to the
organization, a foreign key to the user, and since this is our default class, a
Boolean field for admins. The form will only show a choice for the
organization. Meanwhile, the site admin will have a chance to view and edit the
name and email address of the user, pulled from the underlying user model, e.g.
`auth.User`.

The `__init__` method is responsible for populating the form with the data for
existing account users. It calls the super method first which is necessary to
create the fields. It checks if the primary key is none, rather than testing
the attribute, since the attribute will be there whether or not the model has
been saved yet - it will just be a `NoneType`.

The `save` method is a bit more complex. There's some logic there for
populating the invitation email (more on that below) but mostly this just
updates the linked user, instead of just the link.

Inviting users
~~~~~~~~~~~~~~

Custom org with Simple inheritence
==================================


Mutliple organizations with simple inheritence
==============================================


Advanced customization
======================

* custom tables
* add'l attributes on org user
