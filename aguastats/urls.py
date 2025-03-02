# aguastats/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('painel/', views.dashboard, name='dashboard'),
    path('meu-relogio/', views.my_water_usage, name='my_water_usage'),
    path('relogio/<int:user_id>/', views.user_water_usage, name='user_water_usage'),
]