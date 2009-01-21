from django.conf.urls.defaults import *


urlpatterns = patterns('django_surveys.views',

    url(r'^questions/(?P<question_id>\d+)/$', 'question_detail', name='surv_question_detail'),
)
