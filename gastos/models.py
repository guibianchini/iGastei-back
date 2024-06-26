from django.db import models
from django.core.exceptions import ValidationError
from datetime import datetime
from django.contrib.auth.models import User
from gastos.consts import OPCOES_BANCOS, OPCOES_TIPO_COMPRA, OPCOES_CATEGORIAS
from dateutil.relativedelta import relativedelta


class Gasto(models.Model):
    descricao = models.CharField(max_length=100)
    categoria = models.SmallIntegerField(choices=OPCOES_CATEGORIAS)
    valor_total = models.DecimalField(max_digits=12, decimal_places=2)
    data_compra = models.DateField()
    tipo_pagamento = models.SmallIntegerField(choices=OPCOES_TIPO_COMPRA)
    usuario = models.ForeignKey(User,related_name='gastos_feitos', on_delete=models.CASCADE)
    banco = models.SmallIntegerField(choices=OPCOES_BANCOS)
    parcelas_totais = models.SmallIntegerField(blank=True, null = True)

    def __str__(self):
        return '{0}'.format(
            self.valor_total,
        )
    

    def clean(self):
        super().clean()
        if self.tipo_pagamento == 2 and (not self.parcelas_totais or self.parcelas_totais < 2):
            raise ValidationError('Campo "Parcelas totais" é obrigatório quando a compra for parcelada.')

    @property
    def parcela_atual(self):
        if self.parcelas_totais is not None and self.tipo_pagamento == 2 and self.data_compra is not None:
            data_quitacao = self.data_compra + relativedelta(months=self.parcelas_totais)
            now = datetime.now()
            if (data_quitacao.year > now.year) or (data_quitacao.year == now.year and data_quitacao.month > now.month):
                return now.month - self.data_compra.month + 1

    @property
    def valor_parcela_atual(self):
        now = datetime.now()
        if self.parcelas_totais is not None and self.tipo_pagamento == 2 and self.data_compra is not None:
            data_quitacao = self.data_compra + relativedelta(months=self.parcelas_totais)
            if (data_quitacao.year > now.year) or (data_quitacao.year == now.year and data_quitacao.month > now.month):
                return self.valor_total / self.parcelas_totais
        elif self.tipo_pagamento == 1 and self.data_compra is not None:
            if (datetime.now().month == self.data_compra.month and datetime.now().year == self.data_compra.year):
                return self.valor_total
        else:
            return self.valor_total

    @property        
    def data_quitacao_prevista(self):
        if self.parcelas_totais and self.tipo_pagamento == 2:
            data_quitacao = self.data_compra + relativedelta(months=self.parcelas_totais)
            return data_quitacao

    @property
    def quitada(self):
        if self.parcelas_totais and self.tipo_pagamento == 2:
            parcela_ja_acabou = (self.data_compra.month + self.parcelas_totais - datetime.now().month) == 0
            return parcela_ja_acabou
        if self.tipo_pagamento == 1:
            return not(datetime.now().month == self.data_compra.month and datetime.now().year == self.data_compra.year)