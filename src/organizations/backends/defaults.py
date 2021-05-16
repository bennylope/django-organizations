# -*- coding: utf-8 -*-

"""Backend classes should provide common interface"""

import email.utils
import inspect
import uuid
from typing import ClassVar  # noqa
from typing import Optional  # noqa
from typing import Text  # noqa

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMessage
from django.http import Http404
from django.shortcuts import redirect
from django.shortcuts import render
from django.template import loader
from django.urls import path
from django.urls import reverse
from django.utils.translation import gettext as _

from organizations.backends.forms import UserRegistrationForm
from organizations.backends.forms import org_registration_form
from organizations.utils import create_organization
from organizations.utils import default_org_model
from organizations.utils import model_field_attr


class BaseBackend:
    """
    Base backend class for registering and inviting users to an organization
    """

    registration_form_template = "organizations/register_form.html"
    activation_success_template = "organizations/register_success.html"

    def __init__(self, org_model=None, namespace=None):
        # type: (Optional[ClassVar], Optional[Text]) -> None
        self.user_model = get_user_model()
        self.org_model = org_model or default_org_model()
        self.namespace = namespace

    def namespace_preface(self):
        return "" if not self.namespace else "{}:".format(self.namespace)

    def get_urls(self):
        raise NotImplementedError

    def get_success_url(self):
        """Will return the class's `success_url` attribute unless overridden"""
        raise NotImplementedError

    def get_form(self, **kwargs):
        """Returns the form for registering or inviting a user"""
        if not getattr(self, "form_class", None):
            raise AttributeError("You must define a form_class")
        return self.form_class(**kwargs)

    def get_token(self, user, **kwargs):
        """Returns a unique token for the given user"""
        return PasswordResetTokenGenerator().make_token(user)

    def get_username(self):
        """
        Returns a UUID-based 'random' and unique username.

        This is required data for user models with a username field.
        """
        return str(uuid.uuid4())[
            : model_field_attr(self.user_model, "username", "max_length")
        ]

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

        if not PasswordResetTokenGenerator().check_token(user, token):
            raise Http404(_("Your URL may have expired."))
        form = self.get_form(
            data=request.POST or None, files=request.FILES or None, instance=user
        )
        if form.is_valid():
            form.instance.is_active = True
            user = form.save()
            user.set_password(form.cleaned_data["password1"])
            user.save()
            self.activate_organizations(user)
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password1"],
            )
            login(request, user)
            return redirect(self.get_success_url())
        return render(request, self.registration_form_template, {"form": form})

    def send_reminder(self, user, sender=None, **kwargs):
        """Sends a reminder email to the specified user"""
        if user.is_active:
            return False
        token = PasswordResetTokenGenerator().make_token(user)
        kwargs.update({"token": token})
        self.email_message(
            user, self.reminder_subject, self.reminder_body, sender, **kwargs
        ).send()

    def email_message(
        self,
        user,
        subject_template,
        body_template,
        sender=None,
        message_class=EmailMessage,
        **kwargs
    ):
        """
        Returns an email message for a new user. This can be easily overridden.
        For instance, to send an HTML message, use the EmailMultiAlternatives message_class
        and attach the additional conent.
        """
        if sender:
            try:
                display_name = sender.get_full_name()
            except (AttributeError, TypeError):
                display_name = sender.get_username()
            from_email = "%s <%s>" % (
                display_name,
                email.utils.parseaddr(settings.DEFAULT_FROM_EMAIL)[1],
            )
            reply_to = "%s <%s>" % (display_name, sender.email)
        else:
            from_email = settings.DEFAULT_FROM_EMAIL
            reply_to = from_email

        headers = {"Reply-To": reply_to}
        kwargs.update({"sender": sender, "user": user})

        subject_template = loader.get_template(subject_template)
        body_template = loader.get_template(body_template)
        subject = subject_template.render(
            kwargs
        ).strip()  # Remove stray newline characters
        body = body_template.render(kwargs)
        return message_class(subject, body, from_email, [user.email], headers=headers)


