from django import forms
from django.contrib.auth.models import User

from organizations.models import Organization


class UserRegistrationForm(forms.ModelForm):
    """Form class for completing a user's registration and activating the
    User."""
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    password = forms.CharField(max_length=30, widget=forms.PasswordInput)
    password_confirm = forms.CharField(max_length=30,
            widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.initial['username'] = ''

    class Meta:
        model = User
        exclude = ('is_staff', 'is_superuser', 'is_active', 'last_login',
                'date_joined', 'groups', 'user_permissions')


class OrganizationRegistrationForm(forms.ModelForm):
    """Form class for creating new organizations owned by new users."""
    email = forms.EmailField()

    class Meta:
        model = Organization
        exclude = ('is_active', 'users')

    def save(self, *args, **kwargs):
        self.instance.is_active = False
        super(OrganizationRegistrationForm, self).save(*args, **kwargs)
