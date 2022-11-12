from django.contrib import admin

from .models import Statuses


class StatusesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_date',)
    list_display_links = ('id', 'name',)
    search_fields = ('name',)
    ordering = ['id', ]


admin.site.register(Statuses, StatusesAdmin)
