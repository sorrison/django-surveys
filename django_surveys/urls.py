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
