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

import datetime

from models import Answer


def make_choice_tuple(choices):
    
    output = []
    for c in choices.split(';'):
        output.append((c, c))

    return output


def make_survey_form(survey):

    questions = survey.survey_group.question_set.all()
    fields = {}

    for q in questions:
        try:
            answer = Answer.objects.get(survey=survey, question=q).get_object()
            initial = answer.answer
        except:
            initial = ''

        field = q.get_form_field()

        if q.preset_answers:
            fields[str(q.order)] = field(label=q.question, required=q.required, initial=initial, choices=make_choice_tuple(q.preset_answers), widget=forms.RadioSelect)
        else:
            fields[str(q.order)] = field(label=q.question, required=q.required, initial=initial)

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
