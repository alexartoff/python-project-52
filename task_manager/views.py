from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import TemplateView
from django.contrib.auth import login
from django.contrib.auth.views import LogoutView
from django.views.generic.edit import FormView
from django.utils.translation import gettext as _

from task_manager.forms import UserLoginForm


class IndexView(TemplateView):
    template_name = 'index.html'


class UserLoginView(FormView):
    template_name = 'login.html'
    success_url = 'index_page'
    form_class = UserLoginForm

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)

    def form_invalid(self, form):
        error_message = _('invalid data')
        messages.error(self.request, error_message)
        return super().form_invalid(form)


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("index_page")
