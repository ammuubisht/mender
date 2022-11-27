from django.urls import path
from main.views import *
from . import views

urlpatterns = [
    path('', views.Home, name="home"),
    path('movie', views.Movie, name="movie"),
    path('about', views.About, name="about"),
    path('404', views.Error, name="error"),
    path('shows', views.Shows, name="shows"),
]
