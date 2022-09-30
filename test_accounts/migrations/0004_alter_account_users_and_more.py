# Generated by Django 4.0.7 on 2022-09-30 17:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('test_accounts', '0003_accountinvitation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='users',
            field=models.ManyToManyField(related_name='%(app_label)s_%(class)s', through='test_accounts.AccountUser', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='accountinvitation',
            name='invited_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_sent_invitations', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='accountinvitation',
            name='invitee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_invitations', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='accountuser',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s', to=settings.AUTH_USER_MODEL),
        ),
    ]
