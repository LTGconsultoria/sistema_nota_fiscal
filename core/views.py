from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
import ftplib
import io
from ftplib import FTP, error_perm
from django.contrib import messages

# === Views de Login e Dashboard ===

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Usuário ou senha incorretos'})

    return render(request, 'login.html')


@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')


# === Views de Relatórios ===

@login_required
def pre_relatorio_view(request):
    if request.method == 'POST':
        tipo_relatorio = request.POST.get('tipo_relatorio')
        data_inicio = request.POST.get('data_inicio')
        data_fim = request.POST.get('data_fim')

        if not tipo_relatorio or not data_inicio or not data_fim:
            return HttpResponseBadRequest("Todos os campos são obrigatórios.")

        return redirect(f'relatorio_{tipo_relatorio}', data_inicio=data_inicio, data_fim=data_fim)
    return render(request, 'pre_relatorio.html')


@login_required
def relatorio_geral_view(request, data_inicio, data_fim):
    context = {
        'data_inicio': data_inicio,
        'data_fim': data_fim
    }
    return render(request, 'relatorio_geral.html', context)


@login_required
def relatorio_pendentes_view(request, data_inicio, data_fim):
    context = {
        'data_inicio': data_inicio,
        'data_fim': data_fim
    }
    return render(request, 'relatorio_pendentes.html', context)


@login_required
def relatorio_empresa_view(request, data_inicio, data_fim):
    context = {
        'data_inicio': data_inicio,
        'data_fim': data_fim
    }
    return render(request, 'relatorio_empresa.html', context)


@login_required
def relatorio_estatisticas_view(request, data_inicio, data_fim):
    context = {
        'data_inicio': data_inicio,
        'data_fim': data_fim
    }
    return render(request, 'relatorio_estatisticas.html', context)


@login_required
def relatorio_erros_view(request, data_inicio, data_fim):
    context = {
        'data_inicio': data_inicio,
        'data_fim': data_fim
    }
    return render(request, 'relatorio_erros.html', context)


# === View de Acesso ao FTP ===

@login_required
def lista_pdfs_ftp(request):
    DEFAULT_PATH = '/00-JSG-FTP (GERAL)/'
    current_path = request.GET.get('path', DEFAULT_PATH).strip()

    # Garantir que o caminho não tenha '..' ou navegação acima da raiz
    if '..' in current_path or current_path.startswith('/..'):
        return HttpResponse("Acesso negado.", status=403)

    # Garantir que termine com barra
    if not current_path.endswith('/'):
        current_path += '/'

    # Redireciona para a URL com path padrão se não foi informado
    if request.GET.get('path') is None:
        from django.shortcuts import redirect
        return redirect(f"{request.path}?path={DEFAULT_PATH}")

    host = "6f38071ad3d5.sn.mynetname.net"
    usuario = "sdr.lucas.marins"
    senha = "sdr.lucas.marins@ftp"

    directories = []
    files = []
    error = None

    MES_POR_EXTENSO = {
        "Jan": "janeiro",
        "Feb": "fevereiro",
        "Mar": "março",
        "Apr": "abril",
        "May": "maio",
        "Jun": "junho",
        "Jul": "julho",
        "Aug": "agosto",
        "Sep": "setembro",
        "Oct": "outubro",
        "Nov": "novembro",
        "Dec": "dezembro"
    }

    try:
        with FTP() as ftp:
            ftp.connect(host, port=9921)
            ftp.login(usuario, senha)
            ftp.cwd(current_path)

            entries = []

            # Listando com mlsd e armazenando resultados
            for name, facts in ftp.mlsd():
                if name in ('.', '..'):
                    continue
                entries.append({
                    'name': name,
                    'type': facts['type'],
                    'modified': facts.get('modify', 'sem-data'),
                    'size': facts.get('size', '0')
                })

            # Imprime no console todo o conteúdo do diretório
            print("\n" + "=" * 60)
            print(f"Conteúdo do diretório: {current_path}")
            print("-" * 60)
            for item in entries:
                tipo = "📁 Pasta" if item['type'] == 'dir' else "📄 Arquivo"
                print(f"{tipo}: {item['name']} | Modificado: {item['modified']}")
            print("=" * 60 + "\n")

            # Preenchendo as listas de pastas e arquivos
            for item in entries:
                if item['type'] == 'dir':
                    directories.append(item['name'])
                elif item['type'] == 'file':
                    modified = item['modified']
                    try:
                        dt = datetime.strptime(modified, "%Y%m%d%H%M%S")
                        mes_abreviado = dt.strftime("%b").capitalize()
                        mes_extenso = MES_POR_EXTENSO.get(mes_abreviado, mes_abreviado)
                        modified = f"{dt.day} de {mes_extenso} de {dt.year}"
                    except Exception:
                        modified = "Desconhecida"

                    files.append({
                        'name': item['name'],
                        'modified': modified
                    })

    except Exception as e:
        error = f"Erro ao acessar o FTP: {str(e)}"

    return render(request, 'ftp_lista.html', {
        'current_path': current_path,
        'directories': directories,
        'files': files,
        'error': error,
    })
