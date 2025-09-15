from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'app'

router = DefaultRouter()

router.register(r'news', views.NoticiaViewset, basename = "news")
router.register(r'users', views.UsuarioViewset, basename = "users")
router.register(r'posts', views.PostagemViewset, basename = "posts")

urlpatterns = [
    path('', include(router.urls)),
    path('login/', views.LoginView.as_view(), name = "login"),
]
