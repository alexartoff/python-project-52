from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = 'task_manager.users'
    verbose_name = _("=Task's user=")
    verbose_name_plural = _("=Task's users=")
