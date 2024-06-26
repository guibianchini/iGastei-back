# -*- coding: utf-8 -*-
from rest_framework import serializers
from gastos.models import Gasto

class SerializadorGasto(serializers.ModelSerializer):
    """ 
    Serializador para o objeto Gasto
    """
    class Meta:
        model = Gasto
        exclude = []