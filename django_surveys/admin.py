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


from django.contrib import admin
from models import SurveyGroup, Survey, Question, Answer, TextAnswer, IntegerAnswer, BooleanAnswer, CharAnswer



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
admin.site.register(CharAnswer)
