Installation
============

Use pip to install group accounts::

    $ pip install django-group-accounts

Or get the development version by downloading the source and installing::

    $ python setup.py install

Configuration
-------------

Make sure you have `django.contrib.auth` and `accounts` added to your
`INSTALLED_APPS` list::

    INSTALLED_APPS = (
        'django.contrib.auth',
        ...
        'accounts',
    )

To use the app defaults, include the default URL configuration in your
`urls.py` file::

    urlpatterns = patterns('',
        ...
        url(r'^accounts/', include('accounts.urls')),
    )

