# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.LogInView.as_view(), name='login'),
    url(r'^drill/$', views.DrillView.as_view(), name='drill'),
    url(r"^answer/$", views.AnswerView.as_view(), name='answer'),

]
