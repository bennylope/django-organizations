=====================
Django group accounts
=====================

Create and manage group accounts in Django projects and allow users to be
members of multiple accounts.

Project status
==============

Let's get this out of the way right now. This is definitely pre-alpha. Django
group accounts is hardly feature complete, and it's still exploratory.
Documentation and test coverage is minimal.

Use case
========

It's an important requirement to have not just users on your web site or
application but users who are members of a larger group account. This might be
an additional feature, or it might be a core feature (GitHub has optional group
accounts, Basecamp has required group accounts). Any place where the account is
or can be based on a group of people, rather than just one individual.

Installing
==========

You should install by downloading the source and running::

    $ python setup.py install

Or use pip::

    $ pip install -e git+git://github.com/bennylope/django-group-accounts.git#egg=django-group-accounts

.. First add the application to your Python path. The easiest way is to use `pip`:

..    pip install django-group-accounts

.. Then make sure that you add the `accounts` application to your
.. `INSTALLED_APPS` list.

Using group accounts
====================

Overview
--------

The application relies on Django's `contrib.auth` module for the
User model, and `django-registration
<https://bitbucket.org/ubernostrum/django-registration/>`_ for user

There are three models:

* Account
* AccountUser
* AccountOwner

Each account can have only one owner, however a site user can be a member of
multiple accounts, or own multiple accounts. The AccountUser model servers as
an intermediary between the `Account` and the `Users` to allow this.

Ideally as much of the relationships should be defined in the database.

License
=======

Anyone is free to use or modify this software under ther terms of the BSD
license.

To-do
=====

* Management command to clean orphan accounts
* Add self-registration form
* Integrate existing registration app
* Limit the choices for the owner in the account's admin to account users of
  that account
* Consistent doc strings (formatting and content)
* Consistent use of either "account_user" or "accountuser"
* Redirect profile view to self (unless referrer)
* Apply login_required decorator to 'final' view dispatch methods
* Add signals for registering users with new accounts
* Create an inclusion tag for rendering the list of account users
* Set up registration backend
* Set up invitation backend

* Add messages (person invited, or invitation sent, log in after registering)
* Conditional messages, based on setting

* Use namespaced URLs

* add search fields to admin

Invitation backend
------------------

* Backend is called by sending email to the backend 
* Backend sends out a signal that invitation has been sent
* Sends out an invitation based on an email address
* Returns a dummy user with that email address, but garbage for username, etc
* Takes care of the invitation oriented registration views
* Invitation acceptance should log the user in

    # TODO offer more sophisticated error if no match
    # TODO do everything no matter what so that 
    # TODO be able to specify where redirects go?

/accounts/register/ - add a new account
/accounts/invitation/<invite id>/ - respond to an invitation

Wishlist
--------

* Profile view (among others) should take configurable form class
* Add a user type choice field to AccountUsers for extensibility (switch
  "is_admin" boolean to this?)
* Enable i18n
* Provide a way to use identifiers other than the IDs in the URLs
* Make Account and AccountUser models abstract and/or optional
* Merge users if someone has duplicate user profiles (or just validate that a
  user can have only one AccountUser object per Account)
* Add permissions to AccountUser

Notes
-----

* add MIDDLEWARE that adds the user's AccountUser objects (with Accounts) to the request
* Every account oriented view object should reference the same 'account'
  attribute
* Every account user oriented view object should reference the same 'account'
  and 'account_user' attribute
* Accounts list view should list accounts that the User is a member of, redirect if there is only one(?)
* Dispatch method should call get_object method, NOT the get/request methods


Rules
=====

* Anyone can create an account (subject to application specific restrictions)
* Should see if the user exists before creating a new User object
* Should rely upon django-registration
* Should be authentication agnostic (meaning views should take default forms
  but allow for user defined forms, either as param or module path in settings)

Types of restrictions
---------------------

* Logged in user
* Member of the account
* Admin of the account
* Owner of the account
* User object is logged in user

Editing data
------------

* Only admins can edit account information
* Only admins can edit other users in the account
* Only admins can delete other users in the account
* Owners cannot be deleted
* Only the owner can change account ownership
* Only the owner can edit the owner
* Only admins can add additional users
* Only admins can reset another user's password
* Only the owner can reset the owner's password

Context data
------------

* the User
* the Account
* Is the user a member of the account?
* the account owner
