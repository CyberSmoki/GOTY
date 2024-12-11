from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("results", views.results, name="results"),
    path("vote", views.vote, name="vote"),
    path("app/login", views.login, name="login"),
    path("app/logout", views.logout, name="logout"),
    path("app/oauth2", views.oauth2, name="oauth2"),
    path("app/vote", views.vote_post, name="vote_post"),
    path("faq", views.faq, name="faq")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
