from django import forms
from django.contrib.auth.models import User


class InvitationRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    password = forms.CharField(max_length=30, widget=forms.PasswordInput)
    password_confirm = forms.CharField(max_length=30,
            widget=forms.PasswordInput)

    class Meta:
        model = User

