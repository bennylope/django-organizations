import uuid

from django.conf import settings
from django.conf.urls.defaults import patterns, url
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.exceptions import ImproperlyConfigured
from django.core.mail import EmailMessage
from django.http import Http404
from django.shortcuts import render, redirect
from django.template import Context, loader
from django.utils.translation import ugettext as _

from organizations.backends.tokens import RegistrationTokenGenerator
from organizations.backends.forms import (UserRegistrationForm,
        OrganizationRegistrationForm)
from organizations.utils import create_organization
from organizations.utils import model_field_attr


# Backend classes should provide common interface


class BaseBackend(object):
    """Base backend class for registering and inviting users to an organization
    """

    def get_urls(self):
        raise NotImplementedError

    def get_success_url(self):
        """Will return the class's `success_url` attribute unless overridden"""
        raise NotImplementedError

    def get_form(self, **kwargs):
        """Returns the form for registering or inviting a user"""
        if not hasattr(self, 'form_class'):
            raise AttributeError("You must define a form_class")
        return self.form_class(**kwargs)

    def get_token(self, user, **kwargs):
        """Returns a unique token for the given user"""
        return RegistrationTokenGenerator().make_token(user)

    def get_username(self):
        """Returns an UUID based 'random' and unique username"""
        return unicode(uuid.uuid4())[:model_field_attr(User, 'username', 'max_length')]

    def activate_view(self, request, user_id, token):
        """
        Activates the given User by setting `is_active` to true if the provided
        information is verified.
        """
        try:
            user = User.objects.get(id=user_id, is_active=False)
        except User.DoesNotExist:
            raise Http404(_("Your URL may have expired."))
        if not RegistrationTokenGenerator().check_token(user, token):
            raise Http404(_("Your URL may have expired."))
        form = self.get_form(data=request.POST or None, instance=user)
        if form.is_valid():
            form.instance.is_active = True
            user = form.save()
            user.set_password(form.cleaned_data['password'])
            user.save()
            user = authenticate(username=form.cleaned_data['username'],
                    password=form.cleaned_data['password'])
            login(request, user)
            return redirect(self.get_success_url())
        return render(request, 'organizations/register_form.html',
                {'form': form})

    def send_reminder(self, user, sender=None, **kwargs):
        """Sends a reminder email to the specified user"""
        if user.is_active:
            return False
        token = RegistrationTokenGenerator().make_token(user)
        kwargs.update({'token': token})
        self._send_email(user, self.reminder_subject, self.reminder_body,
                sender, **kwargs)

    def _send_email(self, user, subject_template, body_template,
            sender=None, **kwargs):
        """Utility method for sending emails to new users"""
        try:
            from_email = settings.DEFAULT_FROM_EMAIL
        except AttributeError:
            raise ImproperlyConfigured(_("You must define DEFAULT_FROM_EMAIL in your settings"))

        if sender:
            from_email = "%s %s <%s>" % (sender.first_name, sender.last_name,
                    from_email)
            reply_to = "%s %s <%s>" % (sender.first_name, sender.last_name,
                    sender.email)
        headers = {'Reply-To': reply_to} if sender else {}

        kwargs.update({'sender': sender, 'user': user})
        ctx = Context(kwargs)

        subject_template = loader.get_template(subject_template)
        body_template = loader.get_template(body_template)
        subject = subject_template.render(ctx).strip() # Remove stray newline characters
        body = body_template.render(ctx)
        return EmailMessage(subject, body, from_email, [user.email],
                headers).send()


class RegistrationBackend(BaseBackend):
    """A backend for allowing new users to join the site by creating a new user
    associated with a new organization.
    """
    activation_subject = 'organizations/email/activation_subject.txt'
    activation_body = 'organizations/email/activation_body.html'
    reminder_subject = 'organizations/email/reminder_subject.txt'
    reminder_body = 'organizations/email/reminder_body.html'
    form_class = UserRegistrationForm

    def get_success_url(self):
        return reverse('registration_success')

    def get_urls(self):
        return patterns('',
            url(r'^complete/$', view=self.success_view,
                name="registration_success"),
            url(r'^(?P<user_id>[\d]+)-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
                view=self.activate_view, name="registration_register"),
            url(r'^$', view=self.create_view, name="registration_create"),
            )

    def register_by_email(self, email, sender=None, request=None, **kwargs):
        """
        Returns a User object filled with dummy data and not active, and sends
        an invitation email.
        """
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = User.objects.create(username=self.get_username(), email=email,
                    password=User.objects.make_random_password())
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
        self._send_email(user, self.activation_subject, self.activation_body,
                sender, **kwargs)

    def create_view(self, request):
        """
        Initiates the organization and user account creation process
        """
        if request.user.is_authenticated():
            return redirect("organization_add")
        form = OrganizationRegistrationForm(request.POST or None)
        if form.is_valid():
            try:
                user = User.objects.get(email=form.cleaned_data['email'])
            except User.DoesNotExist:
                user = User.objects.create(username=self.get_username(),
                        email=form.cleaned_data['email'],
                        password=User.objects.make_random_password())
                user.is_active = False
                user.save()
            else:
                return redirect("organization_add")
            organization = create_organization(user, form.cleaned_data['name'],
                    form.cleaned_data['slug'], is_active=False)
            return render(request, 'organizations/register_success.html',
                    {'user': user, 'organization': organization})
        return render(request, 'organizations/register_form.html',
                {'form': form})

    def success_view(self, request):
        return render(request, 'organizations/register_success.html', {})


class InvitationBackend(BaseBackend):
    """A backend for inviting new users to join the site as members of an
    organization.
    """
    invitation_subject = 'organizations/email/invitation_subject.txt'
    invitation_body = 'organizations/email/invitation_body.html'
    reminder_subject = 'organizations/email/reminder_subject.txt'
    reminder_body = 'organizations/email/reminder_body.html'
    form_class = UserRegistrationForm

    def get_success_url(self):
        return reverse('organization_list')

    def get_urls(self):
        return patterns('',
            url(r'^(?P<user_id>[\d]+)-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
                view=self.activate_view, name="invitations_register"),
            )

    def invite_by_email(self, email, sender=None, request=None, **kwargs):
        """Creates an inactive user with the information we know and then sends
        an invitation email for that user to complete registration.

        If your project uses email in a different way then you should make to
        extend this method as it only checks the `email` attribute for Users.
        """
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = User.objects.create(username=self.get_username(),
                    email=email, password=User.objects.make_random_password())
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
        self._send_email(user, self.invitation_subject, self.invitation_body,
                sender, **kwargs)

class NotificationBackend(BaseBackend):
    """A backend for notifying existing users that they have been added an
    organization.
    """
    notification_subject = 'organizations/email/notification_subject.txt'
    notification_body = 'organizations/email/notification_body.html'
    
    def notify_by_email(self, email, sender=None, request=None, **kwargs):
        """Sends an active user a notification email
        """
        try:
            user = User.objects.get(email=email)
            if not user.is_active:
                return False
            self._send_email(user, self.notification_subject, self.notification_body,
                    sender, **kwargs)
        except User.DoesNotExist:
            pass
    
