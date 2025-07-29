from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib import messages

import os
import io
import re
import ftplib
from ftplib import FTP, error_perm
from pdf2image import convert_from_bytes
from PIL import ImageOps
import pytesseract
from datetime import datetime

# Configuração global do Tesseract
os.environ['TESSDATA_PREFIX'] = '/usr/share/tesseract-ocr/5/tessdata'

# === Autenticação e Dashboard ===

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            auth_login(request, user)
            return redirect('dashboard')
        return render(request, 'login.html', {'error': 'Usuário ou senha incorretos'})
    return render(request, 'login.html')


def logout_view(request):
    auth_logout(request)
    return redirect('login')


@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')


# === Relatórios ===

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


def _render_relatorio(request, template, data_inicio, data_fim):
    return render(request, template, {'data_inicio': data_inicio, 'data_fim': data_fim})


@login_required
def relatorio_geral_view(request, data_inicio, data_fim):
    return _render_relatorio(request, 'relatorio_geral.html', data_inicio, data_fim)

@login_required
def relatorio_pendentes_view(request, data_inicio, data_fim):
    return _render_relatorio(request, 'relatorio_pendentes.html', data_inicio, data_fim)

@login_required
def relatorio_empresa_view(request, data_inicio, data_fim):
    return _render_relatorio(request, 'relatorio_empresa.html', data_inicio, data_fim)

@login_required
def relatorio_estatisticas_view(request, data_inicio, data_fim):
    return _render_relatorio(request, 'relatorio_estatisticas.html', data_inicio, data_fim)

@login_required
def relatorio_erros_view(request, data_inicio, data_fim):
    return _render_relatorio(request, 'relatorio_erros.html', data_inicio, data_fim)


# === FTP - Lista e Upload ===

@login_required
def lista_pdfs_ftp(request):
    DEFAULT_PATH = '/00-JSG-FTP (GERAL)/'
    current_path = request.GET.get('path', DEFAULT_PATH).strip()

    if '..' in current_path or current_path.startswith('/..'):
        return HttpResponse("Acesso negado.", status=403)

    if not current_path.endswith('/'):
        current_path += '/'

    if request.GET.get('path') is None:
        return redirect(f"{request.path}?path={DEFAULT_PATH}")

    host = "6f38071ad3d5.sn.mynetname.net"
    usuario = "sdr.lucas.marins"
    senha = "sdr.lucas.marins@ftp"

    directories, files, error = [], [], None
    MES_POR_EXTENSO = {
        "Jan": "janeiro", "Feb": "fevereiro", "Mar": "março", "Apr": "abril",
        "May": "maio", "Jun": "junho", "Jul": "julho", "Aug": "agosto",
        "Sep": "setembro", "Oct": "outubro", "Nov": "novembro", "Dec": "dezembro"
    }

    try:
        with FTP() as ftp:
            ftp.connect(host, port=9921)
            ftp.login(usuario, senha)
            ftp.cwd(current_path)

            entries = [entry for entry in ftp.mlsd() if entry[0] not in ('.', '..')]

            for name, facts in entries:
                tipo = facts['type']
                modified = facts.get('modify', 'sem-data')
                if tipo == 'dir':
                    directories.append(name)
                elif tipo == 'file':
                    try:
                        dt = datetime.strptime(modified, "%Y%m%d%H%M%S")
                        mes = MES_POR_EXTENSO.get(dt.strftime("%b").capitalize(), dt.strftime("%b"))
                        modified = f"{dt.day} de {mes} de {dt.year}"
                    except Exception:
                        modified = "Desconhecida"
                    files.append({'name': name, 'modified': modified})
    except Exception as e:
        error = f"Erro ao acessar o FTP: {str(e)}"

    return render(request, 'ftp_lista.html', {
        'current_path': current_path,
        'directories': directories,
        'files': files,
        'error': error,
    })


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
                ftp.storbinary(f'STOR {upload_file.name}', upload_file.file)
            return HttpResponseRedirect(reverse('lista_pdfs_ftp') + f'?path={current_path}')
        except Exception as e:
            return HttpResponse(f"Erro ao fazer upload: {e}", content_type='text/plain')

    centros_ficticios = [
        "CC001 - Administrativo", "CC002 - Produção", "CC003 - Comercial",
        "CC004 - TI", "CC005 - RH"
    ]

    return render(request, 'ftp_upload.html', {
        'current_path': current_path,
        'centros_ficticios': centros_ficticios,
        'centro_custo': centro_custo,
        'descricao': descricao,
    })


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
        content_type = 'application/pdf' if nome_arquivo.lower().endswith('.pdf') else 'application/octet-stream'
        disposition = 'inline' if nome_arquivo.lower().endswith('.pdf') else 'attachment'

        response = HttpResponse(conteudo, content_type=content_type)
        response['Content-Disposition'] = f'{disposition}; filename="{nome_arquivo}"'
        return response

    except Exception as e:
        return HttpResponse(f"Erro ao carregar o arquivo: {e}", content_type='text/plain')


# === OCR e IA ===

def extrair_dados_nota(texto):
    dados = {}

    cnpj_match = re.search(r'\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}', texto)
    if cnpj_match:
        dados['cnpj'] = cnpj_match.group()

    data_match = re.search(r'\d{2}/\d{2}/\d{4}', texto)
    if data_match:
        dados['data_emissao'] = data_match.group()

    chave_match = re.search(r'(\d[\d\s]{40,})', texto)
    if chave_match:
        chave_limpa = re.sub(r'\D', '', chave_match.group())
        if len(chave_limpa) == 44:
            dados['chave_acesso'] = chave_limpa

    valor_match = re.findall(r'\d{1,3}(?:\.\d{3})*,\d{2}', texto)
    if valor_match:
        dados['valor_total'] = valor_match[-1]

    return dados


@login_required
def analisar_pdf_ftp(request):
    caminho_arquivo = request.GET.get('arquivo')
    if not caminho_arquivo:
        return HttpResponse("Caminho do arquivo não informado.", status=400)

    host = "6f38071ad3d5.sn.mynetname.net"
    usuario = "sdr.lucas.marins"
    senha = "sdr.lucas.marins@ftp"
    buffer = io.BytesIO()

    try:
        with FTP() as ftp:
            ftp.connect(host, 9921)
            ftp.login(usuario, senha)
            ftp.retrbinary(f'RETR {caminho_arquivo}', buffer.write)

        buffer.seek(0)
        imagens = convert_from_bytes(buffer.getvalue(), dpi=300)

        texto_extraido = ''
        for img in imagens[:2]:
            img = ImageOps.autocontrast(img)
            img = img.convert('L')
            img = img.point(lambda x: 0 if x < 140 else 255, '1')
            texto_extraido += pytesseract.image_to_string(img, lang='por', config='--psm 6')

        status_previsto = "OK" if "Nota Fiscal" in texto_extraido else "Suspeito"
        dados_extraidos = extrair_dados_nota(texto_extraido)

        return render(request, 'ia_resultado.html', {
            'arquivo': caminho_arquivo,
            'status_previsto': status_previsto,
            'texto': texto_extraido[:3000],
            'dados': dados_extraidos
        })

    except Exception as e:
        return HttpResponse(f"Erro ao processar PDF com OCR: {e}", content_type='text/plain')
