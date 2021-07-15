from django.views import generic
from django.shortcuts import render

from main.models import Group
from main.constants import AUTH_ADMIN, AUTH_STAFF


# 暫定ポータル画面へ移動
class Home(generic.TemplateView):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        # redirect_url = super(Home, self).get(request, *args, **kwargs)
        context = super(Home, self).get_context_data()

        # login_user_name = request.user.first_name + request.user.last_name + 'さん'
        # context.update({
        #     'login_user_name': login_user_name,
        #})

        return render(request, 'home.html', context)

    def get_level(self, request):
        user = request.user

        groups = Group.objects.filter(user__id=user.id)
        if groups is None or len(groups) == 0:
            return AUTH_ADMIN   # 管理者
        return groups[0].id

