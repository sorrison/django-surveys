from django import forms

import datetime

from models import Answer

def make_survey_form(survey):

    questions = survey.survey_group.question_set.all()
    fields = {}

    for q in questions:
        print q.order
        try:
            answer = Answer.objects.get(survey=survey, question=q).get_child()
            initial = answer.answer
        except:
            initial = ''

        field = q.get_form_field()
        fields[str(q.order)] = field(label=q.question, required=q.required, initial=initial)

    return type('SurveyForm', (forms.BaseForm,), {'base_fields': fields})



def save_survey_form(survey, survey_form):

    data = survey_form.cleaned_data
    survey.date_submitted = datetime.datetime.today()
    survey.save()

    questions = survey.survey_group.question_set.all()

    for q in questions:
        try:
            answer = Answer.objects.get(survey=survey, question=q).get_child()
        except:
            answer_class = q.get_answer_class()
            answer = answer_class()
        
        print type(survey)
        answer.survey = survey
        answer.question = q
        answer.answer = data[str(q.order)]
        answer.save()
