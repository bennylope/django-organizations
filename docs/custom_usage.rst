==============================
Customizing your organizations
==============================

The use cases from which django-organizations originated included more complex
ways of determining access to the views as well as additional relationships to
organizations. The application is extensible with these use cases in mind.

.. _custom-organization-model:

Custom organization models
==========================

Let's say you had an Account model in your app, which defined a group account
to which multiple users could belong, and also had its own logo, a foreign key
to a subscription plan, a website URL, and some descriptive information. Also,
this client organization is related to a service provider organization.::

    class ServiceProvider(Organization):
        """Now this model has a name field and a slug field"""
        url = models.URLField()


    class Client(Organization):
        """Now this model has a name field and a slug field"""
        service_provider = models.ForeignKey(ServiceProvider,
                related_name="clients")
        subscription_plan = models.ForeignKey(SubscriptionPlan)
        subscription_start = models.DateField()
        url = models.URLField()
        description = models.TextField()

        objects = models.Manager()

Now the `ServiceProvider` and `Client` objects you create have the attributes
of the Organization model class, including access to the OrganizationUser and
OrganizationOwner models.  This is an indirect relationship through a join in
the database - this type of inheritance is multi-table inheritance so there
will be a Client table and an Organization table; the latter is what the
OrganizationUser and OrganizationOwner tables are still linked to.

.. _custom-user-model:

Custom user model
=================

By default django-organizations will map User objects from django's
`contrib.auth` application to an Organization. However you can change this by
specifying a different model in your settings using the `AUTH_USER_MODEL`
setting. This should include the appname and model name in a string like so::

    AUTH_USER_MODEL = 'auth.User'

or::

    AUTH_USER_MODEL = 'myapp.MyUser'

.. note::
    If you choose a different user class make sure to pay attention to the API.
    If it differs from the `auth.User` API you will likely need to use an
    extended backend, if you are not already.

This is worth noting here because Django Organizations is compatible with
different user models in Django 1.4, which preceds the official swappable users
feature in Django 1.4.

.. _mixins:

View mixins
===========

Common use cases for extending the views include updating context variable
names, adding project specific functionality, or updating access controls based
on your project::

    class ServiceProvidersOnly(LoginRequired, OrganizationMixin):
        def dispatch(self, request, *args, **kwargs):
            self.request = request
            self.args = args
            self.kwargs = kwargs
            self.organization = self.get_organization()
            self.service_provider = self.organization.provider
            if not self.organization.is_admin(request.user) and not \
                    self.service_provider.is_member(request.user):
                raise PermissionDenied(_("Sorry, admins only"))
            return super(AdminRequiredMixin, self).dispatch(request, *args,
                    **kwargs)


This mixin implements the same restriction as the `AdminRequiredMixin` mixin
and adds an allowance for anyone who is a member of the service provider::

    class AccountUpdateView(ServiceProviderOnly, BaseOrganizationUpdate):
        context_object_name = "account"
        template_name = "myapp/account_detail.html"

        def get_context_data(self, **kwargs):
            context = super(AccountUpdateView, self).get_context_data(**kwargs)
            context.update(provider=self.service_provider)
            return context

The `ServiceProvidersOnly` mixin inherits from the `LoginRequired` class which
is a mixin for applying the `login_required` decorator. You can write your own
(it's fairly simple) or use the convenient mixins provided by `django-braces
<http://django-braces.readthedocs.org/en/latest/index.html>`_.

It would also have been possible to define the `ServiceProvidersOnly` without
inheriting from a base class, and then defining all of the mixins in the view
class definition. This has the benefit of explicitness at the expense of
verbosity::

    class ServiceProvidersOnly(object):
        def dispatch(self, request, *args, **kwargs):
            self.request = request
            self.args = args
            self.kwargs = kwargs
            self.organization = self.get_organization()
            self.service_provider = self.organization.provider
            if not self.organization.is_admin(request.user) and not \
                    self.service_provider.is_member(request.user):
                raise PermissionDenied(_("Sorry, admins only"))
            return super(AdminRequiredMixin, self).dispatch(request, *args,
                    **kwargs)


    class AccountUpdateView(LoginRequired, OrganizationMixin,
                        ServiceProviderOnly, BaseOrganizationUpdate):
        context_object_name = "account"
        template_name = "myapp/account_detail.html"

        def get_context_data(self, **kwargs):
            context = super(AccountUpdateView, self).get_context_data(**kwargs)
            context.update(provider=self.service_provider)
            return context

While this isn't recommended in your own project, the mixins in
django-organizations itself will err on the side of depending on composition
rather than inheritance from other mixins. This may require defining a mixin in
your own project that combines them for simplicity in your own views, but it
reduces the inheritance chain potentially making functionality more difficult
ot identify.

.. note::
    The view mixins expressly allow superusers to access organization
    resources. If this is undesired behavior you will need to use your own
    mixins.


User registration and invitations
=================================

User registration and invitation plays an important role in how you will actually use
Django Organizations, but it is a relatively minor aspect of the app. The default backends
for both registration and invitation try to provide as little functionality to
accomplish the task for most scenarios. These can be extended and customized in
your own project provided that you expose a few consistent interfaces.

Creating the backend
--------------------

Here we'll create a slightly modified invitation backend. The default backend
presumes that your user model has a `username` attribute. If you're simply
using the email address as your user identifier with a custom user model, this
field might be missing.

The default `invite_by_email` method - which is part of
the exposed interface - sends an invitation to the user based on the email
address, and creates an inactive user account if there is no matching user. It
satisfies the `auth.User` username's not null condition by filling the field
with the contents of a freshly generated UUID.

In the example accounts app you would create a file named `backends.py`.::

    from organizations.backends.defaults import InvitationBackend


    class CustomInvitations(InvitationBackend):
        def invite_by_email(self, email, sender=None, request=None, **kwargs):
          try:
              user = self.user_model.objects.get(email=email)
          except self.user_model.DoesNotExist:
              user = self.user_model.objects.create(email=email,
                      password=self.user_model.objects.make_random_password())
              user.is_active = False
              user.save()
          self.send_invitation(user, sender, **kwargs)
          return user


This removes the username from the `create` method.

Configuring the backend
-----------------------

In your settings file you will need to specify that your backend should be
used::

    INVITATION_BACKEND = 'accounts.backends.CustomInvitations'

Your URLs can be configured as normal::

    from organizations.backends import invitation_backend

    urlpatterns = [
        ...
        url(r'^invite/', include(invitation_backend().get_urls())),
    ]

The `invitation_backend` function simply returns the URL patterns from the
`get_urls` method of the specified backend.
