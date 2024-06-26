from django.contrib import admin
from gastos.models import Gasto

class GastoAdmin(admin.ModelAdmin):
    list_display = ['id','descricao','categoria','parcela_atual','parcelas_totais', 'valor_parcela_atual','valor_total', 'data_compra', 'tipo_pagamento', 'usuario', 'banco', 'quitada', 'data_quitacao_prevista']
    search_fields = ['descricao']

admin.site.register(Gasto, GastoAdmin)
