from django.urls import path
from gastos.views import APIListarGastos,APICriarGasto,APIExcluirGasto,APIEditarGasto, APIListarPorBancos

urlpatterns = [
    path('api/', APIListarGastos.as_view(), name='api-listar-gastos'),
    path('api/por-bancos', APIListarPorBancos.as_view(), name='api-listar-gastos-por-banco'),
    path('api/criar/', APICriarGasto.as_view(), name='api-criar-gasto'),
    path('api/excluir/<int:pk>/', APIExcluirGasto.as_view(), name='api-excluir-gasto'),
    path('api/editar/<int:pk>/', APIEditarGasto.as_view(), name='api-editar-gasto')
]
