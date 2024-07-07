from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from todo_app.views import RegisterView, LoginView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('login/', LoginView.as_view(), name='auth_login'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('todos/', ToDoListCreateView.as_view(), name='todo_list_create'),
    # path('todos/<int:pk>/', ToDoDetailView.as_view(), name='todo_detail'),
]
