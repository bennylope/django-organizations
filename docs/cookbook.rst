.. _cookbook:

=================================
Cooking with Django Organizations
=================================

This section aims to provide some clear examples of how to use build your
application with Django organizations. The out-of-the-box setup works but is
unlikely to meet your needs without some further customization.

Proxy models
============

The simplest way to customize an installation of Django organizations (with
respect to the database) is to modify only the Django admin interface to your
organizations.

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

Model admin definitions
~~~~~~~~~~~~~~~~~~~~~~~

::

    from django.contrib import admin
    from organizations.models import (Organization, OrganizationUser,
        OrganizationOwner)
    from .forms import UserAdminForm
    from .models import Account, AccountUser

    class AccountUserAdmin(admin.ModelAdmin):
        form = UserAdminForm()

    admin.site.unregister(Organization)
    admin.site.unregister(OrganizationUser)
    admin.site.unregister(OrganizationOwner)
    admin.site.register(Account)
    admin.site.register(AccountUser, AccountUserAdmin)

It's very simple. All it does is ensure that the default Organization model
interfaces are hidden and then substitute the form class on the AccountUser
admin.

That form is where the business all happens

The admin form class
~~~~~~~~~~~~~~~~~~~~

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

The `save` method only does a little bit more. There's some logic there for
populating the invitation email (more on that below) but mostly this just
updates the linked user, instead of just the link to the user.

Handling user invitations
~~~~~~~~~~~~~~~~~~~~~~~~~

Each invited user is sent an email with a unique registration link. On the
registration page they have the opportunity to update their name and create
their own password. One of the things this form does is prevent users from
changing their email address. There's no reason your own project needs to do
this, of course.::

    from django import forms
    from django.conf import settings
    from django.contrib.sites.models import Site
    from organizations.backends import invitation_backend
    from organizations.backends.forms import UserRegistrationForm
    from .models import PartnerUser

    class RegistrationForm(UserRegistrationForm):
        """
        Form class that allows a user to register after clicking through an
        invitation.
        """
        first_name = forms.CharField(max_length=30)
        last_name = forms.CharField(max_length=30)
        email = forms.EmailField(widget=forms.TextInput(
            attrs={'class': 'disabled', 'readonly': 'readonly'}))
        password = forms.CharField(max_length=128, widget=forms.PasswordInput)
        password_confirm = forms.CharField(max_length=128, widget=forms.PasswordInput)

        def clean(self):
            password = self.cleaned_data.get("password")
            password_confirm = self.cleaned_data.get("password_confirm")
            if password != password_confirm or not password:
                raise forms.ValidationError("Your password entries must match")
            return super(RegistrationForm, self).clean()

    class AccountUserForm(forms.ModelForm):
        # See above

.. TODO add backend specs

Custom org with simple inheritance
==================================

Simply extending the organization model with your own requires the least amount
of fuss and for most applications will probably suffice. This entails using the
stock `OrganizationUser` model and multi-table inheritance to support
additional fields on your organization model.

Models
------

Here's an example from a sport team management application.::

    from django.db import models
    from organizations.models import Organization
    from sports.models import Sport

    class Team(Organization):
        sport = models.ForeignKey(Sport, related_name="teams")
        city = models.CharField(max_length=100)

That's all that's required to update your models. The `Team` model will use the
default `OrganizationUser` and `OrganizationOwner` models.

Views
-----

The class based views can be configured to refer to different model classes and
context variable names by adding a view attributes in your own class or in the
`as_view` class method call.::

    class TeamDetail(BaseOrganizationDetail):
        org_model = Team
        org_context_name = 'team'

Multiple organizations with simple inheritance
==============================================

You can take the inheritance strategy one step further and add additional
organization classes if need be.::

    from django.db import models
    from organizations.models import Organization
    from sports.models import Sport

    class Association(Organization):
        sport = models.ForeignKey(Sport, related_name="associations")

    class Team(Organization):
        association = models.ForeignKey(Association, related_name="teams")
        city = models.CharField(max_length=100)

As in this example you can add them in the same app although it probably makes
more sense to add them in their own apps.

.. _cookbook-advanced:

Advanced customization
======================

As of version 0.2.0 you can add your own fully customized models using unique
table sets, i.e. single table inheritance. In order to do this, your app
should define an organization model, an organization user model, and an
organization owner model, each inheriting from one of the base classes as
follows. Here's an example from an `accounts` app::

    from django.db import models
    from organizations.base import (OrganizationBase, OrganizationUserBase,
            OrganizationOwnerBase)

    class Account(OrganizationBase):
        monthly_subscription = models.IntegerField(default=1000)

    class AccountUser(OrganizationUserBase):
        user_type = models.CharField(max_length=1, default='')

    class AccountOwner(OrganizationOwnerBase):
        pass

This will create the following tables:

* `accounts_account`
* `accounts_accountuser`
* `accounts_accountowner`

The `accounts_account` table will include all of the necessary fields for this
and only this organization model.

.. note::
    Unlike in the example of multi-table inheritance, you cannot add more than
    one custom organization model to an individual app. Each additional
    organization class you want must be defined in its own app.
    Only one organization set per app.

Difference between default models
---------------------------------

The abstract base models provide the almost-bare minimum fields required to
manage organizations. The default models are fairly spare, but include
timestamps, a slug field on the organization, and an `is_admin` field on the
organization user. The first two are implemented with additional dependencies.

If you want a slug field or timestamps on your models, you'll need to add those
in. However you can do so however you want. And if you don't want any of those
fields, you don't have to take them.
