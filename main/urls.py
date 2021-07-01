# -*- coding: utf-8 -*-
# Project: RegisVac

from django.urls import path

from main.views.home.views import Home
from main.views.operator.views import OperatorListView, OperatorCreateView

app_name = 'main'

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('operators', OperatorListView.as_view(), name='operator_list'),
    path('operators/new', OperatorCreateView.as_view(), name='operator_new'),
]
