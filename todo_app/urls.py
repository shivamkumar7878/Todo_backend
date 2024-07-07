from django.urls import path
from .views.todo import ToDoListCreate, ToDoRetrieveUpdateDestroy
from .views.auth import RegisterView, LoginView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('login/', LoginView.as_view(), name='auth_login'),
    path('todos/', ToDoListCreate.as_view(), name='todo-list-create'),
    path('todos/<int:pk>/', ToDoRetrieveUpdateDestroy.as_view(), name='todo-retrieve-update-destroy'),
]
