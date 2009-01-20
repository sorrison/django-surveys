from django.db import models
from django import forms


class SurveyGroup(models.Model):
    name = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()


TYPES = (
    ('text', 'Text'),
    ('int', 'Integer'),
    ('bool', 'Boolean'),
    )

class Question(models.Model):
    survey_group = models.ForeignKey(SurveyGroup)
    order = models.IntegerField()
    question = models.CharField(max_length=200)
    answer_type = models.CharField(max_length=4, choices=TYPES)
    required = models.BooleanField()

    class Meta:
        unique_together = ('survey_group', 'order')
        ordering = ('order',)
    
    def get_form_field(self):
        from django_common.widgets import TextField
        fields = {
            'text': TextField,
            'int': forms.IntegerField,
            'bool': forms.BooleanField,
            }
        return fields[self.answer_type]


    def get_answer_class(self):
        from karaage.surveys.models import TextAnswer, IntegerAnswer, BooleanAnswer
        fields = {
            'text': TextAnswer,
            'int': IntegerAnswer,
            'bool': BooleanAnswer,
            }
        return fields[self.answer_type]


class Survey(models.Model):
    survey_group = models.ForeignKey(SurveyGroup)
    date_submitted = models.DateField(null=True, blank=True)


class Answer(models.Model):
    survey = models.ForeignKey(Survey)
    question = models.ForeignKey(Question)
    type = models.CharField(max_length=4, editable=False)

    def get_child(self):
        if self.type == 'text':
            return self.textanswer
        if self.type == 'bool':
            return self.booleananswer
        if self.type == 'int':
            return self.integeranswer


class TextAnswer(Answer):
    answer = models.TextField(null=True, blank=True)

    def save(self, force_insert=False, force_update=False):
        if not self.id:
            self.type = 'text'
        super(self.__class__, self).save(force_insert, force_update)
 

    def get_form_field(self):
        return forms.CharField

class IntegerAnswer(Answer):
    answer = models.IntegerField(null=True, blank=True)

    def save(self, force_insert=False, force_update=False):
        if not self.id:
            self.type = 'int'
        super(self.__class__, self).save(force_insert, force_update)

    def get_form_field(self):
        return forms.IntgerField


class BooleanAnswer(Answer):
    answer = models.BooleanField()

    def save(self, force_insert=False, force_update=False):
        if not self.id:
            self.type = 'bool'
        super(self.__class__, self).save(force_insert, force_update)

    def get_form_field(self):
        return forms.BooleanField


 
