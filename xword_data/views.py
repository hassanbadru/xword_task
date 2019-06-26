# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import TemplateView
from django.shortcuts import render

# view for user to start new drill
class LogInView(TemplateView):
    template_name = 'login.html'

    def get_context_data(self, **kwargs):
        context = super(LogInView, self).get_context_data(**kwargs)
        return context

# view to present random clue with information about entry
class DrillView(TemplateView):
    template_name = 'drill.html'

    def get_context_data(self, **kwargs):
        context = super(DrillView, self).get_context_data(**kwargs)
        return context

# view to congratulates the user on their success
class AnswerView(TemplateView):
    template_name = 'answer.html'

    def get_context_data(self, **kwargs):
        context = super(AnswerView, self).get_context_data(**kwargs)
        return context
