# -*- coding: utf-8 -*-
# Project: RegisVac

from django.contrib.auth.models import Group, User
from django.contrib.auth.forms import UserCreationForm
from django import forms

from main.models import Operator


class MyUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'is_staff']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 順番の都合で、姓と名を入れ替える
        self.fields['first_name'].label = '姓'
        self.fields['last_name'].label = '名'


class OperatorCreationForm(forms.ModelForm):
    class Meta(forms.ModelForm):
        model = Operator
        fields = []

    auth_group = forms.ModelChoiceField(
        label="役割",
        queryset=Group.objects.exclude(id=1),    # adminを除外する
    )


# 操作者に、削除フラグを設定する
class OperatorRemoveForm(forms.ModelForm):
    class Meta:
        model = Operator
        fields = ['id']

