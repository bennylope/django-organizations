from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

from accounts.models import Account, AccountUser, AccountOwner


class AccountForm(forms.ModelForm):
    """Form class for updating Accounts"""
    class Meta:
        model = Account


class AccountUserForm(forms.ModelForm):
    """Form class for updating AccountUsers"""
    class Meta:
        model = AccountUser
        exclude = ('account', 'user')


class AccountOwnerForm(forms.ModelForm):
    """Form class for updating an Account's AccountOwner"""
    class Meta:
        model = AccountOwner


class AccountUserAddForm(forms.Form):
    """Form class for adding AccountUsers to an Account"""
    # TODO email only
    username = forms.CharField(max_length=30)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=30)
    is_admin = forms.BooleanField(required=False)

    def save(self, account=None):
        from django.contrib.auth.models import User
        # Test for user with same email first?
        user = User.objects.create(
                username=self.cleaned_data['username'],
                email=self.cleaned_data['email'],
                password=User.objects.make_random_password(),
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'])
        # TODO make sure duplicates cannot be added
        account_user = AccountUser.objects.create(
                user=user,
                is_admin=self.cleaned_data['is_admin'],
                account=account,
                )
        return account_user

    def clean(self):
        return self.cleaned_data


class AccountAddForm(AccountUserAddForm):
    """
    Form class for creating a new account, complete with new owner, including a
    User instance, AccountUser instance, and AccountOwner instance.
    """
    # TODO: formset? Allow adding multiple users, need to specify owner though
    # if more than one
    account_name = forms.CharField(max_length=100)
    subdomain = forms.CharField(max_length=100, required=False)
    domain = forms.CharField(max_length=100, required=False)

    def __init__(self, *args, **kwargs):
        super(AccountAddForm, self).__init__(*args, **kwargs)
        self.fields.pop('is_admin')

    def save(self):
        """
        Create the account, then get the user, then make the owner.
        """
        from django.contrib.auth.models import User
        from accounts.utils import create_account
        # Test for user with same email first?
        user = User.objects.create(
                username=self.cleaned_data['username'],
                email=self.cleaned_data['email'],
                password=User.objects.make_random_password(),
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'])
        return create_account(
                self.cleaned_data['account_name'],
                user,
                self.cleaned_data['subdomain'],
                self.cleaned_data['domain'],
                )


class UserProfileForm(forms.ModelForm):
    """
    Form for updating your own profile
    """
    password = forms.CharField(max_length=30, widget=forms.PasswordInput,
            required=False)
    password_confirm = forms.CharField(max_length=30,
            widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        exclude = ('user_permissions', 'groups', 'is_active', 'is_staff',
                'is_superuser', 'last_login', 'date_joined')

    def clean(self):
        data = self.cleaned_data
        password, password_confirm = data.get('password'), data.get('password_confirm')
        if (password or password_confirm) and (password != password_confirm):
            err_msg = u"Your passwords must match"
            self._errors['password_confirm'] = self.error_class([err_msg])
            del data['password']
            del data['password_confirm']
        return data

    def save(self, commit=True):
        if self.cleaned_data['password']:
            self.instance.set_password(self.cleaned_data['password'])
        return super(UserProfileForm, self).save(commit)


class LoginForm(AuthenticationForm):
    """Adds the 'next' field for log in"""
    redirect_url = forms.CharField(max_length=200, required=False,
            widget=forms.HiddenInput())

