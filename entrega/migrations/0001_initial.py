# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Cliente'
        db.create_table('entrega_cliente', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fone', self.gf('django.db.models.fields.CharField')(max_length=16, db_index=True)),
            ('ramal', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=4, blank=True)),
            ('contato', self.gf('django.db.models.fields.CharField')(max_length=64, db_index=True)),
            ('outros_contatos', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('logradouro', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('numero', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('complemento', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('obs', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('entrega', ['Cliente'])

        # Adding unique constraint on 'Cliente', fields ['fone', 'ramal']
        db.create_unique('entrega_cliente', ['fone', 'ramal'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'Cliente', fields ['fone', 'ramal']
        db.delete_unique('entrega_cliente', ['fone', 'ramal'])

        # Deleting model 'Cliente'
        db.delete_table('entrega_cliente')


    models = {
        'entrega.cliente': {
            'Meta': {'unique_together': "(['fone', 'ramal'],)", 'object_name': 'Cliente'},
            'complemento': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'contato': ('django.db.models.fields.CharField', [], {'max_length': '64', 'db_index': 'True'}),
            'fone': ('django.db.models.fields.CharField', [], {'max_length': '16', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logradouro': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'numero': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'obs': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'outros_contatos': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'ramal': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '4', 'blank': 'True'})
        }
    }

    complete_apps = ['entrega']
