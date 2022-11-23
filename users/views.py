from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import ProtectedError
from django.utils.translation import gettext_lazy as _

from .forms import UsersForm, UsersLoginForm
from .models import Users


# Create your views here.
class UsersListView(ListView):
    template_name = 'users.html'
    model = Users
    ordering = 'id'
    context_object_name = 'users'
    extra_context = {'title': _('Users')}


class UserRegisterView(SuccessMessageMixin, CreateView):
    form_class = UsersForm
    template_name = 'register.html'
    success_message = _('%(username)s created successfully')
    success_url = reverse_lazy('user_login')
    extra_context = {'title': _('Create user')}


class UserUpdateView(
    SuccessMessageMixin,
    LoginRequiredMixin,
    UserPassesTestMixin,
    UpdateView
):
    model = Users
    form_class = UsersForm
    template_name = 'update.html'
    success_message = _('%(username)s successfully changed')
    success_url = reverse_lazy('users_list')
    extra_context = {'title': _('Update user')}

    def test_func(self):
        obj = self.get_object()
        return obj.username == self.request.user.username

    def form_valid(self, form):
        obj = form.save()
        login(self.request, obj)
        return redirect(reverse_lazy('index_page'))

    def handle_no_permission(self):
        messages.error(self.request, _("You have't permission!"))
        return redirect(reverse_lazy('users_list'))


class UserDeleteView(
    SuccessMessageMixin,
    LoginRequiredMixin,
    UserPassesTestMixin,
    DeleteView
):
    model = Users
    success_url = reverse_lazy('users_list')
    template_name = 'confirm_delete.html'
    extra_context = {'title': _('Delete user')}

    def test_func(self):
        obj = self.get_object()
        return obj.username == self.request.user.username

    def handle_no_permission(self):
        messages.error(self.request, _("You have't permission!"))
        return redirect(reverse_lazy('users_list'))

    def post(self, request, *args, **kwargs):
        try:
            self.delete(request, *args, **kwargs)
            messages.success(self.request, _('Successfully deleted'))
            return redirect(reverse_lazy('users_list'))
        except ProtectedError:
            messages.error(self.request, _("Error! Can't delete"))
            return redirect(reverse_lazy('users_list'))


class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = 'login.html'
    form_class = UsersLoginForm
    success_message = _('Successfully login')
    next_page = reverse_lazy('index_page')
    extra_context = {'title': _('Login')}

    def form_invalid(self, form):
        messages.error(
            self.request,
            _('Error! Enter correct username & password.')
        )
        return redirect(reverse_lazy('user_login'))


def logout_user(request):
    logout(request)
    messages.info(request, _('Successfully logout'))
    return redirect('index_page')
