# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.utils.translation import gettext_lazy as _

from organizations.backends import invitation_backend
from organizations.models import Organization
from organizations.models import OrganizationUser
from organizations.utils import create_organization


class OrganizationForm(forms.ModelForm):
    """Form class for updating Organizations"""

    owner = forms.ModelChoiceField(OrganizationUser.objects.all())

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)
        self.fields["owner"].queryset = self.instance.organization_users.filter(
            is_admin=True, user__is_active=True
        )
        self.fields["owner"].initial = self.instance.owner.organization_user

    class Meta:
        model = Organization
        exclude = ("users", "is_active")

    def save(self, commit=True):
        if self.instance.owner.organization_user != self.cleaned_data["owner"]:
            self.instance.change_owner(self.cleaned_data["owner"])
        return super().save(commit=commit)

    def clean_owner(self):
        owner = self.cleaned_data["owner"]
        if owner != self.instance.owner.organization_user:
            if self.request.user != self.instance.owner.organization_user.user:
                raise forms.ValidationError(
                    _("Only the organization owner can change ownerhip")
                )
        return owner


class OrganizationUserForm(forms.ModelForm):
    """Form class for updating OrganizationUsers"""

    class Meta:
        model = OrganizationUser
        exclude = ("organization", "user")

    def clean_is_admin(self):
        is_admin = self.cleaned_data["is_admin"]
        if (
            self.instance.organization.owner.organization_user == self.instance
            and not is_admin
        ):
            raise forms.ValidationError(_("The organization owner must be an admin"))
        return is_admin


class OrganizationUserAddForm(forms.ModelForm):
    """Form class for adding OrganizationUsers to an existing Organization"""

    email = forms.EmailField(max_length=75)

    def __init__(self, request, organization, *args, **kwargs):
        self.request = request
        self.organization = organization
        super().__init__(*args, **kwargs)

    class Meta:
        model = OrganizationUser
        exclude = ("user", "organization")

    def save(self, *args, **kwargs):
        """
        The save method should create a new OrganizationUser linking the User
        matching the provided email address. If not matching User is found it
        should kick off the registration process. It needs to create a User in
        order to link it to the Organization.
        """
        try:
            user = get_user_model().objects.get(
                email__iexact=self.cleaned_data["email"]
            )
        except get_user_model().DoesNotExist:
            user = invitation_backend().invite_by_email(
                self.cleaned_data["email"],
                **{
                    "domain": get_current_site(self.request),
                    "organization": self.organization,
                    "sender": self.request.user,
                }
            )
        # Send a notification email to this user to inform them that they
        # have been added to a new organization.
        invitation_backend().send_notification(
            user,
            **{
                "domain": get_current_site(self.request),
                "organization": self.organization,
                "sender": self.request.user,
            }
        )
        return OrganizationUser.objects.create(
            user=user,
            organization=self.organization,
            is_admin=self.cleaned_data["is_admin"],
        )

    def clean_email(self):
        email = self.cleaned_data["email"]
        if self.organization.users.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                _("There is already an organization " "member with this email address!")
            )
        if get_user_model().objects.filter(email__iexact=email).count() > 1:
            raise forms.ValidationError(
                _("This email address has been used multiple times.")
            )
        return email


class OrganizationAddForm(forms.ModelForm):
    """
    Form class for creating a new organization, complete with new owner, including a
    User instance, OrganizationUser instance, and OrganizationOwner instance.
    """

    email = forms.EmailField(
        max_length=75, help_text=_("The email address for the account owner")
    )

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)

    class Meta:
        model = Organization
        exclude = ("users", "is_active")

    def save(self, **kwargs):
        """
        Create the organization, then get the user, then make the owner.
        """
        is_active = True
        try:
            user = get_user_model().objects.get(email=self.cleaned_data["email"])
        except get_user_model().DoesNotExist:
            # TODO(bennylope): look into hooks for alt. registration systems here
            user = invitation_backend().invite_by_email(
                self.cleaned_data["email"],
                **{
                    "domain": get_current_site(self.request),
                    "organization": self.cleaned_data["name"],
                    "sender": self.request.user,
                    "created": True,
                }
            )
            is_active = False
        return create_organization(
            user,
            self.cleaned_data["name"],
            self.cleaned_data["slug"],
            is_active=is_active,
        )


class SignUpForm(forms.Form):
    """
    Form class for signing up a new user and new account.
    """

    name = forms.CharField(max_length=50, help_text=_("The name of the organization"))
    slug = forms.SlugField(
        max_length=50,
        help_text=_("The name in all lowercase, suitable for URL identification"),
    )
    email = forms.EmailField()
