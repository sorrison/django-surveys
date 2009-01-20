from django.contrib import admin
from models import SurveyGroup, Survey, Question, Answer, TextAnswer, IntegerAnswer, BooleanAnswer


admin.site.register(SurveyGroup)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Survey)
admin.site.register(TextAnswer)
admin.site.register(IntegerAnswer)
admin.site.register(BooleanAnswer)
