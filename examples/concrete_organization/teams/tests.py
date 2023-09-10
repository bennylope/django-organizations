from django.test import TestCase

from .models import Department


class TestDepartment(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.department = Department.objects.create(name="Department 1")

    def test_organization_users(self):
        self.assertFalse(
            self.department.organization_users.all().exists()
        )

