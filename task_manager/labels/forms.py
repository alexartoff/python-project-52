from django import forms

from .models import Labels


class LabelForm(forms.ModelForm):
    class Meta:
        model = Labels
        fields = [
            'name',
        ]
