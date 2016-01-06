# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import organizations.base

# Workaround to prevent migrations from using *developer installed* fields
# rather than locally configured fields.
from ..models import SlugField, TimeStampedModel
CreationDateTimeField = TimeStampedModel._meta.get_field('created').__class__
ModificationDateTimeField = TimeStampedModel._meta.get_field('modified').__class__


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='The name of the organization', max_length=200)),
                ('is_active', models.BooleanField(default=True)),
                ('created', CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('slug', SlugField(populate_from=b'name', editable=False, max_length=200, blank=True, help_text='The name in all lowercase, suitable for URL identification', unique=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
                'verbose_name': 'organization',
                'verbose_name_plural': 'organizations',
            },
            bases=(organizations.base.UnicodeMixin, models.Model),
        ),
        migrations.CreateModel(
            name='OrganizationOwner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('organization', models.OneToOneField(related_name='owner', to='organizations.Organization')),
            ],
            options={
                'verbose_name': 'organization owner',
                'verbose_name_plural': 'organization owners',
            },
            bases=(organizations.base.UnicodeMixin, models.Model),
        ),
        migrations.CreateModel(
            name='OrganizationUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('is_admin', models.BooleanField(default=False)),
                ('organization', models.ForeignKey(related_name='organization_users', to='organizations.Organization')),
                ('user', models.ForeignKey(related_name='organizations_organizationuser', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['organization', 'user'],
                'abstract': False,
                'verbose_name': 'organization user',
                'verbose_name_plural': 'organization users',
            },
            bases=(organizations.base.UnicodeMixin, models.Model),
        ),
        migrations.AddField(
            model_name='organizationowner',
            name='organization_user',
            field=models.OneToOneField(to='organizations.OrganizationUser'),
        ),
        migrations.AddField(
            model_name='organization',
            name='users',
            field=models.ManyToManyField(related_name='organizations_organization', through='organizations.OrganizationUser', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='organizationuser',
            unique_together=set([('user', 'organization')]),
        ),
    ]
