# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.views import APIView
from django.views.generic import View
from rest_framework.response import Response
from django.shortcuts import render, redirect
from rest_framework import status

# from django.http import HttpResponse
from django.conf import settings
import logging

logger = logging.getLogger('igastei')

class Index(View):
    """
    Class Based View para mostrar o index
    """
    def get(self, request):
        contexto = {'mensagem': ''}
        if not request.user.is_authenticated:
            return render(request, 'index.html', contexto)
        else:
            # return HttpResponse('Usuário já está autenticado!')
            # return render(request, 'veiculos.html', contexto)
            return render(request, 'index.html', contexto)
            # return redirect("/veiculo")

class CustomTokenObtainPairView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            token = AccessToken.for_user(user)
            print(refresh)
            print(token)
            return Response({
                'refresh': str(refresh),
                'token': str(token),
                'nome': user.username,
                'id': user.id
            })
            
        else:
            return Response({'error': 'Credenciais inválidas'}, status=status.HTTP_401_UNAUTHORIZED)