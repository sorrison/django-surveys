from django import forms

from models import SurveyGroup, Question

class SurveyGroupForm(forms.ModelForm):
    
    class Meta:
        model = SurveyGroup


class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        exclude = ('survey_group')
        
