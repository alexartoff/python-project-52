from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import ProtectedError
from django.utils.translation import gettext_lazy as _

from .forms import LabelForm
from .models import Labels


# Create your views here.
class LabelsListView(LoginRequiredMixin, ListView):
    template_name = 'labels.html'
    model = Labels
    ordering = 'id'
    context_object_name = 'labels'
    login_url = reverse_lazy('user_login')
    extra_context = {'title': _('Labels')}


class LabelCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    form_class = LabelForm
    template_name = 'create.html'
    success_message = _("Label '%(name)s' created successfully")
    success_url = reverse_lazy('labels_list')
    login_url = reverse_lazy('user_login')
    extra_context = {'title': _('Create label')}


class LabelUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Labels
    form_class = LabelForm
    template_name = 'update.html'
    success_message = _('%(name)s successfully changed')
    success_url = reverse_lazy('labels_list')
    extra_context = {'title': _('Update label')}


class LabelDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Labels
    success_url = reverse_lazy('labels_list')
    template_name = 'confirm_delete.html'
    extra_context = {'title': _('Delete label')}

    def post(self, request, *args, **kwargs):
        try:
            self.delete(request, *args, **kwargs)
            messages.success(
                self.request,
                _('Successfully deleted')
            )
            return redirect(reverse_lazy('labels_list'))
        except ProtectedError:
            messages.error(
                self.request,
                _("Error! Can't delete, label in use")
            )
            return redirect(reverse_lazy('labels_list'))
