# -*- coding: utf-8 -*-
from gastos.models import Gasto
from gastos.serializers import SerializadorGasto, SerializadorCadastroGasto
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
        print(self.request.user)
        return Gasto.objects.filter(usuario=self.request.user)
        # return Gasto.objects.filter()

class APICriarGasto(CreateAPIView):
    queryset = Gasto.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = SerializadorCadastroGasto

    def create(self, request, *args, **kwargs):
        print('aaaa', self.request.user)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(usuario=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class APIExcluirGasto(DestroyAPIView):
    queryset = Gasto.objects.all()
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    serializer_class = SerializadorGasto

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class APIEditarGasto(UpdateAPIView):
    queryset = Gasto.objects.all()
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    serializer_class = SerializadorGasto

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)