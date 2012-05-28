====================
django-organizations
====================

:Info: Groups and multi-user account management
:Version: 0.1.0
:Status: alpha
:Author: Ben Lopatin (http://benlopatin.com)

Add user-managed, multi-user groups to your Django project. Use
django-organizations whether your site needs organizations that function like
social groups or multi-user account objects to provide account and subscription
functionality beyond the individual user.

* Relies on `django.contrib.auth` and does not add or require additional user
  or authentication functionality
* Users can be belong to and own more than one organization (account, group)
* Invitation and registration functionality is designed to be flexible to allow
  you to integrate existing invitation and registration apps

Installing
==========

.. First add the application to your Python path. The easiest way is to use `pip`:

..    pip install django-organizations

You should install by downloading the source and running::

    $ python setup.py install

Or use pip::

    $ pip install -e git+git://github.com/bennylope/django-organizations.git#egg=django-organizations

Configuring
-----------

Make sure you have `django.contrib.auth` installed, and add the `organizations`
application to your `INSTALLED_APPS` list::

    INSTALLED_APPS = (
        ...
        'django.contrib.auth',
        'django_wysiwyg',
    )

Then ensure that your project URL conf is updated. You should hook in the
main application URL conf as well as your chosen invitation backend URLs::

    from organizations.backends import invitation_backend

    urlpatterns = patterns('',
        ...
        url(r'^accounts/', include('organizations.urls')),
        url(r'^invitations/', include(invitation_backend().get_urls())),
    )

You can specify a different invitation backend in your project settings, and
the `invitation_backend` function will provide the URLs defined by that
backend::

    ORGS_INVITATION_BACKEND = 'myapp.backends.MyInvitationBackend'

License
=======

Anyone is free to use or modify this software under ther terms of the BSD
license.

Using organizations
====================

Overview
--------

There are three models:

* Organization
* OrganizationUser
* OrganizationOwner

Each organization can have only one owner, however a site user can be a member of
multiple organizations, or own multiple organizations. The OrganizationUser model servers as
an intermediary between the `Organization` and the `Users` to allow this.

Ideally as much of the relationships should be defined in the database.

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
* Set up registration backend
* Add slug field for org name
* Add messages (person invited, or invitation sent, log in after registering)
* Conditional messages, based on setting
* Use namespaced URLs
* add search fields to admin

Invitation backend
------------------

* Backend sends out a signal that invitation has been sent
* offer more sophisticated error if no match
* be able to specify where redirects go?

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
* Allow pools of multiple registration and invitation backends

Rules
=====

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
