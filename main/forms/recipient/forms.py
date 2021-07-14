# -*- coding: utf-8 -*-
# Project: RegisVac

from django.contrib.auth.models import Group, User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django import forms

from main.models import Recipient


class RecipientForm(ModelForm):
    class Meta:
        model = Recipient
        fields = '__all__'


class MyRecipientCreationForm(RecipientForm):
    class Meta(RecipientForm):
        model = Recipient
        fields = ['ID', 'last_name', 'first_name', 'date_of_birth', 'Email_address', 'Phonenumber', 'Address', 'Basic_illness','status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['last_name'].label = '姓'
        self.fields['first_name'].label = '名'


class RecipientCreationForm(ModelForm):
    class Meta(ModelForm):
        model = Recipient
        fields = []

    auth_group = forms.ModelChoiceField(
            label="役割",
            queryset=Group.objects.exclude(id=1),  # adminを除外する
    )


# 操作者に、削除フラグを設定する
class RecipientRemoveForm(ModelForm):
    class Meta:
        model = Recipient
        fields = '__all__'

