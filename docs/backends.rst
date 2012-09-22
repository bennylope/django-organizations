Invitation and Registration Backends
====================================

The backends are used for adding new users to organizations, either by way of
self-registration or invitation by existing organization users. The default
backends should suffice for simple implementations. If you make use of a
profile model or a user model other than `auth.User` you should extend the
releveant backends for your own project. If you've used custom URL names then
you'll also want to extend the backends to use your own success URLs.

Registration
------------

A registration backend is used for creating new users with new organizations,
e.g. new user sign up.

Invitations
-----------

An invitation backend is used for adding new users to an existing organization.
The backend should add existing users and create new users.
