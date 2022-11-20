from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, \
    ListView, DetailView
from django_filters.views import FilterView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import ProtectedError
from django.utils.translation import gettext_lazy as _
from django.db.models import Q

from .forms import TaskForm
from .models import Tasks
from users.models import Users
from .filter import TaskFilter


class TasksListView(LoginRequiredMixin, FilterView):
    template_name = 'tasks.html'
    model = Tasks
    login_url = reverse_lazy('user_login')
    filterset_class = TaskFilter
    extra_context = {'title': _('Tasks')}
    ordering = ['id']


class TaskShowView(LoginRequiredMixin, DetailView):
    template_name = 'show_task.html'
    model = Tasks
    context_object_name = 'task'
    login_url = reverse_lazy('user_login')
    extra_context = {'title': _('Show task')}


class SearchResultView(ListView):
    template_name = 'search.html'
    model = Tasks
    context_object_name = 'search'
    ordering = ['id']

    def get_queryset(self):
        query = self.request.GET.get("q")
        return Tasks.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    def get_context_data(self, **kwargs):
        context = super(SearchResultView, self).get_context_data(**kwargs)
        context['query_search'] = self.request.GET.get('q')
        context['title'] = _('Search results')
        return context


class TaskCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    form_class = TaskForm
    template_name = 'create.html'
    success_message = _("Task '%(name)s' created successfully")
    success_url = reverse_lazy('tasks_list')
    login_url = reverse_lazy('user_login')
    extra_context = {'title': _('Create task')}

    def form_valid(self, form):
        form.instance.author = Users.objects.get(pk=self.request.user.pk)
        return super().form_valid(form)


class TaskUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Tasks
    form_class = TaskForm
    template_name = 'update.html'
    success_message = _('%(name)s successfully changed')
    success_url = reverse_lazy('tasks_list')
    extra_context = {'title': _('Update task')}


class TaskDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Tasks
    success_url = reverse_lazy('tasks_list')
    template_name = 'confirm_delete.html'
    extra_context = {'title': _('Delete task')}

    def post(self, request, *args, **kwargs):
        try:
            self.delete(request, *args, **kwargs)
            messages.success(
                self.request,
                _('Successfully deleted')
            )
            return redirect(reverse_lazy('tasks_list'))
        except ProtectedError:
            messages.error(
                self.request,
                _("Error! Can't delete, task not done")
            )
            return redirect(reverse_lazy('tasks_list'))
