from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from . import views

app_name = "accounts"
urlpatterns = [
    path('create/', views.create, name='create'),
    path('myaccount/', views.my_account, name='my_account'),
    path(
        'login/',
        LoginView.as_view(template_name='accounts/login.html'),
        name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
