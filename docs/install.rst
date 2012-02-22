Installation
============

You should install by downloading the source and running::

    $ python setup.py install

Or use pip::

    $ pip install -e git+git://github.com/bennylope/django-group-accounts.git#egg=django-group-accounts


Configuration
-------------

Add `accounts` to your `INSTALLED_APPS` list::

    INSTALLED_APPS = (
        ...
        'accounts',
    )

To use the app defaults, include the default URL configuration in your
`urls.py` file::

    urlpatterns = patterns('',
        ...
        url(r'^accounts/', include('accounts.urls')),
    )

