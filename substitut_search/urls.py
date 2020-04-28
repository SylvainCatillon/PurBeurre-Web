from django.urls import path

from . import views

app_name = "substitut"
urlpatterns = [
    path('search/', views.search, name='search'),
    path('find/', views.find, name='find'),
    path('detail/', views.detail, name='detail'),
    path('favories/', views.favories, name='favories'),
]
