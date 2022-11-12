from django.contrib.auth.models import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class Users(AbstractUser):
    username = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_('Username')
    )
    password = models.CharField(
        max_length=128,
        verbose_name=_('Password')
    )
    first_name = models.CharField(
        max_length=100,
        default='NONAME',
        verbose_name=_('First name')
    )
    last_name = models.CharField(
        max_length=100,
        verbose_name=_('Last name')
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Active user')
    )
    date_joined = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created')
    )
    last_login = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_('Last login')
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name=_('Staff')
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.first_name} aka "{self.username}"'

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = _("=User=")
        verbose_name_plural = _("=Users=")

    def save(self, *args, **kwargs):
        self.validate_unique()
        super(Users, self).save(*args, **kwargs)
