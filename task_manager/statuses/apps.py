from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class StatusesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'task_manager.statuses'
    verbose_name = _("=Task's status=")
    verbose_name_plural = _("=Task's statuses=")
