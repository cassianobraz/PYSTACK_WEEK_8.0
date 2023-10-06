from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib.auth import authenticate, login


def cadastro(request):
    if request.method == 'GET':
        return render(request, 'cadastro.html')
    elif request.method == 'POST':
        primeiro_nome = request.POST.get('primeiro_nome')
        ultimo_nome = request.POST.get('ultimo_nome')
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        email = request.POST.get('email')
        confirmar_senha = request.POST.get('confirmar_senha')

        if not senha == confirmar_senha:
            messages.add_message(request, constants.ERROR,
                                 'As senhas não são iguais')
            return redirect('/usuarios/cadastro')

        if len(senha) < 6:
            messages.add_message(request, constants.ERROR,
                                 'Sua senha deve ter 7 ou mais digitos')
            return redirect('/usuarios/cadastro')

        try:
            # TODO Validar se o username do usuário não existe
            user = User.objects.create_user(
                first_name=primeiro_nome,
                last_name=ultimo_nome,
                username=username,
                email=email,
                password=senha
            )
            messages.add_message(request, constants.SUCCESS,
                                 'Usuário salvo com sucesso')
        except:
            messages.add_message(request, constants.ERROR,
                                 'Erro interno do sistema, contate um administrador')
            return redirect('/usuarios/cadastro')

        return HttpResponse('Passou')


def logar(request):
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        user = authenticate(username=username, password=senha)

    if user:
        login(request, user)
        # Acontecerá um erro ao redirecionar por enquanto, resolveremos nos próximos passos
        return redirect('/')
    else:
        messages.add_message(request, constants.ERROR,
                             'Usuario ou senha inválidos')
        return redirect('/usuarios/login')
