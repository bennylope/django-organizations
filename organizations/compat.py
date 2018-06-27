"""
One module to handle inter-version Django compatibility
"""


try:
    from django.urls import reverse  # noqa
except ImportError:
    from django.core.urlresolvers import reverse  # noqa

try:
    import six  # noqa
except ImportError:
    from django.utils import six  # noqa
