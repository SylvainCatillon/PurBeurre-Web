from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('legal/', views.legal, name='legal'),
]
