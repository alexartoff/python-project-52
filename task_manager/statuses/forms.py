from django import forms

from .models import Statuses


class StatusForm(forms.ModelForm):

    class Meta:
        model = Statuses
        fields = [
            'name',
        ]
