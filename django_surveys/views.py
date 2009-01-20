from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect

from utils import make_survey_form, save_survey_form


def survey(request, survey_id, survey_model, redirect_url='thanks/', template_name='surveys/survey.html'):
    
    survey = get_object_or_404(survey_model, pk=survey_id)

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
