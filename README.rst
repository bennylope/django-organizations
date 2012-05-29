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

First add the application to your Python path. The easiest way is to use
`pip`::

    pip install django-organizations

You should install by downloading the source and running::

    $ python setup.py install

Configuring
-----------

Make sure you have `django.contrib.auth` installed, and add the `organizations`
application to your `INSTALLED_APPS` list::

    INSTALLED_APPS = (
        ...
        'django.contrib.auth',
        'organizations',
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


Usage Overview
==============

For most use cases it should be sufficient to include the app views directly
using the default URL conf file. You can customize their functionality or
access controls by extending the base views.

There are three models:

* **Organization** The group object. This is what you would associate your own
  app's functionality with, e.g. subscriptions, repositories, projects, etc.
* **OrganizationUser** A custom `through` model for the ManyToMany relationship
  between the `Organization` model and the `User` model. It stores additional
  information about the user specific to the organization and provides a
  convenient link for organization ownership.
* **OrganizationOwner** The user with rights over the life and death of the
  organization. This is a one to one relationship with the `OrganizationUser`
  model. This allows `User` objects to own multiple organizations and makes it
  easy to enforce ownership from within the organization's membership.

The underlying organizations API is simple::

    >>> chris = User.objects.get(username="chris")
    >>> soundgarden = create_organization(chris, "Soundgarden")
    >>> soundgarden.is_user(chris)
    True
    >>> soundgarden.is_admin(chris)
    True
    >>> soundgarden.owner.organization_user
    <OrganizationUser: Chris Cornell>
    >>> soundgarden.owner.organization_user.user
    >>> <User: chris>
    >>> audioslave = create_organization(chris, "Audioslave")
    >>> tom = User.objects.get(username="tom")
    >>> audioslave.add_user(tom, is_admin=True)
    <OrganizationUser: Tom Morello>


Overview
--------

Each organization can have only one owner, however a site user can be a member
of multiple organizations, or own multiple organizations. The OrganizationUser
model servers as an intermediary between the `Organization` and the `Users` to
allow this.

Development & Contributing
==========================

Development is on-going. To-do items have been moved to the wiki for the time
being.

The basic functionality should not need much extending. Current dev priorities
for me and contributors should include:

* Improving the tests and test coverage (ideally moving them back out of the
  main module and executable using the setup.py file)
* Improving the backends and backends concept so that additional invitation and
  registration backends can be used
* Documentation
* Ensuring all application text is translatable

Please use the project's issues tracker to report bugs. Thanks!

Project goals
-------------

django-organizations should be backend agnostic:

1. Authentication agnostic
2. Registration agnostic
3. Invitation agnostic
4. User messaging agnostic

Etc.

License
=======

Anyone is free to use or modify this software under ther terms of the BSD
license.
