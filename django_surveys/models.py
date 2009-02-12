from django.db import models
from django import forms
from django.db.models.fields import FieldDoesNotExist
from django.db.models.related import RelatedObject


class SurveyGroup(models.Model):
    name = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()

    def __unicode__(self):
        return self.name
    

    @models.permalink
    def get_absolute_url(self):
        return ('surv_surveygroup_edit', [self.id])


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
    preset_answers = models.TextField(null=True, blank=True, help_text="Use only with Select and Select Many. Seperate answers with a semicolon.")

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
    _class = models.CharField(max_length=100, editable=False)

    class Meta:
        unique_together = ('survey', 'question')


    def save(self, *args, **kwargs):
        if not self.id:
            parent = self._meta.parents.keys()[0]
            subclasses = parent._meta.get_all_related_objects()
            for klass in subclasses:
                if isinstance(klass, RelatedObject) and klass.field.primary_key and klass.opts == self._meta:
                    self._class = klass.get_accessor_name()
                    break
        return super(Answer, self).save(*args, **kwargs)
    
    def get_object(self):
        try:
            if self._class and self._meta.get_field_by_name(self._class)[0].opts != self._meta:
                return getattr(self, self._class)
        except FieldDoesNotExist:
            pass
        return self


    def get_answer(self):
        return self.get_object().get_answer()


    def __unicode__(self):
        try:
            return str(self.answer)
        except:
            return "%s - %s" % (self.survey, self.question)
        

class TextAnswer(Answer):
    answer = models.TextField(null=True, blank=True)

    def get_answer(self):
        return self.answer


class IntegerAnswer(Answer):
    answer = models.IntegerField(null=True, blank=True)

    def get_answer(self):
        return self.answer


class BooleanAnswer(Answer):
    answer = models.BooleanField()

    def get_answer(self):  
        if self.answer == 0:
            return 'no'
        return 'yes'


class CharAnswer(Answer):
    answer = models.CharField(max_length=100, null=True, blank=True)

    def get_answer(self):
        return self.answer


 