class RegistrationBackend(BaseBackend):
    """
    A backend for allowing new users to join the site by creating a new user
    associated with a new organization.
    """

    # NOTE this backend stands to be simplified further, as email verification
    # should be beyond the purview of this app
    activation_subject = "organizations/email/activation_subject.txt"
    activation_body = "organizations/email/activation_body.html"
    reminder_subject = "organizations/email/reminder_subject.txt"
    reminder_body = "organizations/email/reminder_body.html"
    form_class = UserRegistrationForm

    def get_success_url(self):
        return reverse("registration_success")

    def get_urls(self):
        return [
            path("complete/", view=self.success_view, name="registration_success"),
            path(
                "<int:user_id>-<token>/",
                view=self.activate_view,
                name="registration_register",
            ),
            path("", view=self.create_view, name="registration_create"),
        ]

    @property
    def urls(self):
        return self.get_urls(), self.namespace or "registration"

    def register_by_email(self, email, sender=None, request=None, **kwargs):
        """
        Returns a User object filled with dummy data and not active, and sends
        an invitation email.
        """
        try:
            user = self.user_model.objects.get(email=email)
        except self.user_model.DoesNotExist:
            user = self.user_model.objects.create(
                username=self.get_username(),
                email=email,
                password=self.user_model.objects.make_random_password(),
            )
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
        kwargs.update({"token": token})
        self.email_message(
            user, self.activation_subject, self.activation_body, sender, **kwargs
        ).send()

    def create_view(self, request):
        """
        Initiates the organization and user account creation process
        """
        if request.user.is_authenticated:
            return redirect("organization_add")
        form = org_registration_form(self.org_model)(request.POST or None)
        if form.is_valid():
            try:
                user = self.user_model.objects.get(email=form.cleaned_data["email"])
            except self.user_model.DoesNotExist:
                user = self.user_model.objects.create(
                    username=self.get_username(),
                    email=form.cleaned_data["email"],
                    password=self.user_model.objects.make_random_password(),
                )
                user.is_active = False
                user.save()
            else:
                return redirect("organization_add")
            organization = create_organization(
                user,
                form.cleaned_data["name"],
                form.cleaned_data["slug"],
                is_active=False,
            )
            return render(
                request,
                self.activation_success_template,
                {"user": user, "organization": organization},
            )
        return render(request, self.registration_form_template, {"form": form})

    def success_view(self, request):
        return render(request, self.activation_success_template, {})


class InvitationBackend(BaseBackend):
    """
    A backend for inviting new users to join the site as members of an
    organization.
    """

    notification_subject = "organizations/email/notification_subject.txt"
    notification_body = "organizations/email/notification_body.html"
    invitation_subject = "organizations/email/invitation_subject.txt"
    invitation_body = "organizations/email/invitation_body.html"
    reminder_subject = "organizations/email/reminder_subject.txt"
    reminder_body = "organizations/email/reminder_body.html"
    form_class = UserRegistrationForm

    def get_success_url(self):
        # TODO get this url name from an attribute
        return reverse("organization_list")

    def get_urls(self):
        # TODO enable naming based on a model?
        return [
            path(
                "<int:user_id>-<token>/",
                view=self.activate_view,
                name="invitations_register",
            )
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
            if (
                "username"
                in inspect.getfullargspec(self.user_model.objects.create_user).args
            ):
                user = self.user_model.objects.create(
                    username=self.get_username(),
                    email=email,
                    password=self.user_model.objects.make_random_password(),
                )
            else:
                user = self.user_model.objects.create(
                    email=email, password=self.user_model.objects.make_random_password()
                )
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
        kwargs.update({"token": token})
        self.email_message(
            user, self.invitation_subject, self.invitation_body, sender, **kwargs
        ).send()
        return True

    def send_notification(self, user, sender=None, **kwargs):
        """
        An intermediary function for sending an notification email informing
        a pre-existing, active user that they have been added to a new
        organization.
        """
        if not user.is_active:
            return False
        self.email_message(
            user, self.notification_subject, self.notification_body, sender, **kwargs
        ).send()
        return True
