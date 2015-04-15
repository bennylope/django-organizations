===========
Basic usage
===========

After installing django-organizations you can make basic use of the accounts
with minimal configuration.

Views
=====

The application's default views and URL configuration provide functionality for
account creation, user registration, and account management.

Creating accounts
-----------------

.. note::
    This is a to-do item, and an opportunity to contribute to the project!

User registration
-----------------

You can register new users and organizations through your project's own system
or use the extensible invitation and registration backends.

The default invitation backend accepts an email address and returns the user
who either matches that email address or creates a new user with that email
address. The view for adding a new user is then responsbile for adding this
user to the organization.

The `OrganizationSignup` view is used for allowing a user new to the site to
create an organization and account. This view relies on the registration
backend to create and verify a new user.

The backends can be extended to fit the needs of a given site.

Creating accounts
~~~~~~~~~~~~~~~~~

When a new user signs up to create an account - meaning a new UserAccount for a
new Account - the view creates a new `User`, a new `Account`, a new
`AccountUser`, and a new `AccountOwner` object linking the newly created
`Account` and `AccountUser`.

Adding users
~~~~~~~~~~~~

The user registration system in django-organizations is based on the same
token generating mechanism as Django's password reset functionality.

Changing ownership
------------------

Changing ownership of an organization is as simple as updating the
`OrganizationOwner` such that it points to the new user. There is as of yet no
out of the box view to do this, but adding your own will be trivial.

Invitation & registration backends
==================================

The invitation and registration backends provide a way for your account users
to add new users to their accounts and if your application allows it, for users
to create their own accounts at registration. Each base backend class is
designed to provide a common interface which your backend classes can use to
work with whatever user models, registration systems, additional account
systems, or any other tools you need for your site.
