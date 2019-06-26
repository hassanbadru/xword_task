# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse

from .models import Puzzle, Entry, Clue
from .forms import EntryForm

# view for user to start new drill
class LogInView(TemplateView):
    template_name = 'login.html'

    def get_context_data(self, **kwargs):
        context = super(LogInView, self).get_context_data(**kwargs)

        # initialize new session
        self.request.session['total'] = 0
        self.request.session['correct'] = 0

        if self.request.session.has_key('clue_id'):
            del self.request.session['clue_id']

        return context

# view to present random clue with information about entry
class DrillView(TemplateView):
    template_name = 'drill.html'

    def get_context_data(self, **kwargs):
        context = super(DrillView, self).get_context_data(**kwargs)

        # fetch random clue
        random_clue = Clue.objects.order_by("?").first()
        clue_id = random_clue.id
        print(random_clue)


        self.request.session['clue_id'] = clue_id
        self.request.session['total'] += 1

        context['entry_form'] = EntryForm()
        context['random_clue'] = random_clue
        return context

    def post(self, request, *args, **kwargs):
        entry_form = EntryForm(request.POST or None)
        print(entry_form.is_valid())
        return HttpResponseRedirect(reverse('drill'))




# view to congratulates the user on their success
class AnswerView(TemplateView):
    template_name = 'answer.html'

    def get_context_data(self, **kwargs):
       context = super(AnswerView, self).get_context_data(**kwargs)

       # check if clue id exists in current session / if not, redirect to drill page
       if self.request.session.has_key('clue_id'):
          clue_id = self.request.session['clue_id']

       else:
          return HttpResponseRedirect(reverse('drill'))

       # get clue information from DB
       try:
           clue = Clue.objects.get(pk=clue_id)

       except Clue.DoesNotExist:
          raise Http404("Such Clue Does Not Exist")

       # get information for puzzles that include clue text
       puzzles = Puzzle.objects.get_clue_puzzles(clue.clue_text)
       context['puzzles'] = puzzles


       context['clue'] = clue
       return context
