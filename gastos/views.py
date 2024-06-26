# -*- coding: utf-8 -*-
from gastos.models import Gasto
from django.db.models import Sum
from gastos.serializers import SerializadorGasto, SerializadorGerenciaGasto, GastoBancoSerializer
from gastos.consts import OPCOES_BANCOS
from rest_framework.generics import ListAPIView, DestroyAPIView, CreateAPIView, UpdateAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

class APIListarGastos(ListAPIView):

    serializer_class = SerializadorGasto
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Gasto.objects.filter(usuario=self.request.user)
        quitada_param = self.request.query_params.get('quitada')

        if quitada_param is not None:
            quitada = quitada_param.lower() == 'true'  # Converte para booleano
            queryset = [gasto for gasto in queryset if gasto.quitada == quitada]

        return queryset
    
class APIListarPorBancos(ListAPIView):
    serializer_class = GastoBancoSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
            queryset = Gasto.objects.filter(usuario=self.request.user)

            # Filtrar e agrupar localmente apenas os gastos quitados
            gastos_quitados = [gasto for gasto in queryset if not(gasto.quitada)]

            # Agrupar os resultados quitados pelo campo banco e obter a soma de valor_total
            queryset_agrupado = {}
            for gasto in gastos_quitados:
                banco_nome = next((nome for id, nome in OPCOES_BANCOS if id == gasto.banco), 'Desconhecido')

                if gasto.banco not in queryset_agrupado:
                    queryset_agrupado[gasto.banco] = {
                        'banco': gasto.banco,
                        'banco_nome': banco_nome,
                        'total_valor': gasto.valor_parcela_atual if gasto.valor_parcela_atual else 0,
                    }
                else:
                    queryset_agrupado[gasto.banco]['total_valor'] +=  gasto.valor_parcela_atual if gasto.valor_parcela_atual else 0

            # Converter o dicionário em uma lista para manter o formato do queryset
            queryset_final = list(queryset_agrupado.values())

            return queryset_final

class APICriarGasto(CreateAPIView):
    queryset = Gasto.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = SerializadorGerenciaGasto

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(usuario=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class APIExcluirGasto(DestroyAPIView):
    queryset = Gasto.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = SerializadorGasto

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class APIEditarGasto(UpdateAPIView):
    queryset = Gasto.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = SerializadorGerenciaGasto

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)