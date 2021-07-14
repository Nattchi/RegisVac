# -*- coding: utf-8 -*-
# Project: RegisVac

from django.urls import path

from main.views.home.views import Home
from main.views.operator.views import OperatorListView, OperatorCreateView, OperatorUpdateView
from main.views.recipient.views import RecipientListView, RecipientUpdateView, RecipientCreateView

app_name = 'main'

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('operators', OperatorListView.as_view(), name='operator_list'),
    path('operators/edit/<int:pk>', OperatorUpdateView.as_view(), name='operator_edit'),
    path('operators/new', OperatorCreateView.as_view(), name='operator_new'),
    path('recipient', RecipientListView.as_view(), name='recipient_list'),
    path('recipient/edit/<str:pk>', RecipientUpdateView.as_view(), name='recipient_edit'),
    path('recipient/new', RecipientCreateView.as_view(), name='recipient_new'),
]
