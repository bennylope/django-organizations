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

from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _


class UserRegistrationForm(forms.ModelForm):
    """
    Form class for completing a user's registration and activating the
    User.

    The class operates on a user model which is assumed to have the required
    fields of a BaseUserModel
    """
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    password = forms.CharField(max_length=30, widget=forms.PasswordInput)
    password_confirm = forms.CharField(max_length=30,
            widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.initial['username'] = ''

    def clean(self):
        password = self.cleaned_data.get("password")
        password_confirm = self.cleaned_data.get("password_confirm")
        if password != password_confirm or not password:
            raise forms.ValidationError(_("Your password entries must match"))
        return super(UserRegistrationForm, self).clean()

    class Meta:
        model = get_user_model()
        exclude = ('is_staff', 'is_superuser', 'is_active', 'last_login',
                'date_joined', 'groups', 'user_permissions')


def org_registration_form(org_model):
    """
    Generates a registration ModelForm for the given organization model class
    """

    class OrganizationRegistrationForm(forms.ModelForm):
        """Form class for creating new organizations owned by new users."""
        email = forms.EmailField()

        class Meta:
            model = org_model
            exclude = ('is_active', 'users')

        def save(self, *args, **kwargs):
            self.instance.is_active = False
            super(OrganizationRegistrationForm, self).save(*args, **kwargs)

    return OrganizationRegistrationForm
