# -*- coding: utf-8 -*-
# Project: RegisVac
import re

from django.contrib.auth import password_validation
from django.contrib.auth.models import Group, User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError
from django.utils.html import format_html_join, format_html

from main.models import Operator


def jp_password1_help_text():
    help_texts = ['パスワードは他の個人情報と類似していないものにしてください。', 'パスワードは8文字以上である必要があります。',
                  'パスワードは一般的に使用されていないものにしなければなりません。', 'パスワードをすべて数字のみにすることはできません。']
    help_items = format_html_join('', '<li class="error">{}</li>', ((help_text,) for help_text in help_texts))
    return format_html('<ul>{}</ul>', help_items) if help_items else ''


class JPUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'is_staff']
        labels = {
            'username': 'ユーザー名 [必須]',
            'first_name': '姓',
            'last_name': '名',
            'email': 'メールアドレス',
            'is_staff': 'あなたはスタッフですか?',
        }
        help_texts = {
            'username': 'ユーザー名は150文字以下で、文字、数字、記号 @ / . / + / - / _ のみ使用できます。',
            'is_staff': 'ユーザーがこの管理サイトにログインできるかどうかを指定します。',
        }
        error_messages = {
            'username': {
                'invaild_username_length': 'ユーザー名は150文字以下のものを入力してください。',
                'invalid_format_username': 'ユーザー名には 文字、数字、記号 @ / . / + / - / _ のみ使用できます。',
            },
            'email': {
                'invalid_format_email': 'メールアドレスの入力に誤りがあります。',
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # ラベルを日本語化
        self.fields['password1'].label = 'パスワード [必須]'
        self.fields['password2'].label = '確認用パスワード [必須]'

        # エラーメッセージを日本語化
        self.error_messages['password_mismatch'] = '入力された2つのパスワードが一致しません。'

        # ヘルプテキストを日本語化
        self.fields['password1'].help_text = jp_password1_help_text()
        self.fields['password2'].help_text = '確認のため、もう一度パスワードを入力してください。'

    def clean_username(self):
        username = self.cleaned_data.get("username")

        if (len(username) > 150 or len(username) <= 0):
            raise ValidationError(
                self.error_messages['invaild_username_length'],
                code='invaild_username_length',
            )
        if not re.search(r"[\w\d@.+-]+", username):
            raise ValidationError(
                self.error_messages['invalid_format_username'],
                code='invalid_format_username',
            )

        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if email and not re.match(r"^[\w\-.]+@[\w\-.]+\.[A-Za-z]+$", email):
            raise ValidationError(
                self.error_messages['invalid_format_email'],
                code='invalid_format_email',
            )

        return email

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
                self.add_error('password1', error)

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
