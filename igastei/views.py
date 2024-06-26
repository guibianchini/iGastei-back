# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate
from django.views.generic import View
from django.shortcuts import render, redirect
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