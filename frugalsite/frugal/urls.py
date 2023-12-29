<<<<<<< HEAD:frugalsite/frugalapp/urls.py
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("frugalapp.urls")),
=======
from django.urls import path

from . import views

urlpatterns = [
    path("", views.home_view, name="home"),
    path("welcome", views.welcome_view, name="welcome"),
    path("register", views.registration_view, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("search", views.search_view, name="search"),
    path("results", views.results_view, name="results"),
    path("favorite", views.favorite_view, name="favorite"),
    path("favorite/<int:favorite_id>", views.favorite_details, name="details")
>>>>>>> 9fd34bf (deleted apps and created all views in single app):frugalsite/frugal/urls.py
]