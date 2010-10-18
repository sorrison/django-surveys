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

from django import forms
from django.utils.datastructures import SortedDict
import datetime

from models import Answer

from django.forms.widgets import RadioFieldRenderer as BaseRadioFieldRenderer
from django.utils.safestring import mark_safe
from django.utils.encoding import StrAndUnicode, force_unicode
 
class RadioFieldRenderer(BaseRadioFieldRenderer):
 
    def render(self):
        """Outputs a <ul> for this set of radio fields."""
        return mark_safe(u'<ul class="inline">\n%s\n</ul>' % u'\n'.join([u'<li>%s</li>'
                                                                         % force_unicode(w) for w in self]))


def make_choice_tuple(choices):
    
    output = []
    for c in choices.split(';'):
        output.append((c, c))

    return output


def make_survey_form(survey):

    questions = survey.survey_group.question_set.all()
    fields = SortedDict()

    for q in questions:
        try:
            answer = Answer.objects.get(survey=survey, question=q).get_object()
            initial = answer.answer
        except:
            initial = ''

        field = q.get_form_field()

        if q.answer_type == 'choi':
            fields[str(q.order)] = field(label=q.question, required=q.required, initial=initial, choices=make_choice_tuple(q.preset_answers), widget=forms.RadioSelect(renderer=RadioFieldRenderer), help_text=q.help_text)
        elif q.answer_type == 'many':
            fields[str(q.order)] = field(label=q.question, required=q.required, initial=initial, choices=make_choice_tuple(q.preset_answers), widget=forms.CheckboxSelectMultiple, help_text=q.help_text)
        else:
            fields[str(q.order)] = field(label=q.question, required=q.required, initial=initial, help_text=q.help_text)

    return type('SurveyForm', (forms.BaseForm,), {'base_fields': fields})



def save_survey_form(survey, survey_form):

    data = survey_form.cleaned_data
    survey.date_submitted = datetime.datetime.today()
    survey.save()

    questions = survey.survey_group.question_set.all()

    for q in questions:
        try:
            answer = Answer.objects.get(survey=survey, question=q).get_object()
        except:
            answer_class = q.get_answer_class()
            answer = answer_class()
        
        answer.survey = survey
        answer.question = q
        if q.answer_type == "capt":
            answer.answer = data[str(q.order)][1]
        else:
            answer.answer = data[str(q.order)]
        answer.save()


def get_answer_summary(question, answer_set):
    answer_dict = {}
    survey_dict = {}
    total = 0

    for a in answer_set:
        answer = a.get_object().answer

        if question.answer_type == 'bool':
            if answer == 1:
                answer = 'yes'
            elif answer == 0:
                answer = 'no'

        if answer not in answer_dict:
            answer_dict[answer] = 0

        if answer not in survey_dict:
            survey_dict[answer] = []

        answer_dict[answer] += 1
        survey_dict[answer].append(a.survey)
        total += 1

    answer_array = [ {'answer': answer,'count': answer_dict[answer],'surveys': survey_dict[answer]} for answer in answer_dict ]

    return (answer_dict, answer_array, total)
