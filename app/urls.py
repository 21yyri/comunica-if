from django.urls import path
from .views import *

urlpatterns = [
    path("login/", Login.as_view(), name="login"),
    path("postagem/<int:pk>", Postagens.as_view(), name="postagem-detail"),
    path("noticia/<int:pk>", Noticias.as_view(), name="noticia"),
    path("noticia/", Noticias.as_view(), name="noticia"),
    path("postagem/", Postagens.as_view(), name="postagem"),
    path("carrossel/", Carrossel.as_view(), name="carrossel"),
    path("healthcheck/", Healthcheck.as_view(), name="healthcheck")
]
