from django.contrib.auth.models import User
from django.template import Template, Context
from django.test import TestCase
from django.test.utils import override_settings

from organizations.models import Organization


@override_settings(USE_TZ=True)
class OrgFilterTests(TestCase):

    fixtures = ["users.json", "orgs.json"]

    def setUp(self):
        self.kurt = User.objects.get(username="kurt")
        self.dave = User.objects.get(username="dave")
        self.nirvana = Organization.objects.get(name="Nirvana")
        self.foo = Organization.objects.get(name="Foo Fighters")
        self.context = {}

    def test_is_owner_org_filter(self):
        self.context = {"organization": self.nirvana, "user": self.kurt}
        out = Template(
            "{% load org_tags %}"
            "{% if organization|is_owner:user %}"
            "Is Owner"
            "{% endif %}"
        ).render(
            Context(self.context)
        )
        self.assertEqual(out, "Is Owner")

    def test_is_admin_org_filter(self):
        self.context = {"organization": self.foo, "user": self.dave}
        out = Template(
            "{% load org_tags %}"
            "{% if organization|is_admin:user %}"
            "Is Admin"
            "{% endif %}"
        ).render(
            Context(self.context)
        )
        self.assertEqual(out, "Is Admin")

    def test_is_not_admin_org_filter(self):
        self.context = {"organization": self.nirvana, "user": self.dave}
        out = Template(
            "{% load org_tags %}"
            "{% if not organization|is_admin:user %}"
            "Is Not Admin"
            "{% endif %}"
        ).render(
            Context(self.context)
        )
        self.assertEqual(out, "Is Not Admin")
