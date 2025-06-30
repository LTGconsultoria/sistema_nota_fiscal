from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# View de Login
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Usuário ou senha incorretos.')

    return render(request, 'login.html')


# View protegida - Dashboard
@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')

# View protegida - Dashboard
@login_required
def pre_relatorio_view(request):
    if request.method == 'POST':
        tipo_relatorio = request.POST.get('tipo_relatorio')
        data_inicio = request.POST.get('data_inicio')
        data_fim = request.POST.get('data_fim')

        # Validação simples
        if not tipo_relatorio or not data_inicio or not data_fim:
            return HttpResponseBadRequest("Todos os campos são obrigatórios.")

        # Redireciona para o relatório escolhido com os parâmetros na URL
        return redirect(f'relatorio_{tipo_relatorio}', data_inicio=data_inicio, data_fim=data_fim)

    return render(request, 'pre_relatorio.html')

# core/views.py

def relatorio_geral_view(request, data_inicio, data_fim):
    context = {
        'data_inicio': data_inicio,
        'data_fim': data_fim
    }
    return render(request, 'relatorio_geral.html', context)

def relatorio_pendentes_view(request, data_inicio, data_fim):
    context = {
        'data_inicio': data_inicio,
        'data_fim': data_fim
    }
    return render(request, 'relatorio_pendentes.html', context)

def relatorio_empresa_view(request, data_inicio, data_fim):
    context = {
        'data_inicio': data_inicio,
        'data_fim': data_fim
    }
    return render(request, 'relatorio_empresa.html', context)

def relatorio_estatisticas_view(request, data_inicio, data_fim):
    context = {
        'data_inicio': data_inicio,
        'data_fim': data_fim
    }
    return render(request, 'relatorio_estatisticas.html', context)

def relatorio_erros_view(request, data_inicio, data_fim):
    context = {
        'data_inicio': data_inicio,
        'data_fim': data_fim
    }
    return render(request, 'relatorio_erros.html', context)

def relatorio_usuario_view(request, data_inicio, data_fim):
    context = {
        'data_inicio': data_inicio,
        'data_fim': data_fim
    }
    return render(request, 'relatorio_usuario.html', context)