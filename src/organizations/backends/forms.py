# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.forms import UserCreationForm


class UserRegistrationForm(UserCreationForm):
    """
    Form class for completing a user's registration and activating the
    User.

    The class operates on a user model which is assumed to have the required
    fields of a BaseUserModel
    """

    # TODO(bennylope): Remove this entirely and replace with base class


def org_registration_form(org_model):
    """
    Generates a registration ModelForm for the given organization model class
    """

    class OrganizationRegistrationForm(forms.ModelForm):
        """Form class for creating new organizations owned by new users."""

        email = forms.EmailField()

        class Meta:
            model = org_model
            exclude = ("is_active", "users")

        # def save(self, *args, **kwargs):
        #     self.instance.is_active = False
        #     super().save(*args, **kwargs)

    return OrganizationRegistrationForm
