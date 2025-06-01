from django.urls import path
from .views import UserCreateView, UserDetailView, TaskCreateView, TaskDetailView, TaskListView

urlpatterns = [
    path('users/', UserCreateView.as_view(), name='user-create'),
    path('users/<int:id>/', UserDetailView.as_view(), name='user-detail'),
    path('tasks/', TaskCreateView.as_view(), name='task-create'),
    path('tasks/<int:id>/', TaskDetailView.as_view(), name='task-detail'),
    path('tasks/list/', TaskListView.as_view(), name='task-list'),
]