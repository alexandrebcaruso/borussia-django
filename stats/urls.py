from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='painel'),
    path('painel/', views.dashboard, name='painel'),
    path('relogio/<int:user_id>/', views.user_water_usage, name='relogio'),
]