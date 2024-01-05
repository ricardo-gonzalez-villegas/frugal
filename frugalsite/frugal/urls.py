from django.urls import path

from . import views

urlpatterns = [
    path("", views.welcome_view, name="welcome"),
    path("home", views.home_view, name="home"),
    path("register", views.registration_view, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("search", views.search_view, name="search"),
    path("results", views.results_view, name="results"),
    path("favorite", views.favorite_view, name="favorite"),
    path("favorites", views.favorites_view, name="favorites"),
    path("favorites/<str:favorite_id>/details", views.favorite_details, name="details"),
    path("favorites/<str:favorite_id>/delete", views.favorite_delete, name="delete"),
]