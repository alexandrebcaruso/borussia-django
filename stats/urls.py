from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='painel'),
    path('painel/', views.dashboard, name='painel'),
    path('well/<int:well_id>/', views.water_well_usage, name='well_usage'),
]