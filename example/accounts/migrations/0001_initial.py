# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import organizations.base
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='The name of the organization', max_length=200)),
                ('is_active', models.BooleanField(default=True)),
                ('monthly_subscription', models.IntegerField(default=1000)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
            bases=(organizations.base.UnicodeMixin, models.Model),
        ),
        migrations.CreateModel(
            name='AccountOwner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('organization', models.OneToOneField(related_name='owner', to='accounts.Account')),
            ],
            options={
                'abstract': False,
            },
            bases=(organizations.base.UnicodeMixin, models.Model),
        ),
        migrations.CreateModel(
            name='AccountUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_type', models.CharField(default=b'', max_length=1)),
                ('organization', models.ForeignKey(related_name='organization_users', to='accounts.Account')),
                ('user', models.ForeignKey(related_name='accounts_accountuser', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['organization', 'user'],
                'abstract': False,
            },
            bases=(organizations.base.UnicodeMixin, models.Model),
        ),
        migrations.AddField(
            model_name='accountowner',
            name='organization_user',
            field=models.OneToOneField(to='accounts.AccountUser'),
        ),
        migrations.AddField(
            model_name='account',
            name='users',
            field=models.ManyToManyField(related_name='accounts_account', through='accounts.AccountUser', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='accountuser',
            unique_together=set([('user', 'organization')]),
        ),
    ]
