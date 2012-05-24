from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import login as login_view
from django.contrib.sites.models import get_current_site
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.utils.translation import ugettext as _
from django.views.generic import (View, ListView, DetailView, UpdateView,
        CreateView, DeleteView, FormView)

from organizations.models import Organization
from organizations.mixins import (OrganizationMixin, OrganizationUserMixin,
        MembershipRequiredMixin, AdminRequiredMixin, OwnerRequiredMixin)
from organizations.forms import (LoginForm, OrganizationForm, OrganizationUserForm,
        OrganizationUserAddForm, OrganizationAddForm, UserProfileForm)
from organizations.invitations.backends import InvitationBackend


class LoginView(FormView):
    """
    Performs the same actions as the default Django login view but also
    checks for a logged in user and redirects that person if s/he is
    logged in.
    """
    template_name = "organizations/login.html"
    form_class = LoginForm

    def get(self, request, *args, **kwargs):
        redirect_url = request.GET.get("next", settings.LOGIN_REDIRECT_URL)
        if request.user.is_authenticated():
            return HttpResponseRedirect(redirect_url)
        else:
            form = LoginForm(initial={"redirect_url": redirect_url})
            return self.render_to_response(self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        return login_view(request, redirect_field_name="redirect_url",
                authentication_form=LoginForm)


class LogoutView(View):
    """
    Logs the user out, and then redirects to the login view. It also
    updates the request messages with a message that the user has 
    successfully logged out.
    """

    def get(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.INFO, "You have successfully logged out.")
        return HttpResponseRedirect(reverse('login'))

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)


class BaseOrganizationList(ListView):
    model = Organization
    context_object_name = "organizations"

    def get_queryset(self):
        return super(BaseOrganizationList,
                self).get_queryset().filter(users=self.request.user)


class BaseOrganizationDetail(OrganizationMixin, DetailView):
    def get_context_data(self, **kwargs):
        context = super(BaseOrganizationDetail, self).get_context_data(**kwargs)
        context['organization_users'] = self.organization.organization_users.all()
        context['organization'] = self.organization
        return context


class BaseOrganizationCreate(CreateView):
    model = Organization
    form_class = OrganizationAddForm
    template_name = 'organizations/organization_form.html'

    def get_success_url(self):
        return reverse("organization_list")

    def get_form_kwargs(self):
        kwargs = super(BaseOrganizationCreate, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs


class BaseOrganizationUpdate(OrganizationMixin, UpdateView):
    form_class = OrganizationForm

    def get_form_kwargs(self):
        kwargs = super(BaseOrganizationUpdate, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs


class BaseOrganizationDelete(OrganizationMixin, DeleteView):
    def get_success_url(self):
        return reverse("organization_list")


class BaseOrganizationUserList(OrganizationMixin, ListView):
    def get(self, request, *args, **kwargs):
        self.organization = self.get_organization(**kwargs)
        self.object_list = self.organization.organization_users.all()
        allow_empty = self.get_allow_empty()
        if not allow_empty and len(self.object_list) == 0:
            raise Http404(_(u"Empty list and '%(class_name)s.allow_empty' is False.")
                          % {'class_name': self.__class__.__name__})
        context = self.get_context_data(organization_users=self.object_list,
                organization=self.organization)
        return self.render_to_response(context)


class BaseOrganizationUserDetail(OrganizationUserMixin, DetailView):
    pass


class BaseOrganizationUserCreate(OrganizationMixin, CreateView):
    form_class = OrganizationUserAddForm
    template_name = 'organizations/organizationuser_form.html'

    def get_success_url(self):
        return reverse('organization_user_list',
                kwargs={'organization_pk': self.object.organization.pk})

    def get_form_kwargs(self):
        kwargs = super(BaseOrganizationUserCreate, self).get_form_kwargs()
        kwargs.update({'organization': self.organization, 'request': self.request})
        return kwargs

    def get(self, request, *args, **kwargs):
        self.organization = self.get_object()
        return super(BaseOrganizationUserCreate, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.organization = self.get_object()
        return super(BaseOrganizationUserCreate, self).post(request, *args, **kwargs)


class BaseOrganizationUserRemind(OrganizationUserMixin, DetailView):
    template_name = 'organizations/organizationuser_remind.html'

    def get_object(self, **kwargs):
        self.organization_user = super(BaseOrganizationUserRemind, self).get_object()
        if self.organization_user.user.is_active:
            raise Http404(_("Already active")) # TODO add better error
        return self.organization_user

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        InvitationBackend().send_reminder(self.object.user,
                **{'domain': get_current_site(self.request),
                    'organization': self.organization, 'sender': request.user})
        return HttpResponseRedirect(self.object.get_absolute_url())


class BaseOrganizationUserUpdate(OrganizationUserMixin, UpdateView):
    form_class = OrganizationUserForm


class BaseOrganizationUserDelete(OrganizationUserMixin, DeleteView):
    def get_success_url(self):
        return reverse("organizationuser_list")


class OrganizationList(BaseOrganizationList):
    pass


class OrganizationCreate(BaseOrganizationCreate):
    pass


class OrganizationDetail(MembershipRequiredMixin, BaseOrganizationDetail):
    pass


class OrganizationUpdate(AdminRequiredMixin, BaseOrganizationUpdate):
    pass


class OrganizationDelete(OwnerRequiredMixin, BaseOrganizationDelete):
    pass


class OrganizationUserList(MembershipRequiredMixin, BaseOrganizationUserList):
    pass


class OrganizationUserDetail(AdminRequiredMixin, BaseOrganizationUserDetail):
    pass


class OrganizationUserUpdate(AdminRequiredMixin, BaseOrganizationUserUpdate):
    pass


class OrganizationUserCreate(AdminRequiredMixin, BaseOrganizationUserCreate):
    pass


class OrganizationUserRemind(AdminRequiredMixin, BaseOrganizationUserRemind):
    pass


class OrganizationUserDelete(AdminRequiredMixin, BaseOrganizationUserDelete):
    pass


class UserProfileView(UpdateView):
    form_class = UserProfileForm
    template_name = "organizations/organizationuser_form.html"

    def get_success_url(self):
        success_url = getattr(self, 'success_url')
        return success_url if success_url else reverse('user_profile')

    def get_object(self, **kwargs):
        return self.request.user

    def get_form_kwargs(self):
        kwargs = super(UserProfileView, self).get_form_kwargs()
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)
        context['profile'] = True
        return context
