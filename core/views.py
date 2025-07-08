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
    return render(request, 'relatorios/relatorio_estatisticas.html', context)


@login_required
def relatorio_erros_view(request, data_inicio, data_fim):
    context = {
        'data_inicio': data_inicio,
        'data_fim': data_fim
    }
    return render(request, 'relatorios/relatorio_erros.html', context)


@login_required
def relatorio_usuario_view(request, data_inicio, data_fim):
    context = {
        'data_inicio': data_inicio,
        'data_fim': data_fim
    }
    return render(request, 'relatorios/relatorio_usuario.html', context)


# === View de Acesso ao FTP ===

@login_required
def lista_pdfs_ftp(request):
    DEFAULT_PATH = '/00-JSG-FTP (GERAL)/'

    current_path = request.GET.get('path', DEFAULT_PATH).strip()

    if request.GET.get('path') is None:
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

    def format_size(size_bytes):
        if size_bytes < 0:
            return "Desconhecido"
        elif size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        elif size_bytes < 1024 * 1024 * 1024:
            return f"{size_bytes / (1024 * 1024):.1f} MB"
        else:
            return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"

    try:
        with FTP() as ftp:
            ftp.connect(host, port=9921)
            ftp.login(usuario, senha)
            ftp.cwd(current_path)

            entries = []
            ftp.retrlines('LIST', lambda line: entries.append(line))

            for entry in entries:
                parts = entry.split()
                if not parts:
                    continue

                name = parts[-1]

                if name in ('.', '..'):
                    continue

                if entry.startswith('d'):
                    directories.append(name)
                else:
                    try:
                        size = int(parts[4])
                        date_parts = parts[5:8]
                        modified_str = ' '.join(date_parts)

                        from datetime import datetime
                        try:
                            dt = datetime.strptime(modified_str, "%b %d %H:%M")
                            year = datetime.now().year
                            dt = dt.replace(year=year)
                        except ValueError:
                            dt = datetime.strptime(f"{date_parts[0]} {date_parts[1]} {date_parts[2]}", "%b %d %Y")

                        mes_abreviado = dt.strftime("%b")
                        mes_extenso = MES_POR_EXTENSO.get(mes_abreviado, mes_abreviado)
                        modified = f"{dt.day}/{mes_extenso}/{dt.year}"

                        files.append({
                            'name': name,
                            'size': format_size(size),
                            'modified': modified,
                        })
                    except IndexError:
                        files.append({
                            'name': name,
                            'size': 'Desconhecido',
                            'modified': 'Desconhecida',
                        })

    except ftplib.error_perm as e:
        error = f"Erro de permissão ou caminho inválido: {str(e)}"
    except ftplib.all_errors as e:
        error = f"Erro na conexão FTP: {str(e)}"
    except Exception as e:
        error = f"Erro inesperado: {str(e)}"

    return render(request, 'ftp_lista.html', {
        'current_path': current_path,
        'directories': directories,
        'files': files,
        'error': error,
    })

@login_required
def visualizar_pdf_ftp(request, arquivo):
    host = "6f38071ad3d5.sn.mynetname.net"
    usuario = "sdr.lucas.marins"
    senha = "sdr.lucas.marins@ftp"

    buffer = io.BytesIO()
    try:
        with ftplib.FTP(host) as ftp:
            ftp.login(usuario, senha)
            ftp.retrbinary(f'RETR {arquivo}', buffer.write)
        pdf_content = buffer.getvalue()

        response = HttpResponse(pdf_content, content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="{arquivo}"'
        return response

    except Exception as e:
        return HttpResponse(f"Erro ao carregar o PDF: {e}", content_type='text/plain')


def logout_view(request):
    auth_logout(request)
    return redirect('login')