from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('entrar/', views.user_login, name='entrar'),
    path('sair/', views.user_logout, name='sair'),
    path('perfil/', views.profile, name='perfil'),
]
