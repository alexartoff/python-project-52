from django.db import models
from django.utils.translation import gettext_lazy as _
from task_manager.users.models import Users
from task_manager.statuses.models import Statuses
from task_manager.labels.models import Labels


# Create your models here.
class Tasks(models.Model):
    name = models.CharField(
        max_length=150,
        blank=False,
        unique=True,
        verbose_name=_('Task name')
    )
    author = models.ForeignKey(
        Users,
        on_delete=models.PROTECT,
        related_name='author',
        verbose_name=_('Author')
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created')
    )
    description = models.TextField(
        blank=True,
        verbose_name=_('Description')
    )
    status = models.ForeignKey(
        Statuses,
        on_delete=models.PROTECT,
        verbose_name=_('Status')
    )
    executor = models.ForeignKey(
        Users,
        on_delete=models.PROTECT,
        related_name='executor',
        verbose_name=_('Executor')
    )
    labels = models.ManyToManyField(
        Labels,
        related_name='label',
        blank=True,
        through='TaskRelationLabel',
        verbose_name=_('Labels')
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("=Task=")
        verbose_name_plural = _("=Tasks=")


class TaskRelationLabel(models.Model):
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE)
    label = models.ForeignKey(Labels, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.task} - {self.label}"
