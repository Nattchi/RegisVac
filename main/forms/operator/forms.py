# -*- coding: utf-8 -*-
# Project: RegisVac
from django.contrib.auth import password_validation
from django.contrib.auth.models import Group, User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError
from django.utils.html import format_html_join, format_html
from django.utils.translation import gettext_lazy as _

from main.models import Operator


def jp_password1_help_text():
    help_texts = ['パスワードは他の個人情報と類似していないものにしてください。', 'パスワードは8文字以上である必要があります。',
                  'パスワードは一般的に使用されていないものにしなければなりません。', 'パスワードをすべて数字のみにすることはできません。']
    help_items = format_html_join('', '<li>{}</li>', ((help_text,) for help_text in help_texts))
    return format_html('<ul>{}</ul>', help_items) if help_items else ''


class JPUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'is_staff']
        labels = {
            'username': 'ユーザー名',
            'first_name': '姓',
            'last_name': '名',
            'email': 'メールアドレス',
            'is_staff': 'あなたはスタッフですか?',
        }
        help_texts = {
            'username': 'パスワードは150文字以下であること。文字、数字、記号 @ / . / + / - / _ のみ使用できます。',
            'is_staff': 'ユーザーがこの管理サイトにログインできるかどうかを指定します。',

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # ラベルを日本語化
        self.fields['password1'].label = 'パスワード'
        self.fields['password2'].label = '確認用パスワード'

        # エラーメッセージを日本語化
        self.error_messages['password_mismatch'] = '入力された2つのパスワードが一致しません。'

        # ヘルプテキストを日本語化
        self.fields['password1'].help_text = jp_password1_help_text()
        self.fields['password2'].help_text = '確認のため、もう一度パスワードを入力してください。'

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error('password2', error)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


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
        queryset=Group.objects.exclude(id=1),  # adminを除外する
    )


# 操作者に、削除フラグを設定する
class OperatorRemoveForm(forms.ModelForm):
    class Meta:
        model = Operator
        fields = ['id']
