# -*- coding: utf-8 -*-

# Copyright (c) 2012-2019, Ben Lopatin and contributors
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.  Redistributions in binary
# form must reproduce the above copyright notice, this list of conditions and the
# following disclaimer in the documentation and/or other materials provided with
# the distribution
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from typing import Optional  # noqa
from typing import Text  # noqa

from importlib import import_module

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
