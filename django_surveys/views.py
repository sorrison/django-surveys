from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.forms.models import inlineformset_factory
from django.core.urlresolvers import reverse
from django.core.paginator import QuerySetPaginator

from django_common.graphs.googlechart import GraphGenerator

from utils import make_survey_form, save_survey_form
from models import Survey, Question, BooleanAnswer, CharAnswer, SurveyGroup
from forms import SurveyGroupForm

def do_survey(request, survey_id, redirect_url='thanks/', template_name='django_surveys/survey.html', extra_context={}):
    
    survey = get_object_or_404(Survey, pk=survey_id)

    SurveyForm = make_survey_form(survey)

    if request.method == 'POST':
        form = SurveyForm(request.POST)

        if form.is_valid():

            save_survey_form(survey, form)

            return HttpResponseRedirect(redirect_url)

    else:
        form = SurveyForm()

    context = extra_context
    context.update({
            'form': form,
            'survey': survey,
            })

    return render_to_response(template_name, context, context_instance=RequestContext(request))


#def survey_done(request, survey_id):

def question_detail(request, question_id):
    
    question = get_object_or_404(Question, pk=question_id)


    if question.answer_type == 'bool' or question.answer_type == 'choi':
        return question_detail_pie(request, question)

    
    return render_to_response('django_surveys/question_detail.html', locals(), context_instance=RequestContext(request))


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
    
    if question.answer_type == 'bool':
        answer_set = BooleanAnswer.objects.filter(question=question)
    elif question.answer_type == 'choi':
        answer_set = CharAnswer.objects.filter(question=question)

    grapher = GraphGenerator()
    graph_url = grapher.pie_chart(answer_dict).get_url()

    return render_to_response('django_surveys/question_detail_pie.html', locals(), context_instance=RequestContext(request))



def add_edit_survey(request, surveygroup_id=None):

    if surveygroup_id:
        surveygroup = get_object_or_404(SurveyGroup, pk=surveygroup_id)
        flag = 2
    else:
        surveygroup = None
        flag = 1

    QuestionFormSet = inlineformset_factory(SurveyGroup, Question, extra=3)

    if request.method == 'POST':
        surveygroup_form = SurveyGroupForm(request.POST, instance=surveygroup)
        question_formset = QuestionFormSet(request.POST, instance=surveygroup)
        
        if surveygroup_form.is_valid() and question_formset.is_valid():
            surveygroup = surveygroup_form.save()
            if flag == 1:
                question_formset = QuestionFormSet(request.POST, instance=surveygroup)
                question_formset.is_valid()
            question_formset.save()

            
            if 'another' in request.POST:
                return HttpResponseRedirect(reverse('surv_survey_edit', args=[surveygroup.id]))

            return HttpResponseRedirect(reverse('surv_surveygroup_list'))

    else:

        surveygroup_form = SurveyGroupForm(instance=surveygroup)
        question_formset = QuestionFormSet(instance=surveygroup)




    return render_to_response('django_surveys/survey_form.html', locals(), context_instance=RequestContext(request)) 


def surveygroup_list(request):

    page_no = int(request.GET.get('page', 1))

    surveygroup_list = SurveyGroup.objects.all()

    p = QuerySetPaginator(surveygroup_list, 50)
    page = p.page(page_no)

    return render_to_response('django_surveys/surveygroup_list.html', locals(), context_instance=RequestContext(request)) 

    
