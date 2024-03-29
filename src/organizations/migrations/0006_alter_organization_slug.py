# Generated by Django 4.0.7 on 2022-10-13 02:45

from django.db import migrations

import organizations.fields


class Migration(migrations.Migration):
    dependencies = [
        ("organizations", "0005_alter_organization_users_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="organization",
            name="slug",
            field=organizations.fields.SlugField(
                blank=True,
                editable=False,
                help_text="The name in all lowercase, suitable for URL identification",
                max_length=200,
                populate_from="name",
                unique=True,
            ),
        ),
    ]
