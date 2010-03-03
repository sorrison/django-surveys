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


from django.template import Library
from django import template
from django.template import resolve_variable
from django.utils.safestring import mark_safe

from django_surveys.models import Answer
from django_surveys.graphs import pie_chart


register = Library()

@register.simple_tag
def graph_summary_url(answer_summary):
    graph_url = pie_chart(answer_summary[0]).get_url()
    return mark_safe(graph_url)

@register.tag
def qa_row(parser, token):
    try:
        tag_name, survey, question = token.split_contents()
    except:
        raise template.TemplateSyntaxError, "%r tag requires exactly two arguments" % token.contents.split()[0]

    return SurveyQANode(survey, question)

class SurveyQANode(template.Node):

    def __init__(self, survey, question):
        self.survey = template.Variable(survey)
        self.question = template.Variable(question)

    def render(self, context):
        try:
            survey = self.survey.resolve(context)
            question = self.question.resolve(context)
        except template.VariableDoesNotExist:
            return ''
        
        try:
            answer = Answer.objects.get(question=question, survey=survey)
        except:
            answer = None
        context.push()
        context.push()
        context['question'] = question
        context['answer'] = answer

        timesheet_template =  template.loader.get_template('django_surveys/survey_qa_row.html')
        output = timesheet_template.render(context)
        context.pop()
        context.pop()
        return output



