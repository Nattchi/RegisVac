# -*- coding: utf-8 -*-
# Project: RegisVac

from django.views import generic
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.models import Group, User
from django.contrib.auth.mixins import LoginRequiredMixin

from main.forms.operator.forms import MyUserCreationForm, OperatorCreationForm, OperatorRemoveForm, JPUserCreationForm

app_name = 'main'


# 一覧画面
class OperatorListView(LoginRequiredMixin, generic.ListView):
    model = User
    template_name = "main/operator/operator_list.html"
    object_list = User.objects.order_by('username')
    success_url = reverse_lazy('home')


# 登録画面
# まっさらな状態
class OperatorCreateView(CreateView):
    model = User
    form_class = JPUserCreationForm
    template_name = "main/operator/operator_form.html"
    success_url = reverse_lazy('main:operator_list')


# 更新画面
class OperatorUpdateView(UpdateView):
    model = User
    form_class = JPUserCreationForm
    template_name = "main/operator/operator_form.html"
    success_url = reverse_lazy('main:operator_list')

