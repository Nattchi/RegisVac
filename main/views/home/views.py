from django.views import generic
from django.shortcuts import render


# 暫定ポータル画面へ移動
class Home(generic.TemplateView):
    template_name = 'home.html'
