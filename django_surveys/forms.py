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


from django import forms
from django.contrib.admin.widgets import AdminDateWidget

from django_surveys.models import SurveyGroup, Question

class SurveyGroupForm(forms.ModelForm):
    start_date = forms.DateField(widget=AdminDateWidget)
    end_date = forms.DateField(widget=AdminDateWidget)

    class Meta:
        model = SurveyGroup


class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        exclude = ('survey_group')
        
