from django.contrib import admin

from .models import Labels


class LabelsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_date',)
    list_display_links = ('id', 'name',)
    search_fields = ('name',)
    ordering = ['id', ]


admin.site.register(Labels, LabelsAdmin)
