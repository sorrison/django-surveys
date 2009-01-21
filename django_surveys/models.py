from django.db import models
from django import forms


class SurveyGroup(models.Model):
    name = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()

    def __unicode__(self):
        return self.name
    

TYPES = (
    ('text', 'Text'),
    ('int', 'Integer'),
    ('bool', 'Boolean'),
    ('choi', 'Select'),
    ('many', 'Select Many'),
    )

class Question(models.Model):
    survey_group = models.ForeignKey(SurveyGroup)
    order = models.IntegerField()
    question = models.CharField(max_length=200)
    answer_type = models.CharField(max_length=4, choices=TYPES)
    required = models.BooleanField()
    preset_answers = models.TextField(null=True, blank=True, help_text="Seperate answers with a ;")

    class Meta:
        unique_together = ('survey_group', 'order')
        ordering = ('order',)
    
    def __unicode__(self):
        return self.question

    @models.permalink
    def get_absolute_url(self):
        return ('surv_question_detail', [self.id,])

    def get_form_field(self):
        from django_common.widgets import TextField
        fields = {
            'text': TextField,
            'int': forms.IntegerField,
            'bool': forms.BooleanField,
            'choi': forms.ChoiceField,
            }
        return fields[self.answer_type]


    def get_answer_class(self):
        from django_surveys.models import TextAnswer, IntegerAnswer, BooleanAnswer
        fields = {
            'text': TextAnswer,
            'int': IntegerAnswer,
            'bool': BooleanAnswer,
            'choi': CharAnswer,
            }
        return fields[self.answer_type]


class Survey(models.Model):
    survey_group = models.ForeignKey(SurveyGroup)
    submitter = models.CharField(max_length=100, default="anonymous")
    date_submitted = models.DateField(null=True, blank=True)

    def __unicode__(self):
        return '%s - %s - %s' % (self.survey_group, self.id, self.date_submitted)


class Answer(models.Model):
    survey = models.ForeignKey(Survey)
    question = models.ForeignKey(Question)
    type = models.CharField(max_length=4, editable=False)


    class Meta:
        unique_together = ('survey', 'question')

    def get_child(self):
        if self.type == 'text':
            return self.textanswer
        elif self.type == 'bool':
            return self.booleananswer
        elif self.type == 'int':
            return self.integeranswer
        elif self.type == 'choi':
            return self.charanswer

    def get_answer(self):
        return self.get_child().get_answer()


    def __unicode__(self):
        try:
            return str(self.answer)
        except:
            return "%s - %s" % (self.survey, self.question)
        

class TextAnswer(Answer):
    answer = models.TextField(null=True, blank=True)

    def save(self, force_insert=False, force_update=False):
        if not self.id:
            self.type = 'text'
        super(self.__class__, self).save(force_insert, force_update)
 

    def get_answer(self):
        return self.answer


class IntegerAnswer(Answer):
    answer = models.IntegerField(null=True, blank=True)

    def save(self, force_insert=False, force_update=False):
        if not self.id:
            self.type = 'int'
        super(self.__class__, self).save(force_insert, force_update)


    def get_answer(self):
        return self.answer


class BooleanAnswer(Answer):
    answer = models.BooleanField()

    def save(self, force_insert=False, force_update=False):
        if not self.id:
            self.type = 'bool'
        super(self.__class__, self).save(force_insert, force_update)

    def get_answer(self):  
        if self.answer == 0:
            return 'no'
        return 'yes'


class CharAnswer(Answer):
    answer = models.CharField(max_length=100, null=True, blank=True)

    def save(self, force_insert=False, force_update=False):
        if not self.id:
            self.type = 'choi'
        super(self.__class__, self).save(force_insert, force_update)

    def get_answer(self):
        return self.answer


 

