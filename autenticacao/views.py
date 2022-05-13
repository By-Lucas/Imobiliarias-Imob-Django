from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib import auth

# Alertas de messagens
from django.contrib import messages
from django.contrib.messages import constants

def cadastro(request):
    if request.method == 'GET':
        # Se o ususario já estiver logado, será direcionado para pagina principal
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, 'cadastro.html')
    elif request.method == 'POST':
        #capiturar informacoes do form 'name' no html
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        #print(username, email, senha)

        # Se o tamanho do nome, email e senha for igual a 0, redireciona para a pagina
        # o strip() remove todos os espaços em brancos do form
        if len(username.strip()) == 0 or len(email.strip()) == 0 or len(senha.strip()) == 0:
            messages.add_message(request, constants.ERROR, 'Preencha todos os campos')
            return redirect('/auth/cadastro')

        # Verifica se está tentando cadastrar um usuario já existente
        user = User.objects.filter(username=username)
        print(user) # Exibe o nome no pint se ja tiver usuario cadastrado com mesmo username
        if user.exists():
            messages.add_message(request, constants.ERROR, 'Já existe um usuário com esse nome cadastrado')
            return redirect('/auth/cadastro')
            
        try:
            # Criar usuario (cadastrar)
            user = User.objects.create_user(username=username, 
                        email=email, 
                        password=senha)
            user.save()
            messages.add_message(request, constants.SUCCESS, 'Cadastro realizado com sucesso')
            return redirect('/auth/logar')
        except:
            messages.add_message(request, constants.ERROR, 'Erro interno do sistema')
            return redirect('/auth/cadastro')


def logar(request):
    if request.method == 'GET':
        # Se o ususario já estiver logado, será direcionado para pagina principal
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, 'logar.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        # existe um usuario e senha igual o que foi digitado?
        usuario = auth.authenticate(username=username, password=senha)
        if not usuario:
            messages.add_message(request, constants.ERROR, 'Usuário ou senha incorreto!')
            return redirect('/auth/logar')
        else:
            auth.login(request, usuario) #logar e ser redirecionado para a raiz do sistema
            return redirect('/')
        #return HttpResponse(f'{username} {senha}')
        

def sair(request):
    auth.logout(request)
    return redirect('/auth/logar')

