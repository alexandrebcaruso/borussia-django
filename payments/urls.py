from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('pagamentos/', views.user_payments, name='pagamentos'),
    path('enviar-comprovante/<int:year>/<int:month>/', views.upload_receipt, name='enviar_comprovante'),
    path('gestao-pagamentos/', views.payment_list, name='gestao_pagamentos'),
    path('historico-pagamentos/<int:user_id>/<int:year>/<int:month>/', views.payment_history, name='historico_pagamentos'),
]
