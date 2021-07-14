from django.contrib import admin

from .models import Operator, Recipient

admin.site.register(Operator)
#admin.site.register(Recipient)


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'status', 'ID')
    search_fields = ('last_name', 'first_name', 'ID')
    list_filter = ['status']
    list_per_page = 10
