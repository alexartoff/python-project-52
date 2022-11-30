from django.urls import path

from .views import TasksListView, TaskCreateView, \
    TaskUpdateView, TaskDeleteView, TaskShowView

urlpatterns = [
    path('', TasksListView.as_view(), name='tasks_list'),
    path('create/', TaskCreateView.as_view(), name='add_task'),
    path('<int:pk>/update/', TaskUpdateView.as_view(), name='task_update'),
    path('<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),
    path('<int:pk>/', TaskShowView.as_view(), name='show_task'),
]
