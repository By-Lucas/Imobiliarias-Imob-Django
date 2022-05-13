from multiprocessing import context
from django.http.response import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from .models import Imovel, Cidade


@login_required(login_url='/auth/logar/')
def home(request):
    # REceber as informacoes do form (name='get do name')
    preco_minimo = request.GET.get('preco_minimo')
    preco_maximo = request.GET.get('preco_maximo')
    cidade = request.GET.get('cidade')
    tipo = request.GET.getlist('tipo') # PEgar uma lista de termos que o usuario selecionar
    #print(f'\nPMIN:{preco_minimo}| PMAX:{preco_maximo}| Cidade:{cidade}| Tipo:{tipo}\n')
    cidades = Cidade.objects.all()

    if preco_minimo or preco_maximo or cidade or tipo:
        if not preco_minimo :
            preco_minimo = 0 # Se usuaario nao selecionar nada o preco minimo vai ser 0
        if not preco_maximo :
            preco_maximo = 9999999999  # Se usuaario nao selecionar nada o preco maximo vai ser 99999999
        if not tipo :
            tipo = ['A', 'C'] # Se usuaario nao selecionar nada, i tipo vai ser A=Apartamento e C=Casa

        imoveis = Imovel.objects.filter(valor__gte=preco_minimo)\
            .filter(valor__lte=preco_maximo)\
            .filter(tipo_imovel__in=tipo).filter(cidade=cidade)
    else:
        imoveis = Imovel.objects.all()
        
    return render(request, 'home.html', {'imoveis':imoveis, 'cidades':cidades})

def imovel(request, id):
    imovel = get_object_or_404(Imovel, id=id)
    # Abaixo mostra 2 imoveis ( talvez voce se intereça por esses imoveis) Imvel da mesma cidade que esta vendo
    sugestoes = Imovel.objects.filter(cidade=imovel.cidade).exclude(id=id)[:2]
    print(sugestoes)
    return render(request, 'imovel.html', {'imovel': imovel, 'sugestoes': sugestoes, 'id': id})