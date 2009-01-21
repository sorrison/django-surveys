from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect

from django_common.graphs.googlechart import GraphGenerator
from utils import make_survey_form, save_survey_form
from models import Survey, Question


def do_survey(request, survey_id, redirect_url='thanks/', template_name='surveys/survey.html'):
    
    survey = get_object_or_404(Survey, pk=survey_id)

    SurveyForm = make_survey_form(survey)

    if request.method == 'POST':
        form = SurveyForm(request.POST)

        if form.is_valid():

            save_survey_form(survey, form)

            return HttpResponseRedirect(redirect_url)

    else:
        form = SurveyForm()

    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


#def survey_done(request, survey_id):

def question_detail(request, question_id):
    
    question = get_object_or_404(Question, pk=question_id)


    if question.answer_type == 'bool' or question.answer_type == 'choi':
        return question_detail_pie(request, question)

    
    return render_to_response('surveys/question_detail.html', locals(), context_instance=RequestContext(request))


def question_detail_pie(request, question):
    answer_dict = {}
    total = 0
    for a in question.answer_set.all():
        answer = a.get_child().answer

        if question.answer_type == 'bool':
            if answer == 1:
                answer = 'yes'
            elif answer == 0:
                answer = 'no'

        try:
            answer_dict[answer] += 1
        except:
            answer_dict[answer] = 1

        total += 1
    

    grapher = GraphGenerator()
    graph_url = grapher.pie_chart(answer_dict)

    return render_to_response('surveys/question_detail_pie.html', locals(), context_instance=RequestContext(request))

