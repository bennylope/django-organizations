# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import organizations.fields


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='slug',
            field=organizations.fields.SlugField(help_text='The name in all lowercase, suitable for URL identification', unique=True, populate_from='name', max_length=200, editable=True),
        ),
    ]
