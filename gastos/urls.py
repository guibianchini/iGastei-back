from django.urls import path
from gastos.views import APIListarVeiculos

urlpatterns = [
    path('api/', APIListarVeiculos.as_view(), name='api-listar-veiculos')
]
