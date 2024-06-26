from django.urls import path
from gastos.views import APIListarGastos

urlpatterns = [
    path('api/', APIListarGastos.as_view(), name='api-listar-gastos')
]
