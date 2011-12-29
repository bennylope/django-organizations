from django import forms

from accounts.models import Account, AccountUser, AccountOwner


class AccountForm(forms.ModelForm):
    """Form for updating accounts"""
    class Meta:
        model = Account


class AccountUserForm(forms.ModelForm):
    """Form for updating account users"""
    class Meta:
        model = AccountUser


class AccountOwnerForm(forms.ModelForm):
    """Form for updating account owner"""
    class Meta:
        model = AccountOwner

