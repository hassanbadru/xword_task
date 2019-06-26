# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
import logging
import six

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
        self.request.session['repeat'] = False

        if self.request.session.has_key('clue_id'):
            del self.request.session['clue_id']

        return context

# view to present random clue with information about entry
class DrillView(TemplateView):
    template_name = 'drill.html'

    def get_context_data(self, **kwargs):
        context = super(DrillView, self).get_context_data(**kwargs)
        repeat = False

        # check session if clue is repeated
        if self.request.session.has_key('repeat'):
           repeat = self.request.session['repeat']

        # check if clue is being repeated, get clue instance
        if repeat:
           clue_id = self.request.session['clue_id']

           try:
               random_clue = Clue.objects.get(pk=clue_id)
           except Clue.DoesNotExist:
               raise Http404("Such Clue Does Not Exist")

        else:
           # Initialize values for new clue instance
           random_clue = Clue.objects.order_by("?").first()
           clue_id = random_clue.id

           self.request.session['clue_id'] = clue_id
           self.request.session['total'] += 1
           self.request.session['success'] = False

        # add data to context for templates
        context['entry_form'] = EntryForm()
        context['random_clue'] = random_clue
        context['repeat'] = repeat

        context['total'] = self.request.session['total']
        context['correct'] = self.request.session['correct']

        return context


    def post(self, request, *args, **kwargs):
        # check if clue id exists in current session / if not, redirect to drill page
        if not request.session.has_key('clue_id'):
            self.request.session['repeat'] = False
            return HttpResponseRedirect(reverse('drill'))

        # Get clue ID
        clue_id = self.request.session['clue_id']

        # Fetch POST field from Entry Form
        entry_form = EntryForm(request.POST or None)
        entry_text = entry_form['entry_text'].value()

        # validate entry text
        if not isinstance(entry_text, six.text_type):
            raise Exception('Entry Text must be a string')

        # Get Clue Data and find match with entry text
        clue_match = Clue.objects.get(pk=clue_id)
        entry_match = Entry.objects.filter(entry_text=entry_text.upper()).first()

        logger = logging.getLogger(__name__)
        if entry_match == clue_match.entry:
            # keep track of correct answers (int), wrong answer (bool), and success qnw3
            logger.info('Match found')
            self.request.session['correct'] += 1
            self.request.session['repeat'] = False
            self.request.session['success'] = True

            # Redirects to the view product of product details and for review
            return HttpResponseRedirect(reverse('answer'))

        logger.info("Match not found")
        request.session['repeat'] = True
        return HttpResponseRedirect(reverse('drill'))




# view to congratulates the user on their success
class AnswerView(TemplateView):
    template_name = 'answer.html'

    def get_context_data(self, **kwargs):
       context = super(AnswerView, self).get_context_data(**kwargs)

       # check if clue id exists in current session / if not, redirect to drill page
       if not self.request.session.has_key('clue_id'):
           return HttpResponseRedirect(reverse('drill'))

       # reset repeat clue option to default
       if self.request.session.has_key('repeat'):
          self.request.session['repeat'] = False

       # get clue ID from current session
       clue_id = self.request.session['clue_id']

       # get clue information from DB
       try:
           clue = Clue.objects.get(pk=clue_id)

       except Clue.DoesNotExist:
          raise Http404("Such Clue Does Not Exist")

       # get information for puzzles that include clue text
       puzzles = Puzzle.objects.get_clue_puzzles(clue.clue_text)

       # add data to context for templates
       context['puzzles'] = puzzles
       context['clue'] = clue

       context['total'] = self.request.session['total']
       context['correct'] = self.request.session['correct']
       context['success'] = self.request.session['success']

       return context
