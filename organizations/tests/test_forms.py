from django.test import TestCase
from django.test.client import RequestFactory
from django.test.utils import override_settings

from organizations.forms import OrganizationForm, OrganizationUserForm
from organizations.models import Organization
from organizations.tests.utils import request_factory_login


@override_settings(USE_TZ=True)
class OrgFormTests(TestCase):

    fixtures = ['users.json', 'orgs.json']

    def setUp(self):
        self.factory = RequestFactory()
        self.org = Organization.objects.get(name="Nirvana")
        self.admin = self.org.organization_users.get(user__username="krist")
        self.owner = self.org.organization_users.get(user__username="kurt")

    def test_admin_edits_org(self):
        user = self.admin.user
        request = request_factory_login(self.factory, user)
        form = OrganizationForm(request, instance=self.org, data={
            'name': self.org.name, 'slug': self.org.slug,
            'owner': self.owner.id})
        self.assertTrue(form.is_valid())
        form = OrganizationForm(request, instance=self.org, data={
            'name': self.org.name, 'slug': self.org.slug,
            'owner': self.admin.id})
        self.assertFalse(form.is_valid())

    def test_owner_edits_org(self):
        user = self.owner.user
        request = request_factory_login(self.factory, user)
        form = OrganizationForm(request, instance=self.org, data={
            'name': self.org.name, 'slug': self.org.slug,
            'owner': self.owner.id})
        self.assertTrue(form.is_valid())
        form = OrganizationForm(request, instance=self.org, data={
            'name': self.org.name, 'slug': self.org.slug,
            'owner': self.admin.id})
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(self.org.owner.organization_user, self.admin)

    def test_edit_owner_user(self):
        form = OrganizationUserForm(instance=self.owner,
                data={'is_admin': True})
        self.assertTrue(form.is_valid())
        form = OrganizationUserForm(instance=self.owner,
                data={'is_admin': False})
        self.assertFalse(form.is_valid())

    def test_save_org_form(self):
        request = request_factory_login(self.factory, self.owner.user)
        form = OrganizationForm(request, instance=self.org, data={
                'name': self.org.name, 'slug': self.org.slug,
                'owner': self.owner.id})
        self.assertTrue(form.is_valid())
        form.save()

    def test_save_user_form(self):
        form = OrganizationUserForm(instance=self.owner,
                data={'is_admin': True})
        self.assertTrue(form.is_valid())
        form.save()

