"""task_manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from task_manager import views
from task_manager.users.views import UserLoginView, logout_user
from django.conf.urls.i18n import i18n_patterns
from task_manager.tasks.views import SearchResultView

urlpatterns = i18n_patterns(
    path('', views.IndexView.as_view(), name='index_page'),
    path('admin/', admin.site.urls),
    path('login/', UserLoginView.as_view(), name='user_login'),
    path('logout/', logout_user, name='user_logout'),
    path('users/', include('task_manager.users.urls')),
    path('statuses/', include('task_manager.statuses.urls')),
    path('tasks/', include('task_manager.tasks.urls')),
    path('labels/', include('task_manager.labels.urls')),
    path('search/', SearchResultView.as_view(), name='search_result'),
    # path('error/', views.error_page)
    prefix_default_language=False
)
