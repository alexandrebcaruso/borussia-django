from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('entrar/', views.user_login, name='entrar'),
    path('sair/', views.user_logout, name='sair'),
    path('meus-pagamentos/', views.my_payments, name='meus_pagamentos'),
    path('perfil/', views.profile, name='perfil'),
    path('enviar-comprovante/<int:year>/<int:month>/', views.upload_receipt, name='enviar_comprovante'),
    path('gestao-pagamentos/', views.payment_list, name='gestao_pagamentos'),
    path('historico-pagamentos/<int:user_id>/<int:year>/<int:month>/', views.payment_history, name='historico_pagamentos'),
]
