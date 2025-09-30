from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from pprint import pprint

app_name = 'app'

router = DefaultRouter()

router.register(r'users', views.UsuarioViewset, basename = "users")
router.register(r'posts', views.PostagemViewset, basename = "posts")
router.register(r'news', views.NoticiaViewset, basename = "news")

urlpatterns = [
    path('', include(router.urls)),
    path('login/', views.LoginView.as_view(), name = "login"),
    path('carrossel', views.Carrossel.as_view(), name = "carrossel"),
    path('news/setor/<str:setor>', views.NoticiaporSetor.as_view(), name = "noticiaporsetor")
]
