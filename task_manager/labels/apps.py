from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class LabelsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'task_manager.labels'
    verbose_name = _("=Task's label=")
    verbose_name_plural = _("=Task's labels=")
