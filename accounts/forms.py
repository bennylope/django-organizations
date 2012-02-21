from django import forms

from accounts.models import Account, AccountUser, AccountOwner


class AccountForm(forms.ModelForm):
    """Form for updating accounts"""
    class Meta:
        model = Account


class AccountUserForm(forms.ModelForm):
    """
    Form for updating account users
    """
    username = forms.CharField(max_length=50)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()
    is_admin = forms.BooleanField(required=False)

    class Meta:
        model = AccountUser
        exclude = ('account', 'user')

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, label_suffix=':',
                 empty_permitted=False, instance=None):
        if instance:
            initial['username'] = instance.user.username
            initial['first_name'] = instance.user.first_name
            initial['last_name'] = instance.user.last_name
            initial['email'] = instance.user.email
        super(AccountUserForm, self).__init__(data=data, files=files,
                 initial=initial, instance=instance)

    def save(self, commit=True):
        form_data = self.cleaned_data
        self.instance.user.username = form_data['username']
        self.instance.user.first_name = form_data['first_name']
        self.instance.user.last_name = form_data['last_name']
        self.instance.user.email = form_data['email']
        if commit:
            self.instance.user.save()
        return super(AccountUserForm, self).save(commit)


class AccountUserAddForm(forms.Form):
    """
    Form for creating account users
    """
    username = forms.CharField(max_length=30)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=30)
    is_admin = forms.BooleanField(required=False)

    def save(self, account=None):
        from django.contrib.auth.models import User
        # Test for user with same email first?
        user = User.objects.create_user(
                username=self.cleaned_data['username'],
                email=self.cleaned_data['email'],
                password=User.objects.make_random_password()
                )
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
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
    # TODO hide the is_admin field, it's True by default for this
    # TODO make a util mixin for creating the user...
    account_name = forms.CharField(max_length=100)
    subdomain = forms.CharField(max_length=100, required=False)
    domain = forms.CharField(max_length=100, required=False)

    def save(self):
        """
        Create the account, then get the user, then make the owner.
        """
        from django.contrib.auth.models import User
        from accounts.utils import create_account
        # Test for user with same email first?
        user = User.objects.create_user(
                username=self.cleaned_data['username'],
                email=self.cleaned_data['email'],
                password=User.objects.make_random_password()
                )
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return create_account(
                self.cleaned_data['account_name'],
                user,
                self.cleaned_data['subdomain'],
                self.cleaned_data['domain'],
                )



class ProfileUserForm(AccountUserForm):
    """
    Form for updating your own profile
    """
    password1 = forms.CharField(required=False, widget=forms.PasswordInput)
    password2 = forms.CharField(required=False, widget=forms.PasswordInput)


class AccountOwnerForm(forms.ModelForm):
    """Form for updating account owner"""
    class Meta:
        model = AccountOwner

