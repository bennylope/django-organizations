# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('organization_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='organizations.Organization')),
                ('sport', models.CharField(max_length=100, null=True, blank=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
            bases=('organizations.organization',),
        ),
    ]
