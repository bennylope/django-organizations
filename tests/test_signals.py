from django.contrib.auth.models import User
from django.test import TestCase
from django.test.utils import override_settings
from mock import call
from mock_django.signals import mock_signal_receiver

from organizations.models import Organization
from organizations.signals import owner_changed
from organizations.signals import user_added
from organizations.signals import user_removed


@override_settings(USE_TZ=True)
class SignalsTestCase(TestCase):

    fixtures = ['users.json', 'orgs.json']

    def setUp(self):
        self.kurt = User.objects.get(username="kurt")
        self.dave = User.objects.get(username="dave")
        self.krist = User.objects.get(username="krist")
        self.duder = User.objects.get(username="duder")
        self.foo = Organization.objects.get(name="Foo Fighters")
        self.org = Organization.objects.get(name="Nirvana")
        self.admin = self.org.organization_users.get(user__username="krist")
        self.owner = self.org.organization_users.get(user__username="kurt")

    def test_user_added_called(self):

        with mock_signal_receiver(user_added) as add_receiver:
            self.foo.add_user(self.krist)

            self.assertEqual(add_receiver.call_args_list, [
                call(signal=user_added, sender=self.foo, user=self.krist),
            ])

        with mock_signal_receiver(user_added) as add_receiver:
            self.foo.get_or_add_user(self.duder)

            self.assertEqual(add_receiver.call_args_list, [
                call(signal=user_added, sender=self.foo, user=self.duder),
            ])

    def test_user_added_not_called(self):

        with mock_signal_receiver(user_added) as add_receiver:
            self.foo.get_or_add_user(self.dave)

            self.assertEqual(add_receiver.call_args_list, [])

    def test_user_removed_called(self):

        with mock_signal_receiver(user_removed) as remove_receiver:
            self.foo.add_user(self.krist)
            self.foo.remove_user(self.krist)

            self.assertEqual(remove_receiver.call_args_list, [
                call(signal=user_removed, sender=self.foo, user=self.krist),
            ])

    def test_owner_changed_called(self):

        with mock_signal_receiver(owner_changed) as changed_receiver:
            self.org.change_owner(self.admin)

            self.assertEqual(changed_receiver.call_args_list, [
                call(signal=owner_changed, sender=self.org,
                     old=self.owner, new=self.admin),
            ])
