from django.utils.importlib import import_module

from organizations.app_settings import (ORGS_INVITATION_BACKEND,
        ORGS_REGISTRATION_BACKEND)


def invitation_backend():
    # TODO exception handling
    class_module, class_name = ORGS_INVITATION_BACKEND.rsplit('.', 1)
    mod = import_module(class_module)
    return getattr(mod, class_name)()


def registration_backend():
    class_module, class_name = ORGS_REGISTRATION_BACKEND.rsplit('.', 1)
    mod = import_module(class_module)
    return getattr(mod, class_name)()
