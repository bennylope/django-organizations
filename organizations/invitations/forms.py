from django import forms


from organizations.forms import UserProfileForm


class InvitationRegistrationForm(UserProfileForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    password = forms.CharField(max_length=30, widget=forms.PasswordInput)
    password_confirm = forms.CharField(max_length=30,
            widget=forms.PasswordInput)
