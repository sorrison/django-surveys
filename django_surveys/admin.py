from django.contrib import admin
from models import SurveyGroup, Survey, Question, Answer, TextAnswer, IntegerAnswer, BooleanAnswer



class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'order', 'answer_type', 'required',)
    list_filter = ('survey_group',)





admin.site.register(Question, QuestionAdmin)



admin.site.register(SurveyGroup)
admin.site.register(Answer)
admin.site.register(Survey)
admin.site.register(TextAnswer)
admin.site.register(IntegerAnswer)
admin.site.register(BooleanAnswer)
