from django.contrib import admin

from .models import Operator, Recipient

admin.site.register(Operator)
admin.site.register(Recipient)

