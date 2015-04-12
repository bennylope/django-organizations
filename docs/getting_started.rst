===============
Getting started
===============

Django-organizations allows you to add multi-user accounts to your application
and tie permissions, events, and other data to organization level accounts.

The core of the application consists of three models:

* An **organization** model; the group object. This is what you would associate your own
  app's functionality with, e.g. subscriptions, repositories, projects, etc.
* An **organization user**; a `through` model relating your **users** to your
  **organization**. It provides a convenient link for organization ownership
  (below) and also a way of storing organization/user specific information.
* An **organization owner**. This model links to an **organization user** who
  has rights over the life and death of the organization.


Installation
============

First add the application to your Python path. The easiest way is to use
`pip`::

    pip install django-organizations

.. note::
    If you are using Django<=1.4.10 you will need to install an up-to-date
    version of the `six` package. Previous Django versions included an older
    version of `six` with which Django Organizations is incompatible.

.. note::

    If you are using South you must use 1.0. Django Organizations is
    incompatible with earlier versions of South, as this project uses the
    `south_migrations` folder for schema migrations in order to maintain Django
    1.7 compatability.

Ensure that you have a user system in place to connect to your organizations.
django-organizations will work with the `django.contrib.auth` package or custom
user models (see configuration below).

To install the default models add `organizations` to `INSTALLED_APPS` in your
settings file.::

    INSTALLED_APPS = (
        'django.contrib.auth',
        'organizations',
    )

This should work for the majority of cases, from either simple, out-of-the-box
installations to custom organization models.

If however you want to use single-table customized organization models and/or
custom organization user models, it may be best to treat Django organizations
as a library and *not* install it in your Django project. See the
:ref:`cookbook-advanced` section.

Upgrading Django versions
-------------------------

If you are upgrading the Django version of an existing deployment that
deprecates South in favor of Django's native migrations, you will need to fake
the migrations for Django Organizations (if you have installed the app
directly, of course).

Configuration
=============

You can specify a different model in your settings using the
`AUTH_USER_MODEL` setting `described in the docs
<https://docs.djangoproject.com/en/1.5/ref/settings/#std:setting-AUTH_USER_MODEL>`_.
You can use this setting to configure a custom user model or to refer to a
profile model if your project is using Django 1.4.

URLs
----

If you plan on using the default URLs, hook the application URLs into your main
application URL configuration in `urls.py`. If you plan on using the
invitation/registration system, set your backend URLs, too::

    from organizations.backends import invitation_backend

    urlpatterns = patterns('',
        url(r'^accounts/', include('organizations.urls')),
        url(r'^invitations/', include(invitation_backend().get_urls())),
    )

Registration & invitation
-------------------------

You can specify a different :ref:`invitation backend <invitation-backend>` in
your project settings, and the `invitation_backend` function will provide the
URLs defined by that backend. You can do the same with the
:ref:`registration backend <registration-backend>`::

    ORGS_INVITATION_BACKEND = 'myapp.backends.MyInvitationBackend'
    ORGS_REGISTRATION_BACKEND = 'myapp.backends.MyRegistrationBackend'

Timestamp model and slug field
------------------------------

Historically Django-Organizations relied on `django-extensions
<http://django-extensions.readthedocs.org/en/latest/>`_ for the base
`TimeStampedModel
<http://django-extensions.readthedocs.org/en/latest/model_extensions.html>`_
and `AutoSlugField
<http://django-extensions.readthedocs.org/en/latest/field_extensions.html>`_.
While these work great, this does require that every project install
django-extensions for two small features.

If you decide to use the default django-organization models by adding
`organizations` to your INSTALLED_APPS, you can choose a different
TimeStampedModel base and AutoSlugField. Just specify the full dotted path like so::

    ORGS_SLUGFIELD = 'django_extensions.db.fields.AutoSlugField'
    ORGS_TIMESTAMPED_MODEL = 'django_extensions.db.models.TimeStampedModel'

While you can specify the source of these classes, **their interfaces must be
consistent.** The TimeStampedModel should have two timestamp fields
(`DateTimeField`) named `created` and `modified`, respectively. The SlugField
must accept the `populate_from` keyword argument.

Users and multi-account membership
==================================

.. TODO add image showing how these are all related

The key to these relationships is that while an `OrganizationUser` is
associated with one and only one `Organization`, a `User` can be associated
with multiple `OrganizationUsers` and hence multiple `Organizations`.

.. note::

    This means that the OrganizationUser class cannot be used as a UserProfile
    as that requires a one-to-one relationship with the User class. User
    profile information is better provided by a profile specific model.

In your project you can associate accounts with things like subscriptions,
documents, and other shared resources, all of which the account users can then
access.

Views and Mixins
================

Hooking the django-organizations URLs into your project provides a default set
of views for accessing and updating organizations and organization membership.

The included `class based views
<https://docs.djangoproject.com/en/1.5/topics/class-based-views/>`_ are based on
a set of mixins that allow the views to limit access by a user's relationship
to an organization and that query the appropriate organization or user based on
URL keywords.

Implementing in your own project
================================

While django-organizations has some basic usability 'out-of-the-box', it's
designed to be used as a foundation for project specific functionality. The
:ref:`view mixins <mixins>` should provide base functionality from which to
work for most projects, and the :ref:`cookbook` section provides detailed
examples for various integration scenarios.
