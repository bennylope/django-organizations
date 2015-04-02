# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import organizations.base
from django.conf import settings
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='The name of the organization', max_length=200)),
                ('is_active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(verbose_name='created', blank=True, default=django.utils.timezone.now, editable=False)),
                ('modified', models.DateTimeField(verbose_name='modified', blank=True, default=django.utils.timezone.now, editable=False)),
                ('slug', models.SlugField(unique=True, blank=True, help_text='The name in all lowercase, suitable for URL identification', max_length=200, editable=False)),
            ],
            options={
                'verbose_name': 'organization',
                'abstract': False,
                'ordering': ['name'],
                'verbose_name_plural': 'organizations',
            },
            bases=(organizations.base.UnicodeMixin, models.Model),
        ),
        migrations.CreateModel(
            name='OrganizationOwner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(verbose_name='created', blank=True, default=django.utils.timezone.now, editable=False)),
                ('modified', models.DateTimeField(verbose_name='modified', blank=True, default=django.utils.timezone.now, editable=False)),
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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(verbose_name='created', blank=True, default=django.utils.timezone.now, editable=False)),
                ('modified', models.DateTimeField(verbose_name='modified', blank=True, default=django.utils.timezone.now, editable=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('organization', models.ForeignKey(related_name='organization_users', to='organizations.Organization')),
                ('user', models.ForeignKey(related_name='organizations_organizationuser', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'organization user',
                'abstract': False,
                'ordering': ['organization', 'user'],
                'verbose_name_plural': 'organization users',
            },
            bases=(organizations.base.UnicodeMixin, models.Model),
        ),
        migrations.AlterUniqueTogether(
            name='organizationuser',
            unique_together=set([('user', 'organization')]),
        ),
        migrations.AddField(
            model_name='organizationowner',
            name='organization_user',
            field=models.OneToOneField(to='organizations.OrganizationUser'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='organization',
            name='users',
            field=models.ManyToManyField(related_name='organizations_organization', through='organizations.OrganizationUser', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
