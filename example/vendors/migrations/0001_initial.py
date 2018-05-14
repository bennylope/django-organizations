# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import organizations.base
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ("auth", "0006_require_contenttypes_0002"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Vendor",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="The name of the organization", max_length=200
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("street_address", models.CharField(default=b"", max_length=100)),
                ("city", models.CharField(default=b"", max_length=100)),
            ],
            options={"ordering": ["name"], "abstract": False},
            bases=(organizations.base.UnicodeMixin, models.Model),
        ),
        migrations.CreateModel(
            name="VendorOwner",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "organization",
                    models.OneToOneField(related_name="owner", to="vendors.Vendor"),
                ),
            ],
            options={"abstract": False},
            bases=(organizations.base.UnicodeMixin, models.Model),
        ),
        migrations.CreateModel(
            name="VendorUser",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("user_type", models.CharField(default=b"", max_length=1)),
                (
                    "organization",
                    models.ForeignKey(
                        related_name="organization_users", to="vendors.Vendor"
                    ),
                ),
                (
                    "permissions",
                    models.ManyToManyField(to="auth.Permission", blank=True),
                ),
                (
                    "user",
                    models.ForeignKey(
                        related_name="vendors_vendoruser", to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
            options={"ordering": ["organization", "user"], "abstract": False},
            bases=(organizations.base.UnicodeMixin, models.Model),
        ),
        migrations.AddField(
            model_name="vendorowner",
            name="organization_user",
            field=models.OneToOneField(to="vendors.VendorUser"),
        ),
        migrations.AddField(
            model_name="vendor",
            name="users",
            field=models.ManyToManyField(
                related_name="vendors_vendor",
                through="vendors.VendorUser",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterUniqueTogether(
            name="vendoruser", unique_together=set([("user", "organization")])
        ),
    ]
