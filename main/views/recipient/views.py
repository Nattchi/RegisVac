# -*- coding: utf-8 -*-
# Project: RegisVac

from django.views import generic
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.models import Group, User
from django.contrib.auth.mixins import LoginRequiredMixin

from main.forms.operator.forms import MyUserCreationForm, OperatorCreationForm, OperatorRemoveForm

app_name = 'main'


# 一覧画面
class RecipientListView(LoginRequiredMixin, generic.ListView):
    model = User
    template_name = "main/Recipient/Recipient_list.html"
    object_list = User.objects.order_by('username')
    success_url = reverse_lazy('home')

