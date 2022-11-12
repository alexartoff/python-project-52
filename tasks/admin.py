from django.contrib import admin

from .models import Tasks


class TasksAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'author', 'executor', 'status', "created_date"
    )
    list_display_links = (
        'id', 'name', 'author', 'executor', 'status', "created_date"
    )
    search_fields = ('name', 'status')
    ordering = ['id', ]


admin.site.register(Tasks, TasksAdmin)
