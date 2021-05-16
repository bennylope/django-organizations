# -*- coding: utf-8 -*-
from django.db import migrations

import organizations.fields


class Migration(migrations.Migration):

    dependencies = [("organizations", "0001_initial")]

    operations = [
        migrations.AlterField(
            model_name="organization",
            name="slug",
            field=organizations.fields.SlugField(
                blank=True,
                editable=False,
                help_text="The name in all lowercase, suitable for URL identification",
                max_length=200,
                populate_from=("name",),
                unique=True,
            ),
        )
    ]
