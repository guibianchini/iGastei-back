# -*- coding: utf-8 -*-
from django.shortcuts import render
from gastos.models import Gasto
from gastos.serializers import SerializadorGasto
from rest_framework.generics import ListAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework import permissions

class APIListarVeiculos(ListAPIView):

    serializer_class = SerializadorGasto
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Gasto.objects.filter(usuario=self.request.user)