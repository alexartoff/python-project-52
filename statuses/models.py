from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Statuses(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_('Status name')
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created')
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("=Status=")
        verbose_name_plural = _("=Statuses=")

    def save(self, *args, **kwargs):
        self.validate_unique()
        super(Statuses, self).save(*args, **kwargs)
