Customizing usage
=================

The use cases from which django-organizations originated included more complex
ways of determining access to the views as well as additional relationships to
organizations. The application is extensible with these use cases in mind.

Custom models
-------------

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

View mixins
-----------

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
                return HttpResponseForbidden(_("Sorry, admins only"))
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
class definition. This has the benefit of explitness at the expense of
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
                return HttpResponseForbidden(_("Sorry, admins only"))
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

While this isn't recommended in your own proejct, the mixins in
django-organizations itself will err on the side of depending on composition
rather than inheritence from other mixins. This may require defining a mixin in
your own project that combines them for simplicity in your own views, but it
reduces the inheritence chain potentially making functionality more difficult
ot identify.
