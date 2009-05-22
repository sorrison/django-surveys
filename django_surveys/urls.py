from django.conf.urls.defaults import *


urlpatterns = patterns('django_surveys.views',

    url(r'^$', 'surveygroup_list', name='surv_surveygroup_list'),
    url(r'^create/$', 'add_edit_survey', name='surv_survey_add'),
    url(r'^thanks/$', 'survey_thanks', name='surv_survey_thanks'),
    url(r'^(?P<surveygroup_id>\d+)/edit/$', 'add_edit_survey', name='surv_survey_edit'),
    url(r'^(?P<surveygroup_id>\d+)/surveys/$', 'survey_list', name='surv_surveygroup_surveys'),
    url(r'^(?P<surveygroup_id>\d+)/questions/$', 'question_list', name='surv_surveygroup_questions'),
    url(r'^questions/(?P<question_id>\d+)/$', 'question_detail', name='surv_question_detail'),
    url(r'^surveys/(?P<survey_id>\d+)/$', 'survey_detail', name='surv_survey_detail'),
)
