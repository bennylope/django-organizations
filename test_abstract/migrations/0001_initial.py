# Generated by Django 2.0 on 2017-12-07 03:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import organizations.base
import organizations.fields


class Migration(migrations.Migration):
    initial = True

    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]

    operations = [
        migrations.CreateModel(
            name="CustomOrganization",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="The name of the organization", max_length=200
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                (
                    "created",
                    organizations.fields.AutoCreatedField(
                        default=django.utils.timezone.now, editable=False
                    ),
                ),
                (
                    "modified",
                    organizations.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now, editable=False
                    ),
                ),
                (
                    "slug",
                    organizations.fields.SlugField(
                        editable=True,
                        help_text=(
                            "The name in all lowercase, suitable for URL identification"
                        ),
                        max_length=200,
                        populate_from="name",
                        unique=True,
                    ),
                ),
                ("street_address", models.CharField(default="", max_length=100)),
                ("city", models.CharField(default="", max_length=100)),
            ],
            options={
                "verbose_name": "organization",
                "verbose_name_plural": "organizations",
                "ordering": ["name"],
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="CustomOwner",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    organizations.fields.AutoCreatedField(
                        default=django.utils.timezone.now, editable=False
                    ),
                ),
                (
                    "modified",
                    organizations.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now, editable=False
                    ),
                ),
                (
                    "organization",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="owner",
                        to="test_abstract.CustomOrganization",
                    ),
                ),
            ],
            options={
                "verbose_name": "organization owner",
                "verbose_name_plural": "organization owners",
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="CustomUser",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    organizations.fields.AutoCreatedField(
                        default=django.utils.timezone.now, editable=False
                    ),
                ),
                (
                    "modified",
                    organizations.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now, editable=False
                    ),
                ),
                ("is_admin", models.BooleanField(default=False)),
                ("user_type", models.CharField(default="", max_length=1)),
                (
                    "organization",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="organization_users",
                        to="test_abstract.CustomOrganization",
                    ),
                ),
                (
                    "permissions",
                    models.ManyToManyField(blank=True, to="auth.Permission"),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="test_abstract_customuser",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "organization user",
                "verbose_name_plural": "organization users",
                "ordering": ["organization", "user"],
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="customowner",
            name="organization_user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                to="test_abstract.CustomUser",
            ),
        ),
        migrations.AddField(
            model_name="customorganization",
            name="users",
            field=models.ManyToManyField(
                related_name="test_abstract_customorganization",
                through="test_abstract.CustomUser",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterUniqueTogether(
            name="customuser", unique_together={("user", "organization")}
        ),
    ]
