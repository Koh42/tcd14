from django.urls import path

from . import views

urlpatterns = [
    path("", views.redirect_oauth, name="index"),
    path("code", views.receive_oauth_code, name="oauth"),
    path("logout", views.logout, name="logout"),
    path("me", views.me, name="me"),
]