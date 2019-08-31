from django.urls import path

from .views import IndexView, LoginView, LogoutView

app_name = 'mock_login'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
