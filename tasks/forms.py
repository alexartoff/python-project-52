from django import forms
# from django.utils.translation import gettext_lazy as _

from .models import Tasks


class TaskForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = [
            'name',
            'description',
            'status',
            'executor',
            'labels',
        ]
