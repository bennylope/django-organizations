from django import forms
from django.contrib.auth.models import User


class InvitationRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    password = forms.CharField(max_length=30, widget=forms.PasswordInput)
    password_confirm = forms.CharField(max_length=30,
            widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(InvitationRegistrationForm, self).__init__(*args, **kwargs)
        self.initial['username'] = ''

    class Meta:
        model = User
        exclude = ('is_staff', 'is_superuser', 'is_active', 'last_login',
                'date_joined', 'groups', 'user_permissions')

