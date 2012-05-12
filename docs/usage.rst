Basic Usage
===========

After installing django-group-accounts you can make basic use of the accounts
with minimal configuration.

The application's default views and URL configuration provide functionality for
account creation, user registration, and account management.

Authentication
--------------

django-group-accounts relies on `django.contrib.auth` for the `User` model and
authentication mechanisms. Modified login and logout views are included to make
use of Django's messaging framework, `django.contrib.messages`, and to add an
authenticated user redirect to the login view.

The app's URL config includes Django's password reset views by default.

Creating accounts
-----------------

TODO

Registration
------------

The registration views allow new site members to create new users and accounts
on the site, and to invite additional people to join the account.

Creating accounts
~~~~~~~~~~~~~~~~~

When a new user signs up to create an account - meaning a new UserAccount for a
new Account - the view creates a new `User`, a new `Account`, a new
`AccountUser`, and a new `AccountOwner` object linking the newly created
`Account` and `AccountUser`.

Adding users
~~~~~~~~~~~~

The user registration system in django-group-accounts is based on the same
token generating mechanism as Django's password reset functionality.

Changing ownership
------------------

TODO
