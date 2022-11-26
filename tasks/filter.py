import django_filters
from django import forms

from labels.models import Labels
from tasks.models import Tasks
from django.utils.translation import gettext_lazy as _


class TaskFilter(django_filters.FilterSet):
    own_tasks = django_filters.BooleanFilter(
        method='show_own_task',
        widget=forms.CheckboxInput,
        label=_('Show own tasks'),
    )
    labels = django_filters.ModelChoiceFilter(
        queryset=Labels.objects.all(),
        label=_('Label'),
    )

    def show_own_task(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset

    class Meta:
        model = Tasks
        fields = ['status', 'executor', 'labels', 'own_tasks']
        filter_overrides = {
            django_filters.BooleanFilter: {
                'filter_class': django_filters.BooleanFilter,
                'extra': lambda f: {
                    'widget': forms.CheckboxInput,
                },
            },
        }
