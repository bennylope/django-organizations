from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.sites.models import get_current_site
from django.utils.translation import ugettext_lazy as _

from accounts.models import Account, AccountUser, AccountOwner
from accounts.invitations.backends import InvitationBackend


class LoginForm(AuthenticationForm):
    """Adds the 'next' field for log in"""

    redirect_url = forms.CharField(max_length=200, required=False,
            widget=forms.HiddenInput())


class AccountForm(forms.ModelForm):
    """Form class for updating Accounts"""

    class Meta:
        model = Account
        exclude = ('users', 'is_active')


class AccountUserForm(forms.ModelForm):
    """Form class for updating AccountUsers"""

    class Meta:
        model = AccountUser
        exclude = ('account', 'user')

    def clean_is_admin(self):
        is_admin = self.cleaned_data['is_admin']
        if self.instance.account.owner.account_user == self.instance and not is_admin:
            raise forms.ValidationError(_("The account owner must be an admin"))
        return is_admin



class AccountOwnerForm(forms.ModelForm):
    """Form class for updating an Account's AccountOwner"""
    class Meta:
        model = AccountOwner


class AccountUserAddForm(forms.ModelForm):
    """Form class for adding AccountUsers to an existing Account"""
    email = forms.EmailField(max_length=30) # TODO check length

    def __init__(self, data=None, files=None, initial=None, instance=None,
            account=None, request=None):
        # TODO change parameter order?
        self.account = account
        self.request = request
        super(AccountUserAddForm, self).__init__(data=data, initial=initial,
                instance=instance)

    class Meta:
        model = AccountUser
        exclude = ('user', 'account')

    def save(self, *args, **kwargs):
        """
        The save method should create a new AccountUser linking the User
        matching the provided email address. If not matching User is found it
        should kick off the registration process. It needs to create a User in
        order to link it to the Account.
        """
        from django.contrib.auth.models import User
        try:
            user = User.objects.get(email=self.cleaned_data['email'])
        except User.MultipleObjectsReturned:
            raise forms.ValidationError(_("This email address has been used multiple times."))
        except User.DoesNotExist:
            # TODO either replace the way the domain is set or send the request
            # so that the backend can do it... OR send a callable or use a
            # custom function...
            user = InvitationBackend().create_invitation(
                    self.cleaned_data['email'],
                    **{'domain': get_current_site(self.request),
                        'account': self.account})
        return AccountUser.objects.create(user=user, account=self.account,
                is_admin=self.cleaned_data['is_admin'])

    def clean_email(self):
        email = self.cleaned_data['email']
        if self.account.users.filter(email=email):
            raise forms.ValidationError(_("There is already an account member with this email address!"))
        return email



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

