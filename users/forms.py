from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Users


class UsersForm(UserCreationForm):
    password1 = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput()
    )

    class Meta:
        model = Users
        fields = [
            'username',
            'first_name',
            'last_name',
            'password1',
            'password2'
        ]

    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username) <= 3:
            raise ValidationError(
                _(f'Username "{username}" is too short! minimum 4 symbols')
            )
        return username


class UsersLoginForm(AuthenticationForm):
    class Meta:
        model = Users
        fields = [
            'username',
            'password'
        ]
