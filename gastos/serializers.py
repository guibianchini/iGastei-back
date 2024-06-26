# -*- coding: utf-8 -*-
from rest_framework import serializers
from gastos.models import Gasto

class SerializadorGasto(serializers.ModelSerializer):
    """ 
    Serializador para o objeto Gasto
    """
    parcela_atual = serializers.ReadOnlyField()
    valor_parcela_atual = serializers.ReadOnlyField()
    data_quitacao_prevista = serializers.ReadOnlyField()
    quitada = serializers.ReadOnlyField()
    categoria_display = serializers.CharField(source='get_categoria_display')
    banco_display = serializers.CharField(source='get_banco_display')
    tipo_pagamento_display = serializers.CharField(source='get_tipo_pagamento_display')
    class Meta:
        model = Gasto
        fields = '__all__'
        exclude = []

class SerializadorGerenciaGasto(serializers.ModelSerializer):
    """ 
    Serializador para o objeto Gasto
    """
    class Meta:
        model = Gasto
        fields = '__all__'
        extra_kwargs = {
            'usuario': {'required': False}
        }