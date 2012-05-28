from django.conf import settings
from django.contrib import messages
from django.contrib.sites.models import get_current_site
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.utils.translation import ugettext as _
from django.views.generic import (ListView, DetailView, UpdateView, CreateView,
        DeleteView, FormView)

from organizations.models import Organization
from organizations.mixins import (OrganizationMixin, OrganizationUserMixin,
        MembershipRequiredMixin, AdminRequiredMixin, OwnerRequiredMixin)
from organizations.forms import (OrganizationForm, OrganizationUserForm,
        OrganizationUserAddForm, OrganizationAddForm)
from organizations.invitations.backends import InvitationBackend



class BaseOrganizationList(ListView):
    queryset = Organization.active.all()
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
    # TODO move to invitations backend?

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

