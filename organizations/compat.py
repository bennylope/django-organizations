"""
One module to handle inter-version Django compatibility
"""

try:
    import six  # noqa
except ImportError:
    from django.utils import six  # noqa
