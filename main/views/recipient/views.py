# -*- coding: utf-8 -*-
# Project: RegisVac

from django.views import generic
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.models import Group, User
from django.contrib.auth.mixins import LoginRequiredMixin

from main.models import Recipient
from main.forms.recipient.forms import MyRecipientCreationForm, RecipientCreationForm, RecipientRemoveForm

app_name = 'main'


# 一覧画面
class RecipientListView(LoginRequiredMixin, generic.ListView):
    model = Recipient
    template_name = "main/Recipient/Recipient_list.html"
    #recipient_list = User.objects.order_by('username')
    success_url = reverse_lazy('home')

# 登録画面
# まっさらな状態
class RecipientCreateView(CreateView):
    model = Recipient
    form_class = MyRecipientCreationForm
    template_name = "main/Recipient/Recipient_form.html"
    success_url = reverse_lazy('main:recipient_list')


# 更新画面
class RecipientUpdateView(UpdateView):
    model = Recipient
    form_class = MyRecipientCreationForm
    template_name = "main/Recipient/Recipient_form.html"
    success_url = reverse_lazy('main:recipient_list')


