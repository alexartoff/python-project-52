from django.contrib import admin

from users.models import Users


class UsersAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'first_name', 'username',
        'last_name', 'is_superuser', "is_active"
    )
    list_display_links = ('id', 'username', 'first_name', 'last_name')
    search_fields = ('username', 'last_name')
    ordering = ['id', ]


admin.site.register(Users, UsersAdmin)
