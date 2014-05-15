# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Account'
        db.create_table('accounts_account', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('monthly_subscription', self.gf('django.db.models.fields.IntegerField')(default=1000)),
        ))
        db.send_create_signal('accounts', ['Account'])

        # Adding model 'AccountUser'
        db.create_table('accounts_accountuser', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_type', self.gf('django.db.models.fields.CharField')(default='', max_length=1)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='accounts_accountuser', to=orm['auth.User'])),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(related_name='organization_users', to=orm['accounts.Account'])),
        ))
        db.send_create_signal('accounts', ['AccountUser'])

        # Adding unique constraint on 'AccountUser', fields ['user', 'organization']
        db.create_unique('accounts_accountuser', ['user_id', 'organization_id'])

        # Adding model 'AccountOwner'
        db.create_table('accounts_accountowner', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('organization_user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['accounts.AccountUser'], unique=True)),
            ('organization', self.gf('django.db.models.fields.related.OneToOneField')(related_name='owner', unique=True, to=orm['accounts.Account'])),
        ))
        db.send_create_signal('accounts', ['AccountOwner'])


    def backwards(self, orm):
        # Removing unique constraint on 'AccountUser', fields ['user', 'organization']
        db.delete_unique('accounts_accountuser', ['user_id', 'organization_id'])

        # Deleting model 'Account'
        db.delete_table('accounts_account')

        # Deleting model 'AccountUser'
        db.delete_table('accounts_accountuser')

        # Deleting model 'AccountOwner'
        db.delete_table('accounts_accountowner')


    models = {
        'accounts.account': {
            'Meta': {'ordering': "['name']", 'object_name': 'Account'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'monthly_subscription': ('django.db.models.fields.IntegerField', [], {'default': '1000'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'accounts_account'", 'symmetrical': 'False', 'through': "orm['accounts.AccountUser']", 'to': "orm['auth.User']"})
        },
        'accounts.accountowner': {
            'Meta': {'object_name': 'AccountOwner'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organization': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'owner'", 'unique': 'True', 'to': "orm['accounts.Account']"}),
            'organization_user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['accounts.AccountUser']", 'unique': 'True'})
        },
        'accounts.accountuser': {
            'Meta': {'ordering': "['organization', 'user']", 'unique_together': "(('user', 'organization'),)", 'object_name': 'AccountUser'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'organization_users'", 'to': "orm['accounts.Account']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'accounts_accountuser'", 'to': "orm['auth.User']"}),
            'user_type': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['accounts']