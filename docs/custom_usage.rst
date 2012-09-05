Customizing usage
=================

The use cases from which django-organizations originated included more complex
ways of determining access to the views as well as additional relationships to
organizations. The application is extensible with these use cases in mind.

Custom models
-------------

I'm not sure exactly what you're trying to do, but there are two basic ways of
going about this: one, directly using the Organization model and two, extending
it with your own account/group model.

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


This mixin implements the same restriction as the `AdminRequiredMixin` mixin
and adds an allowance for anyone who is a member of the service provider.
