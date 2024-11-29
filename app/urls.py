from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("app/oauth2", views.oauth2, name="oauth2"),
    path("app/logout", views.logout, name="logout")
]