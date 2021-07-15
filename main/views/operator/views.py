# -*- coding: utf-8 -*-
# Project: RegisVac

from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.models import Group, User
from django.contrib.auth.mixins import LoginRequiredMixin

from main.forms.operator.forms import OperatorCreationForm, OperatorRemoveForm, JPUserCreationForm

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

    def get(self, request, *args, **kwargs):
        user_form = JPUserCreationForm()
        operator_form = OperatorCreationForm()
        context = {
            'user_form': user_form,
            'operator_form': operator_form,
        }
        return render(request, 'main/operator/operator_form.html', context)

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_superuser = False
        user.is_active = True
        user.save()

        operator = user.operator
        operator.hidden_flag = False
        operator.save()

        auth_group_id = int(self.request.POST.get('auth_group', None))
        my_group = Group.objects.get(id=auth_group_id)
        my_group.user_set.add(user)
        return redirect("main:operator_list")


# 更新画面
class OperatorUpdateView(UpdateView):
    model = User
    form_class = JPUserCreationForm
    template_name = "main/operator/operator_form.html"
    success_url = reverse_lazy('main:operator_list')
    object = None

    def get(self, request, *args, **kwargs):
        # ユーザID
        user_id = kwargs['pk']
        user = User.objects.get(pk=user_id)
        self.object = user
        user_form = self.get_form(self.form_class)
        context = self.get_context_data(object=self.object, form=user_form)
        user_form = context['form']

        operator = user.operator
        self.object = operator
        operator_form = self.get_form(OperatorCreationForm)
        context = self.get_context_data(object=operator, form=operator_form)
        operator_form = context["operator_form"]

        context = {
              'form': user_form,
              'operator_form': operator_form,
        }
        self.object = user

        return render(request, 'main/operator/operator_form.html', context)

    def form_valid(self, form):
        user = form.save(commit=False)
        user.save()

        operator = user.operator
        operator.title = self.request.POST.get('title', None)
        operator.save()

        old_groups = user.groups.all()
        for g in old_groups:
            g.user_set.remove(user)
        auth_group_id = int(self.request.POST.get('auth_group', None))
        my_group = Group.objects.get(id=auth_group_id)
        my_group.user_set.add(user)
        return redirect("main:operator_list")

    def get_context_data(self, **kwargs):
        # スーパークラスのget_context_dataを使うとobject_listに
        # 表示中のモデルの情報が入るのでそれを利用
        context = super(OperatorUpdateView, self).get_context_data(**kwargs)
        args = (self.get_form_kwargs())
        if 'Operator' in str(type(args['instance'])):
            operator = args['instance']
            user = User.objects.get(pk=operator.user_id)
            groups = user.groups.all()
            # 複数のグループには、所属しない前提
            if len(groups) > 0:
                group = groups[0]
                initial = args['initial']
                initial.update(auth_group=group)
                args['initial'] = initial

        user_form = JPUserCreationForm(**args)
        operator_form = OperatorCreationForm(**args)

        # contextは辞書型
        context.update({
            'form': user_form,
            'operator_form': operator_form,
        })
        return context

