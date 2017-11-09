# -*- coding: utf-8 -*-

# Copyright (c) 2012-2015, Ben Lopatin and contributors
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.  Redistributions in binary
# form must reproduce the above copyright notice, this list of conditions and the
# following disclaimer in the documentation and/or other materials provided with
# the distribution
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""Backend classes should provide common interface
"""

import email.utils
import inspect
import uuid

from django.conf import settings
from django.conf.urls import url
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import redirect
from django.shortcuts import render
from django.template import loader
from django.utils.translation import ugettext as _

from organizations.backends.forms import UserRegistrationForm
from organizations.backends.forms import org_registration_form
from organizations.backends.tokens import RegistrationTokenGenerator
from organizations.utils import create_organization
from organizations.utils import default_org_model
from organizations.utils import model_field_attr


class BaseBackend(object):
    """
    Base backend class for registering and inviting users to an organization
    """
    registration_form_template = 'organizations/register_form.html'
    activation_success_template = 'organizations/register_success.html'

    def __init__(self, org_model=None):
        self.user_model = get_user_model()
        self.org_model = org_model or default_org_model()

    def get_urls(self):
        raise NotImplementedError

    def get_success_url(self):
        """Will return the class's `success_url` attribute unless overridden"""
        raise NotImplementedError

    def get_form(self, **kwargs):
        """Returns the form for registering or inviting a user"""
        if not hasattr(self, 'form_class'):
            raise AttributeError(_("You must define a form_class"))
        return self.form_class(**kwargs)

    def get_token(self, user, **kwargs):
        """Returns a unique token for the given user"""
        return RegistrationTokenGenerator().make_token(user)

    def get_username(self):
        """
        Returns a UUID-based 'random' and unique username.

        This is required data for user models with a username field.
        """
        return str(uuid.uuid4())[:model_field_attr(self.user_model, 'username', 'max_length')]

    def activate_organizations(self, user):
        """
        Activates the related organizations for the user.

        It only activates the related organizations by model type - that is, if
        there are multiple types of organizations then only organizations in
        the provided model class are activated.
        """
        try:
            relation_name = self.org_model().user_relation_name
        except TypeError:
            # No org_model specified, raises a TypeError because NoneType is
            # not callable. This the most sensible default:
            relation_name = "organizations_organization"
        organization_set = getattr(user, relation_name)
        for org in organization_set.filter(is_active=False):
            org.is_active = True
            org.save()

    def activate_view(self, request, user_id, token):
        """
        View function that activates the given User by setting `is_active` to
        true if the provided information is verified.
        """
        try:
            user = self.user_model.objects.get(id=user_id, is_active=False)
        except self.user_model.DoesNotExist:
            raise Http404(_("Your URL may have expired."))
        if not RegistrationTokenGenerator().check_token(user, token):
            raise Http404(_("Your URL may have expired."))
        form = self.get_form(data=request.POST or None, instance=user)
        if form.is_valid():
            form.instance.is_active = True
            user = form.save()
            user.set_password(form.cleaned_data['password'])
            user.save()
            self.activate_organizations(user)
            user = authenticate(username=form.cleaned_data['username'],
                    password=form.cleaned_data['password'])
            login(request, user)
            return redirect(self.get_success_url())
        return render(request, self.registration_form_template, {'form': form})

    def send_reminder(self, user, sender=None, **kwargs):
        """Sends a reminder email to the specified user"""
        if user.is_active:
            return False
        token = RegistrationTokenGenerator().make_token(user)
        kwargs.update({'token': token})
        self.email_message(user, self.reminder_subject, self.reminder_body, sender, **kwargs).send()

    def email_message(self, user, subject_template, body_template,
            sender=None, message_class=EmailMessage, **kwargs):
        """
        Returns an email message for a new user. This can be easily overriden.
        For instance, to send an HTML message, use the EmailMultiAlternatives message_class
        and attach the additional conent.
        """
        if sender:
            from_email = "%s %s <%s>" % (sender.first_name, sender.last_name,
                    email.utils.parseaddr(settings.DEFAULT_FROM_EMAIL)[1])
            reply_to = "%s %s <%s>" % (sender.first_name, sender.last_name, sender.email)
        else:
            from_email = settings.DEFAULT_FROM_EMAIL
            reply_to = from_email

        headers = {'Reply-To': reply_to}
        kwargs.update({'sender': sender, 'user': user})

        subject_template = loader.get_template(subject_template)
        body_template = loader.get_template(body_template)
        subject = subject_template.render(kwargs).strip()  # Remove stray newline characters
        body = body_template.render(kwargs)
        return message_class(subject, body, from_email, [user.email], headers=headers)


