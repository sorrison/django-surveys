# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'SurveyGroup.abstract'
        db.add_column('django_surveys_surveygroup', 'abstract', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'SurveyGroup.abstract'
        db.delete_column('django_surveys_surveygroup', 'abstract')


    models = {
        'django_surveys.answer': {
            'Meta': {'unique_together': "(('survey', 'question'),)", 'object_name': 'Answer'},
            '_class': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['django_surveys.Question']"}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['django_surveys.Survey']"})
        },
        'django_surveys.booleananswer': {
            'Meta': {'object_name': 'BooleanAnswer', '_ormbases': ['django_surveys.Answer']},
            'answer': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'answer_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['django_surveys.Answer']", 'unique': 'True', 'primary_key': 'True'})
        },
        'django_surveys.charanswer': {
            'Meta': {'object_name': 'CharAnswer', '_ormbases': ['django_surveys.Answer']},
            'answer': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'answer_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['django_surveys.Answer']", 'unique': 'True', 'primary_key': 'True'})
        },
        'django_surveys.integeranswer': {
            'Meta': {'object_name': 'IntegerAnswer', '_ormbases': ['django_surveys.Answer']},
            'answer': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'answer_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['django_surveys.Answer']", 'unique': 'True', 'primary_key': 'True'})
        },
        'django_surveys.question': {
            'Meta': {'unique_together': "(('survey_group', 'order'),)", 'object_name': 'Question'},
            'answer_type': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'help_text': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'preset_answers': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'survey_group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['django_surveys.SurveyGroup']"})
        },
        'django_surveys.survey': {
            'Meta': {'object_name': 'Survey'},
            'date_submitted': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'submitter': ('django.db.models.fields.CharField', [], {'default': "'anonymous'", 'max_length': '100'}),
            'survey_group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['django_surveys.SurveyGroup']"})
        },
        'django_surveys.surveygroup': {
            'Meta': {'object_name': 'SurveyGroup'},
            'abstract': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {})
        },
        'django_surveys.textanswer': {
            'Meta': {'object_name': 'TextAnswer', '_ormbases': ['django_surveys.Answer']},
            'answer': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'answer_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['django_surveys.Answer']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['django_surveys']
