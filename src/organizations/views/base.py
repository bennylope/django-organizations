# -*- coding: utf-8 -*-

from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseGone
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import FormView
from django.views.generic import ListView
from django.views.generic import UpdateView

from organizations.backends import invitation_backend
from organizations.backends import registration_backend
from organizations.forms import OrganizationAddForm
from organizations.forms import OrganizationForm
from organizations.forms import OrganizationUserAddForm
from organizations.forms import OrganizationUserForm
from organizations.forms import SignUpForm
from organizations.utils import create_organization
from organizations.views.mixins import OrganizationMixin
from organizations.views.mixins import OrganizationUserMixin


class BaseOrganizationList(ListView):
    context_object_name = "organizations"

    def get_queryset(self):
        return self.org_model.active.filter(users=self.request.user)


class BaseOrganizationDetail(OrganizationMixin, DetailView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["organization_users"] = self.organization.organization_users.all()
        context["organization"] = self.organization
        return context


class BaseOrganizationCreate(CreateView):
    form_class = OrganizationAddForm
    template_name = "organizations/organization_form.html"

    def get_success_url(self):
        return reverse("organization_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"request": self.request})
        return kwargs


class BaseOrganizationUpdate(OrganizationMixin, UpdateView):
    form_class = OrganizationForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"request": self.request})
        return kwargs


class BaseOrganizationDelete(OrganizationMixin, DeleteView):
    def get_success_url(self):
        return reverse("organization_list")


class BaseOrganizationUserList(OrganizationMixin, ListView):
    def get(self, request, *args, **kwargs):
        self.organization = self.get_organization()
        self.object_list = self.organization.organization_users.all()
        context = self.get_context_data(
            object_list=self.object_list,
            organization_users=self.object_list,
            organization=self.organization,
        )
        return self.render_to_response(context)


class BaseOrganizationUserDetail(OrganizationUserMixin, DetailView):
    pass


class BaseOrganizationUserCreate(OrganizationMixin, CreateView):
    form_class = OrganizationUserAddForm
    template_name = "organizations/organizationuser_form.html"

    def get_success_url(self):
        return reverse(
            "organization_user_list",
            kwargs={"organization_pk": self.object.organization.pk},
        )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"organization": self.organization, "request": self.request})
        return kwargs

    def get(self, request, *args, **kwargs):
        self.organization = self.get_object()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.organization = self.get_object()
        return super().post(request, *args, **kwargs)


class BaseOrganizationUserRemind(OrganizationUserMixin, DetailView):
    """
    Reminder view for already-linked org users

    This is only applicable for invitation backends using the
    strategy the original "default" backend uses, which is to
    immediately add existing users to the organization after
    invite, but leave new users inactive until confirmation.

    """

    template_name = "organizations/organizationuser_remind.html"
    # TODO move to invitations backend?

    def get_success_url(self):
        return reverse(
            "organization_user_list",
            kwargs={"organization_pk": self.object.organization.pk},
        )

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user.is_active:
            return HttpResponseGone(_("User is already active"))
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user.is_active:
            return HttpResponseGone(_("User is already active"))
        invitation_backend().send_reminder(
            self.object.user,
            **{
                "domain": get_current_site(self.request),
                "organization": self.organization,
                "sender": request.user,
            }
        )
        return redirect(self.get_success_url())


class BaseOrganizationUserUpdate(OrganizationUserMixin, UpdateView):
    form_class = OrganizationUserForm


class BaseOrganizationUserDelete(OrganizationUserMixin, DeleteView):
    def get_success_url(self):
        return reverse(
            "organization_user_list",
            kwargs={"organization_pk": self.object.organization.pk},
        )


class OrganizationSignup(FormView):
    """
    View that allows unregistered users to create an organization account.

    It simply processes the form and then calls the specified registration
    backend.
    """

    form_class = SignUpForm
    template_name = "organizations/signup_form.html"
    # TODO get success from backend, because some backends may do something
    # else, like require verification
    backend = registration_backend()

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("organization_add")
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        if getattr(self, "success_url", None):
            return self.success_url
        raise ImproperlyConfigured(
            "{cls} must either have a `success_url` attribute defined"
            "or override `get_success_url`".format(cls=self.__class__.__name__)
        )

    def form_valid(self, form):
        """
        Register user and create the organization
        """
        user = self.backend.register_by_email(form.cleaned_data["email"])
        create_organization(
            user=user,
            name=form.cleaned_data["name"],
            slug=form.cleaned_data["slug"],
            is_active=False,
        )
        return redirect(self.get_success_url())


class ViewFactory:
    """
    A class that can create a faked 'module' with model specific views

    These views have NO access control applied.
    """

    def __init__(self, org_model):
        self.org_model = org_model

    @property
    def OrganizationList(self):
        klass = BaseOrganizationList
        klass.org_model = self.org_model
        return klass

    @property
    def OrganizationDetail(self):
        klass = BaseOrganizationDetail
        klass.org_model = self.org_model
        return klass

    @property
    def OrganizationCreate(self):
        klass = BaseOrganizationCreate
        klass.org_model = self.org_model
        return klass

    @property
    def OrganizationUpdate(self):
        klass = BaseOrganizationUpdate
        klass.org_model = self.org_model
        return klass

    @property
    def OrganizationDelete(self):
        klass = BaseOrganizationDelete
        klass.org_model = self.org_model
        return klass

    @property
    def OrganizationUserList(self):
        klass = BaseOrganizationUserList
        klass.org_model = self.org_model
        return klass

    @property
    def OrganizationUserDetail(self):
        klass = BaseOrganizationUserDetail
        klass.org_model = self.org_model
        return klass

    @property
    def OrganizationUserUpdate(self):
        klass = BaseOrganizationUserUpdate
        klass.org_model = self.org_model
        return klass

    @property
    def OrganizationUserCreate(self):
        klass = BaseOrganizationUserCreate
        klass.org_model = self.org_model
        return klass

    @property
    def OrganizationUserDelete(self):
        klass = BaseOrganizationUserDelete
        klass.org_model = self.org_model
        return klass

    @property
    def OrganizationUserRemind(self):
        klass = BaseOrganizationUserRemind
        klass.org_model = self.org_model
        return klass
