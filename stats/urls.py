from django.urls import path
from stats import api
from . import views

urlpatterns = [
    path('', views.dashboard, name='painel'),
    path('painel/', views.dashboard, name='painel'),
    path('poco/<int:well_id>/', views.water_well_usage, name='poco_detalhe'),
    path('painel/api/wells-geojson/', api.wells_geojson, name='wells_geojson'),
]