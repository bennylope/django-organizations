from django.contrib.auth import get_user_model
from django.test import TestCase
from django.test.client import RequestFactory
from django.test.utils import override_settings

from organizations.forms import OrganizationAddForm
from organizations.forms import OrganizationForm
from organizations.forms import OrganizationUserAddForm
from organizations.forms import OrganizationUserForm
from organizations.models import Organization
from tests.utils import request_factory_login

User = get_user_model()


class TestOrganizationAddForm(TestCase):
    """
    Tests for adding new organizations
    """

    def setUp(self):
        self.factory = RequestFactory()

    def test_expected_valid_data_validates(self):
        """Test our happy path"""
        request = self.factory.request()
        form = OrganizationAddForm(
            request,
            data={"slug": "new_org", "name": "New Org", "email": "cthulu@oldgods.org"},
        )
        self.assertTrue(form.is_valid())

    def test_add_organization_for_existing_user(self):
        user = User.objects.create_user(
            "timmy", password="ajsdkfa3", email="timmy@whoa.com"
        )
        request = self.factory.request()
        form = OrganizationAddForm(
            request, data={"slug": "new_org", "name": "New Org", "email": user.email}
        )
        self.assertTrue(form.is_valid())
        new_org = form.save()
        self.assertTrue(new_org.is_active)
        self.assertEqual(new_org.name, "New Org")

    def test_add_organization_for_new_user(self):
        user = User.objects.create_user(
            "timmy", password="ajsdkfa3", email="timmy@whoa.com"
        )
        request = request_factory_login(self.factory, user)
        form = OrganizationAddForm(
            request,
            data={
                "slug": "new_org",
                "name": "New Org",
                "email": "i.am.new.here@geemail.com",
            },
        )
        self.assertTrue(form.is_valid())
        new_org = form.save()
        self.assertFalse(new_org.is_active)  # Inactive until confirmation


class TestOrganizationUserAddForm(TestCase):
    fixtures = ["users.json", "orgs.json"]

    def setUp(self):
        self.factory = RequestFactory()
        self.org = Organization.objects.get(name="Nirvana")
        self.owner = self.org.organization_users.get(user__username="kurt")

    def test_multiple_users_exist(self):
        User.objects.create_user("asdkjf", password="ajsdkfa", email="bob@bob.com")
        User.objects.create_user("asdkjf1", password="ajsdkfa3", email="bob@bob.com")
        request = request_factory_login(self.factory, self.owner.user)
        form = OrganizationUserAddForm(
            request=request,
            organization=self.org,
            data={"email": "bob@bob.com"},
        )
        self.assertFalse(form.is_valid())

    def test_add_user_already_in_organization(self):
        admin = self.org.organization_users.get(user__username="krist")
        request = request_factory_login(self.factory, self.owner.user)
        form = OrganizationUserAddForm(
            request=request,
            organization=self.org,
            data={"email": admin.user.email},
        )
        self.assertFalse(form.is_valid())

    def test_save_org_user_add_form(self):
        request = request_factory_login(self.factory, self.owner.user)
        form = OrganizationUserAddForm(
            request=request,
            organization=self.org,
            data={"email": "test_email@example.com", "is_admin": False},
        )
        self.assertTrue(form.is_valid())
        form.save()


@override_settings(USE_TZ=True)
class TestOrganizationForm(TestCase):
    fixtures = ["users.json", "orgs.json"]

    def setUp(self):
        self.factory = RequestFactory()
        self.org = Organization.objects.get(name="Nirvana")
        self.admin = self.org.organization_users.get(user__username="krist")
        self.owner = self.org.organization_users.get(user__username="kurt")

    def test_admin_edits_org(self):
        user = self.admin.user
        request = request_factory_login(self.factory, user)
        form = OrganizationForm(
            request,
            instance=self.org,
            data={"name": self.org.name, "slug": self.org.slug, "owner": self.owner.pk},
        )
        self.assertTrue(form.is_valid())
        form = OrganizationForm(
            request,
            instance=self.org,
            data={"name": self.org.name, "slug": self.org.slug, "owner": self.admin.pk},
        )
        self.assertFalse(form.is_valid())

    def test_owner_edits_org(self):
        user = self.owner.user
        request = request_factory_login(self.factory, user)
        form = OrganizationForm(
            request,
            instance=self.org,
            data={"name": self.org.name, "slug": self.org.slug, "owner": self.owner.pk},
        )
        self.assertTrue(form.is_valid())
        form = OrganizationForm(
            request,
            instance=self.org,
            data={"name": self.org.name, "slug": self.org.slug, "owner": self.admin.pk},
        )
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(self.org.owner.organization_user, self.admin)


class TestOrganizationUserForm(TestCase):
    fixtures = ["users.json", "orgs.json"]

    def setUp(self):
        self.factory = RequestFactory()
        self.org = Organization.objects.get(name="Nirvana")
        self.admin = self.org.organization_users.get(user__username="krist")
        self.owner = self.org.organization_users.get(user__username="kurt")

    def test_edit_owner_user(self):
        form = OrganizationUserForm(instance=self.owner, data={"is_admin": True})
        self.assertTrue(form.is_valid())
        form = OrganizationUserForm(instance=self.owner, data={"is_admin": False})
        self.assertFalse(form.is_valid())

    def test_save_org_form(self):
        request = request_factory_login(self.factory, self.owner.user)
        form = OrganizationForm(
            request,
            instance=self.org,
            data={"name": self.org.name, "slug": self.org.slug, "owner": self.owner.pk},
        )
        self.assertTrue(form.is_valid())
        form.save()

    def test_save_user_form(self):
        form = OrganizationUserForm(instance=self.owner, data={"is_admin": True})
        self.assertTrue(form.is_valid())
        form.save()
