from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class TasksConfig(AppConfig):
    name = 'task_manager.tasks'
    verbose_name = _("=Task=")
    verbose_name_plural = _("=Tasks=")
