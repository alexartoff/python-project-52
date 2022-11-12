from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import ProtectedError
from django.utils.translation import gettext_lazy as _

from .forms import StatusForm
from .models import Statuses


# Create your views here.
class StatusesListView(LoginRequiredMixin, ListView):
    template_name = 'statuses.html'
    model = Statuses
    ordering = 'id'
    context_object_name = 'statuses'
    login_url = reverse_lazy('user_login')
    extra_context = {'title': _('Statuses')}


class StatusCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    form_class = StatusForm
    template_name = 'create.html'
    success_message = _("Status '%(name)s' created successfully")
    success_url = reverse_lazy('statuses_list')
    login_url = reverse_lazy('user_login')
    extra_context = {'title': _('Create status')}


class StatusUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Statuses
    form_class = StatusForm
    template_name = 'update.html'
    success_message = _('%(name)s successfully changed')
    success_url = reverse_lazy('statuses_list')
    extra_context = {'title': _('Update status')}


class StatusDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Statuses
    success_url = reverse_lazy('statuses_list')
    template_name = 'confirm_delete.html'
    extra_context = {'title': _('Delete status')}

    def post(self, request, *args, **kwargs):
        try:
            self.delete(request, *args, **kwargs)
            messages.success(
                self.request,
                _('Successfully deleted')
            )
            return redirect(reverse_lazy('statuses_list'))
        except ProtectedError:
            messages.error(
                self.request,
                _("Error! Can't delete, status in use")
            )
            return redirect(reverse_lazy('statuses_list'))
