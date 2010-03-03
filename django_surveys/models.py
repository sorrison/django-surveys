# Copyright 2008 VPAC
#
# This file is part of django-surveys.
#
# django-surveys is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# django-surveys is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with django-surveys  If not, see <http://www.gnu.org/licenses/>.

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
        return ('surv_survey_edit', [self.id])


TYPES = (
    ('text', 'Text'),
    ('int', 'Integer'),
    ('bool', 'Boolean'),
    ('choi', 'Select'),
    ('many', 'Select Many'),
    ('capt', 'Captcha'),
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
        if self.answer_type == "capt":
            from captcha.fields import CaptchaField
            return CaptchaField

        from widgets import TextField
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
            'capt': TextAnswer,
            'text': TextAnswer,
            'int': IntegerAnswer,
            'bool': BooleanAnswer,
            'choi': CharAnswer,
            }
        return fields[self.answer_type]

    def has_graph(self):
        if self.answer_type == 'bool' or self.answer_type == 'choi':
            return True
        else:
            return False

    def get_answer_summary(self):
        from utils import get_answer_summary
        return get_answer_summary(self, self.answer_set.all())

class Survey(models.Model):
    survey_group = models.ForeignKey(SurveyGroup)
    submitter = models.CharField(max_length=100, default="anonymous")
    date_submitted = models.DateField(null=True, blank=True)

    class Meta:
         permissions = (
            ("survey_admin", "Survey Admin"),
         )
	
    def __unicode__(self):
        return '%s - %s - %s' % (self.survey_group, self.id, self.date_submitted)

    @models.permalink
    def get_absolute_url(self):
        return ('surv_survey_detail', [self.id])


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


 

