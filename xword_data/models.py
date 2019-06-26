# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.manager import Manager

class PuzzleManager(Manager):
    def get_clue_puzzles(self, clue_text):
        return self.filter(_clue_puzzle__clue_text=clue_text)

# Puzzle Model
class Puzzle(models.Model):
    title= models.CharField(max_length=255)
    date= models.DateField(null=False)
    byline= models.CharField(null=False, max_length=255)
    publisher = models.CharField(max_length=12)

    objects = PuzzleManager()

    def __str__(self):
        return f'{self.byline} by {self.publisher} on {self.date}'


# Entry model
class Entry(models.Model):
    entry_text = models.CharField(unique=True, null=False, max_length=50)

    def __str__(self):
        return self.entry_text


# Clue Model
class Clue(models.Model):
    entry = models.ForeignKey(Entry, on_delete=CASCADE, related_name="_clue_entry")
    puzzle = models.ForeignKey(Puzzle, on_delete=CASCADE, related_name="_clue_puzzle")
    clue_text = models.CharField(null=False, max_length=512)
    theme = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.entry.entry_text} - {self.clue_text}'
