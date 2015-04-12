# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Account'
        db.create_table(u'test_accounts_account', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('monthly_subscription', self.gf('django.db.models.fields.IntegerField')(default=1000)),
        ))
        db.send_create_signal('test_accounts', ['Account'])

        # Adding model 'AccountUser'
        db.create_table(u'test_accounts_accountuser', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_type', self.gf('django.db.models.fields.CharField')(default='', max_length=1)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='test_accounts_accountuser', to=orm['auth.User'])),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(related_name='organization_users', to=orm['test_accounts.Account'])),
        ))
        db.send_create_signal('test_accounts', ['AccountUser'])

        # Adding unique constraint on 'AccountUser', fields ['user', 'organization']
        db.create_unique(u'test_accounts_accountuser', [u'user_id', u'organization_id'])

        # Adding model 'AccountOwner'
        db.create_table(u'test_accounts_accountowner', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('organization_user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['test_accounts.AccountUser'], unique=True)),
            ('organization', self.gf('django.db.models.fields.related.OneToOneField')(related_name='owner', unique=True, to=orm['test_accounts.Account'])),
        ))
        db.send_create_signal('test_accounts', ['AccountOwner'])


    def backwards(self, orm):
        # Removing unique constraint on 'AccountUser', fields ['user', 'organization']
        db.delete_unique(u'test_accounts_accountuser', [u'user_id', u'organization_id'])

        # Deleting model 'Account'
        db.delete_table(u'test_accounts_account')

        # Deleting model 'AccountUser'
        db.delete_table(u'test_accounts_accountuser')

        # Deleting model 'AccountOwner'
        db.delete_table(u'test_accounts_accountowner')


    models = {
        'test_accounts.account': {
            'Meta': {'ordering': "['name']", 'unique_together': '()', 'object_name': 'Account', 'index_together': '()'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'monthly_subscription': ('django.db.models.fields.IntegerField', [], {'default': '1000'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'test_accounts_account'", 'symmetrical': 'False', 'through': "orm['test_accounts.AccountUser']", 'to': "orm['auth.User']"})
        },
        'test_accounts.accountowner': {
            'Meta': {'unique_together': '()', 'object_name': 'AccountOwner', 'index_together': '()'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organization': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'owner'", 'unique': 'True', 'to': "orm['test_accounts.Account']"}),
            'organization_user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['test_accounts.AccountUser']", 'unique': 'True'})
        },
        'test_accounts.accountuser': {
            'Meta': {'ordering': "['organization', 'user']", 'unique_together': "(('user', 'organization'),)", 'object_name': 'AccountUser', 'index_together': '()'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'organization_users'", 'to': "orm['test_accounts.Account']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'test_accounts_accountuser'", 'to': "orm['auth.User']"}),
            'user_type': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1'})
        },
        'auth.group': {
            'Meta': {'unique_together': '()', 'object_name': 'Group', 'index_together': '()'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission', 'index_together': '()'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'unique_together': '()', 'object_name': 'User', 'index_together': '()'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': "orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': "orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'", 'index_together': '()'},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['test_accounts']
