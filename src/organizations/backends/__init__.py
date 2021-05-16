# -*- coding: utf-8 -*-

from importlib import import_module
from typing import Optional  # noqa
from typing import Text  # noqa

from organizations.app_settings import ORGS_INVITATION_BACKEND
from organizations.app_settings import ORGS_REGISTRATION_BACKEND
from organizations.backends.defaults import BaseBackend  # noqa


def invitation_backend(backend=None, namespace=None):
    # type: (Optional[Text], Optional[Text]) -> BaseBackend
    """
    Returns a specified invitation backend

    Args:
        backend: dotted path to the invitation backend class
        namespace: URL namespace to use

    Returns:
        an instance of an InvitationBackend

    """
    backend = backend or ORGS_INVITATION_BACKEND
    class_module, class_name = backend.rsplit(".", 1)
    mod = import_module(class_module)
    return getattr(mod, class_name)(namespace=namespace)


def registration_backend(backend=None, namespace=None):
    # type: (Optional[Text], Optional[Text]) -> BaseBackend
    """
    Returns a specified registration backend

    Args:
        backend: dotted path to the registration backend class
        namespace: URL namespace to use

    Returns:
        an instance of an RegistrationBackend

    """
    backend = backend or ORGS_REGISTRATION_BACKEND
    class_module, class_name = backend.rsplit(".", 1)
    mod = import_module(class_module)
    return getattr(mod, class_name)(namespace=namespace)
