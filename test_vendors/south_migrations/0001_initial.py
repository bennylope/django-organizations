# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Vendor'
        db.create_table('test_vendors_vendor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('street_address', self.gf('django.db.models.fields.CharField')(default='', max_length=100)),
            ('city', self.gf('django.db.models.fields.CharField')(default='', max_length=100)),
        ))
        db.send_create_signal('test_vendors', ['Vendor'])

        # Adding model 'VendorUser'
        db.create_table('test_vendors_vendoruser', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_type', self.gf('django.db.models.fields.CharField')(default='', max_length=1)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='test_vendors_vendoruser', to=orm['auth.User'])),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(related_name='organization_users', to=orm['test_vendors.Vendor'])),
        ))
        db.send_create_signal('test_vendors', ['VendorUser'])

        # Adding unique constraint on 'VendorUser', fields ['user', 'organization']
        db.create_unique('test_vendors_vendoruser', ['user_id', 'organization_id'])

        # Adding M2M table for field permissions on 'VendorUser'
        m2m_table_name = db.shorten_name('test_vendors_vendoruser_permissions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('vendoruser', models.ForeignKey(orm['test_vendors.vendoruser'], null=False)),
            ('permission', models.ForeignKey(orm['auth.permission'], null=False))
        ))
        db.create_unique(m2m_table_name, ['vendoruser_id', 'permission_id'])

        # Adding model 'VendorOwner'
        db.create_table('test_vendors_vendorowner', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('organization_user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['test_vendors.VendorUser'], unique=True)),
            ('organization', self.gf('django.db.models.fields.related.OneToOneField')(related_name='owner', unique=True, to=orm['test_vendors.Vendor'])),
        ))
        db.send_create_signal('test_vendors', ['VendorOwner'])


    def backwards(self, orm):
        # Removing unique constraint on 'VendorUser', fields ['user', 'organization']
        db.delete_unique('test_vendors_vendoruser', ['user_id', 'organization_id'])

        # Deleting model 'Vendor'
        db.delete_table('test_vendors_vendor')

        # Deleting model 'VendorUser'
        db.delete_table('test_vendors_vendoruser')

        # Removing M2M table for field permissions on 'VendorUser'
        db.delete_table(db.shorten_name('test_vendors_vendoruser_permissions'))

        # Deleting model 'VendorOwner'
        db.delete_table('test_vendors_vendorowner')


    models = {
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
        },
        'test_vendors.vendor': {
            'Meta': {'ordering': "['name']", 'object_name': 'Vendor'},
            'city': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'street_address': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'test_vendors_vendor'", 'symmetrical': 'False', 'through': "orm['test_vendors.VendorUser']", 'to': "orm['auth.User']"})
        },
        'test_vendors.vendorowner': {
            'Meta': {'object_name': 'VendorOwner'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organization': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'owner'", 'unique': 'True', 'to': "orm['test_vendors.Vendor']"}),
            'organization_user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['test_vendors.VendorUser']", 'unique': 'True'})
        },
        'test_vendors.vendoruser': {
            'Meta': {'ordering': "['organization', 'user']", 'unique_together': "(('user', 'organization'),)", 'object_name': 'VendorUser'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'organization_users'", 'to': "orm['test_vendors.Vendor']"}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'test_vendors_vendoruser'", 'to': "orm['auth.User']"}),
            'user_type': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1'})
        }
    }

    complete_apps = ['test_vendors']