class RegistrationBackend(BaseBackend):
    """
    A backend for allowing new users to join the site by creating a new user
    associated with a new organization.
    """
    # NOTE this backend stands to be simplified further, as email verification
    # should be beyond the purview of this app
    activation_subject = 'organizations/email/activation_subject.txt'
    activation_body = 'organizations/email/activation_body.html'
    reminder_subject = 'organizations/email/reminder_subject.txt'
    reminder_body = 'organizations/email/reminder_body.html'
    form_class = UserRegistrationForm

    def get_success_url(self):
        return reverse('registration_success')

    def get_urls(self):
        return [
            url(r'^complete/$', view=self.success_view,
                name="registration_success"),
            url(r'^(?P<user_id>[\d]+)-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
                view=self.activate_view, name="registration_register"),
            url(r'^$', view=self.create_view, name="registration_create"),
        ]

    def register_by_email(self, email, sender=None, request=None, **kwargs):
        """
        Returns a User object filled with dummy data and not active, and sends
        an invitation email.
        """
        try:
            user = self.user_model.objects.get(email=email)
        except self.user_model.DoesNotExist:
            user = self.user_model.objects.create(username=self.get_username(),
                    email=email, password=self.user_model.objects.make_random_password())
            user.is_active = False
            user.save()
        self.send_activation(user, sender, **kwargs)
        return user

    def send_activation(self, user, sender=None, **kwargs):
        """
        Invites a user to join the site
        """
        if user.is_active:
            return False
        token = self.get_token(user)
        kwargs.update({'token': token})
        self.email_message(user, self.activation_subject, self.activation_body, sender, **kwargs).send()

    def create_view(self, request):
        """
        Initiates the organization and user account creation process
        """
        if request.user.is_authenticated():
            return redirect("organization_add")
        form = org_registration_form(self.org_model)(request.POST or None)
        if form.is_valid():
            try:
                user = self.user_model.objects.get(email=form.cleaned_data['email'])
            except self.user_model.DoesNotExist:
                user = self.user_model.objects.create(username=self.get_username(),
                        email=form.cleaned_data['email'],
                        password=self.user_model.objects.make_random_password())
                user.is_active = False
                user.save()
            else:
                return redirect("organization_add")
            organization = create_organization(user, form.cleaned_data['name'],
                    form.cleaned_data['slug'], is_active=False)
            return render(request, self.activation_success_template, {'user': user, 'organization': organization})
        return render(request, self.registration_form_template, {'form': form})

    def success_view(self, request):
        return render(request, self.activation_success_template, {})


class InvitationBackend(BaseBackend):
    """
    A backend for inviting new users to join the site as members of an
    organization.
    """
    notification_subject = 'organizations/email/notification_subject.txt'
    notification_body = 'organizations/email/notification_body.html'
    invitation_subject = 'organizations/email/invitation_subject.txt'
    invitation_body = 'organizations/email/invitation_body.html'
    reminder_subject = 'organizations/email/reminder_subject.txt'
    reminder_body = 'organizations/email/reminder_body.html'
    form_class = UserRegistrationForm

    def get_success_url(self):
        # TODO get this url name from an attribute
        return reverse('organization_list')

    def get_urls(self):
        # TODO enable naming based on a model?
        return [
            url(r'^(?P<user_id>[\d]+)-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
                view=self.activate_view, name="invitations_register"),
        ]

    def invite_by_email(self, email, sender=None, request=None, **kwargs):
        """Creates an inactive user with the information we know and then sends
        an invitation email for that user to complete registration.

        If your project uses email in a different way then you should make to
        extend this method as it only checks the `email` attribute for Users.
        """
        try:
            user = self.user_model.objects.get(email=email)
        except self.user_model.DoesNotExist:
            # TODO break out user creation process
            if 'username' in inspect.getargspec(self.user_model.objects.create_user).args:
                user = self.user_model.objects.create(username=self.get_username(),
                        email=email, password=self.user_model.objects.make_random_password())
            else:
                user = self.user_model.objects.create(email=email,
                        password=self.user_model.objects.make_random_password())
            user.is_active = False
            user.save()
        self.send_invitation(user, sender, **kwargs)
        return user

    def send_invitation(self, user, sender=None, **kwargs):
        """An intermediary function for sending an invitation email that
        selects the templates, generating the token, and ensuring that the user
        has not already joined the site.
        """
        if user.is_active:
            return False
        token = self.get_token(user)
        kwargs.update({'token': token})
        self.email_message(user, self.invitation_subject, self.invitation_body, sender, **kwargs).send()
        return True

    def send_notification(self, user, sender=None, **kwargs):
        """
        An intermediary function for sending an notification email informing
        a pre-existing, active user that they have been added to a new
        organization.
        """
        if not user.is_active:
            return False
        self.email_message(user, self.notification_subject, self.notification_body, sender, **kwargs).send()
        return True
