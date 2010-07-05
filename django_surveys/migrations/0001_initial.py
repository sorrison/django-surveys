# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'SurveyGroup'
        db.create_table('django_surveys_surveygroup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('start_date', self.gf('django.db.models.fields.DateField')()),
            ('end_date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('django_surveys', ['SurveyGroup'])

        # Adding model 'Question'
        db.create_table('django_surveys_question', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('survey_group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['django_surveys.SurveyGroup'])),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
            ('question', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('answer_type', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('required', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('preset_answers', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('django_surveys', ['Question'])

        # Adding unique constraint on 'Question', fields ['survey_group', 'order']
        db.create_unique('django_surveys_question', ['survey_group_id', 'order'])

        # Adding model 'Survey'
        db.create_table('django_surveys_survey', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('survey_group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['django_surveys.SurveyGroup'])),
            ('submitter', self.gf('django.db.models.fields.CharField')(default='anonymous', max_length=100)),
            ('date_submitted', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal('django_surveys', ['Survey'])

        # Adding model 'Answer'
        db.create_table('django_surveys_answer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('survey', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['django_surveys.Survey'])),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['django_surveys.Question'])),
            ('_class', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('django_surveys', ['Answer'])

        # Adding unique constraint on 'Answer', fields ['survey', 'question']
        db.create_unique('django_surveys_answer', ['survey_id', 'question_id'])

        # Adding model 'TextAnswer'
        db.create_table('django_surveys_textanswer', (
            ('answer_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['django_surveys.Answer'], unique=True, primary_key=True)),
            ('answer', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('django_surveys', ['TextAnswer'])

        # Adding model 'IntegerAnswer'
        db.create_table('django_surveys_integeranswer', (
            ('answer_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['django_surveys.Answer'], unique=True, primary_key=True)),
            ('answer', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('django_surveys', ['IntegerAnswer'])

        # Adding model 'BooleanAnswer'
        db.create_table('django_surveys_booleananswer', (
            ('answer_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['django_surveys.Answer'], unique=True, primary_key=True)),
            ('answer', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
        ))
        db.send_create_signal('django_surveys', ['BooleanAnswer'])

        # Adding model 'CharAnswer'
        db.create_table('django_surveys_charanswer', (
            ('answer_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['django_surveys.Answer'], unique=True, primary_key=True)),
            ('answer', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('django_surveys', ['CharAnswer'])


    def backwards(self, orm):
        
        # Deleting model 'SurveyGroup'
        db.delete_table('django_surveys_surveygroup')

        # Deleting model 'Question'
        db.delete_table('django_surveys_question')

        # Removing unique constraint on 'Question', fields ['survey_group', 'order']
        db.delete_unique('django_surveys_question', ['survey_group_id', 'order'])

        # Deleting model 'Survey'
        db.delete_table('django_surveys_survey')

        # Deleting model 'Answer'
        db.delete_table('django_surveys_answer')

        # Removing unique constraint on 'Answer', fields ['survey', 'question']
        db.delete_unique('django_surveys_answer', ['survey_id', 'question_id'])

        # Deleting model 'TextAnswer'
        db.delete_table('django_surveys_textanswer')

        # Deleting model 'IntegerAnswer'
        db.delete_table('django_surveys_integeranswer')

        # Deleting model 'BooleanAnswer'
        db.delete_table('django_surveys_booleananswer')

        # Deleting model 'CharAnswer'
        db.delete_table('django_surveys_charanswer')


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
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'start_date': ('django.db.models.fields.DateField', [], {})
        },
        'django_surveys.textanswer': {
            'Meta': {'object_name': 'TextAnswer', '_ormbases': ['django_surveys.Answer']},
            'answer': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'answer_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['django_surveys.Answer']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['django_surveys']