# views.py
import io
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from ftplib import FTP


@login_required
def abrir_arquivo_ftp(request, arquivo):
    host = "6f38071ad3d5.sn.mynetname.net"
    usuario = "sdr.lucas.marins"
    senha = "sdr.lucas.marins@ftp"

    buffer = io.BytesIO()

    try:
        with FTP() as ftp:
            ftp.connect(host, 9921)
            ftp.login(usuario, senha)
            ftp.retrbinary(f'RETR {arquivo}', buffer.write)

        conteudo = buffer.getvalue()
        nome_arquivo = arquivo.split('/')[-1]

        # Detectar se é PDF
        if nome_arquivo.lower().endswith('.pdf'):
            response = HttpResponse(conteudo, content_type='application/pdf')
            response['Content-Disposition'] = f'inline; filename="{nome_arquivo}"'
        else:
            response = HttpResponse(conteudo, content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{nome_arquivo}"'

        return response

    except Exception as e:
        return HttpResponse(f"Erro ao carregar o arquivo: {e}", content_type='text/plain')


# views.py
import ftplib
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse


@login_required
def upload_arquivo_ftp(request):
    current_path = request.GET.get('path', '/00-JSG-FTP (GERAL)/').strip()
    centro_custo = request.POST.get('centro_custo', '')
    descricao = request.POST.get('descricao', '')

    if request.method == 'POST' and request.FILES.get('arquivo'):
        upload_file = request.FILES['arquivo']

        host = "6f38071ad3d5.sn.mynetname.net"
        usuario = "sdr.lucas.marins"
        senha = "sdr.lucas.marins@ftp"

        try:
            with ftplib.FTP() as ftp:
                ftp.connect(host, 9921)
                ftp.login(usuario, senha)
                ftp.cwd(current_path)

                # Fazer upload do arquivo
                ftp.storbinary(f'STOR {upload_file.name}', upload_file.file)

            # Redireciona de volta para o mesmo diretório
            return HttpResponseRedirect(reverse('lista_pdfs_ftp') + f'?path={current_path}')

        except Exception as e:
            return HttpResponse(f"Erro ao fazer upload: {e}", content_type='text/plain')

    # Dados fictícios para mostrar no form
    centros_ficticios = [
        "CC001 - Administrativo",
        "CC002 - Produção",
        "CC003 - Comercial",
        "CC004 - TI",
        "CC005 - RH"
    ]

    return render(request, 'ftp_upload.html', {
        'current_path': current_path,
        'centros_ficticios': centros_ficticios,
        'centro_custo': centro_custo,
        'descricao': descricao,
    })



def logout_view(request):
    auth_logout(request)
    return redirect('login')