====================
Django Organizations
====================

Create and manage organizations in Django projects and allow users to be
members of multiple organizations.

Project status
==============

**This project is pre-alpha.** Test coverage is broken, documentation needs
updating, and features are changing.

Use case
========

It's an important requirement to have not just users on your web site or
application but users who are members of a larger group organization. This might be
an additional feature, or it might be a core feature (GitHub has optional group
organizations, Basecamp has required organizations). Any place where the organization is
or can be based on a group of people, rather than just one individual.

Installing
==========

You should install by downloading the source and running::

    $ python setup.py install

Or use pip::

    $ pip install -e git+git://github.com/bennylope/django-organizations.git#egg=django-organizations

.. First add the application to your Python path. The easiest way is to use `pip`:

..    pip install django-organizations

.. Then make sure that you add the `organizations` application to your
.. `INSTALLED_APPS` list.

Using organizations
====================

Overview
--------

The application relies on Django's `contrib.auth` module for the
User model, and `django-registration
<https://bitbucket.org/ubernostrum/django-registration/>`_ for user

There are three models:

* Organization
* OrganizationUser
* OrganizationOwner

Each organization can have only one owner, however a site user can be a member of
multiple organizations, or own multiple organizations. The OrganizationUser model servers as
an intermediary between the `Organization` and the `Users` to allow this.

Ideally as much of the relationships should be defined in the database.

License
=======

Anyone is free to use or modify this software under ther terms of the BSD
license.

To-do
=====

* Management command to clean orphan organizations
* Add self-registration form
* Integrate existing registration app
* Limit the choices for the owner in the organization's admin to organization users of
  that organization
* Consistent doc strings (formatting and content)
* Consistent use of either "organization_user" or "organizationuser"
* Redirect profile view to self (unless referrer)
* Apply login_required decorator to 'final' view dispatch methods
* Add signals for registering users with new organizations
* Create an inclusion tag for rendering the list of organization users
* Set up registration backend
* Set up invitation backend
* List only organizations which the user belongs to

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

Invitations should be added to the DB so that we can track who invited and when

/organizations/register/ - add a new organization
/organizations/invitation/<invite id>/ - respond to an invitation

Wishlist
--------

* Profile view (among others) should take configurable form class
* Add a user type choice field to OrganizationUsers for extensibility (switch
  "is_admin" boolean to this?)
* Enable i18n
* Provide a way to use identifiers other than the IDs in the URLs
* Make Organization and OrganizationUser models abstract and/or optional
* Merge users if someone has duplicate user profiles (or just validate that a
  user can have only one OrganizationUser object per Organization)
* Add permissions to OrganizationUser
* Include an optional welcome message from the sender

Notes
-----

* add MIDDLEWARE that adds the user's OrganizationUser objects (with Organizations) to the request
* Every organization oriented view object should reference the same 'organization'
  attribute
* Every organization user oriented view object should reference the same 'organization'
  and 'organization_user' attribute
* Organizations list view should list organizations that the User is a member of, redirect if there is only one(?)
* Dispatch method should call get_object method, NOT the get/request methods


Rules
=====

* Anyone can create an organization (subject to application specific restrictions)
* Should see if the user exists before creating a new User object
* Should rely upon django-registration
* Should be authentication agnostic (meaning views should take default forms
  but allow for user defined forms, either as param or module path in settings)

Types of restrictions
---------------------

* Logged in user
* Member of the organization
* Admin of the organization
* Owner of the organization
* User object is logged in user

Editing data
------------

* Only admins can edit organization information
* Only admins can edit other users in the organization
* Only admins can delete other users in the organization
* Owners cannot be deleted
* Only the owner can change organization ownership
* Only the owner can edit the owner
* Only admins can add additional users
* Only admins can reset another user's password
* Only the owner can reset the owner's password

Context data
------------

* the User
* the Organization
* Is the user a member of the organization?
* the organization owner
