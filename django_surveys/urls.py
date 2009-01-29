from django.conf.urls.defaults import *


urlpatterns = patterns('django_surveys.views',

    url(r'^$', 'surveygroup_list', name='surv_surveygroup_list'),
    url(r'^create/$', 'add_edit_survey', name='surv_survey_add'),
    url(r'^(?P<surveygroup_id>\d+)/edit/$', 'add_edit_survey', name='surv_surveygroup_edit'),
    url(r'^questions/(?P<question_id>\d+)/$', 'question_detail', name='surv_question_detail'),
)
