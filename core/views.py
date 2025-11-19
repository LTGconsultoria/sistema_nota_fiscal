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


# === FTP - Lista e Upload ===#

@login_required
def lista_pdfs_ftp(request):
    DEFAULT_PATH = '/'  # <-- ajustado para iniciar na raiz
    current_path = request.GET.get('path', DEFAULT_PATH).strip()

    # Bloqueia tentativa de subir diretórios acima da raiz
    if '..' in current_path or current_path.startswith('/..'):
        return HttpResponse("Acesso negado.", status=403)

    # Garante que o caminho termine com barra
    if not current_path.endswith('/'):
        current_path += '/'

    # Se não veio path na URL, redireciona adicionando o path padrão
    if request.GET.get('path') is None:
        return redirect(f"{request.path}?path={DEFAULT_PATH}")

    host = "6f38071ad3d5.sn.mynetname.net"
    usuario = "sdr.lucas.marins"
    senha = "sdr.lucas.marins@ftp"

    directories = []
    files = []
    error = None
    parent_path = '/'
    try:
        if current_path not in ('/', ''):
            tmp = current_path[:-1] if current_path.endswith('/') else current_path
            idx = tmp.rfind('/')
            parent_path = tmp[:idx+1] if idx != -1 else '/'
    except Exception:
        parent_path = '/'

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

            # Lista com MLSD e armazena resultados
            for name, facts in ftp.mlsd():
                if name in ('.', '..'):
                    continue
                entries.append({
                    'name': name,
                    'type': facts['type'],
                    'modified': facts.get('modify', 'sem-data'),
                    'size': facts.get('size', '0')
                })

            # Log no console (opcional)
            print("\n" + "=" * 60)
            print(f"Conteúdo do diretório: {current_path}")
            print("-" * 60)
            for item in entries:
                tipo = "📁 Pasta" if item['type'] == 'dir' else "📄 Arquivo"
                print(f"{tipo}: {item['name']} | Modificado: {item['modified']}")
            print("=" * 60 + "\n")

            # Separa pastas e arquivos + formata data
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
        'parent_path': parent_path,
    })


@login_required
def upload_arquivo_ftp(request):
    current_path = request.GET.get('path', '/').strip()
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
def validar_chave_acesso(chave):
    """
    Verifica se a chave de acesso tem 44 dígitos e se o dígito verificador está correto.
    """
    if not chave.isdigit() or len(chave) != 44:
        return False

    corpo = chave[:43]
    dv_real = int(chave[-1])

    pesos = list(range(2, 10)) * 5  # 43 posições
    pesos = pesos[:43][::-1]

    soma = sum(int(digito) * peso for digito, peso in zip(corpo, pesos))
    resto = soma % 11
    dv_calculado = 11 - resto if resto >= 2 else 0

    return dv_calculado == dv_real


def extrair_dados_nota(texto):
    dados = {}

    # CNPJ
    cnpj_match = re.search(r'\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}', texto)
    if cnpj_match:
        dados['cnpj'] = cnpj_match.group()

    # Data de emissão
    data_match = re.search(r'\d{2}/\d{2}/\d{4}', texto)
    if data_match:
        dados['data_emissao'] = data_match.group()

    # Padrões de texto que indicam a presença da chave
    PADROES_CHAVE = [
        "chave de acesso",
        "chave de acesso da nota",
        "chave de acesso da nf-e",
        "chave de acesso da nota fiscal eletrônica",
        "acesso da nf-e",
        "número de acesso",
        "nf-e:",
        "consulta de autenticidade no portal",
    ]

    # Busca linha a linha para maior precisão
    linhas = texto.lower().splitlines()
    for linha in linhas:
        for padrao in PADROES_CHAVE:
            if padrao in linha:
                numeros = re.findall(r'\d', linha)
                chave = ''.join(numeros)
                if len(chave) == 44 and validar_chave_acesso(chave):
                    dados['chave_acesso'] = chave
                    break
        if 'chave_acesso' in dados:
            break

    # Fallback: busca geral se não achou com contexto
    if 'chave_acesso' not in dados:
        chave_match = re.search(r'(\d[\d\s]{40,})', texto)
        if chave_match:
            chave_limpa = re.sub(r'\D', '', chave_match.group())
            if len(chave_limpa) == 44:
                dados['chave_acesso'] = chave_limpa

    # Valor total (último valor no formato 0.000,00)
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


@login_required
def analisar_todos_ftp(request):
    diretorio = request.GET.get('path', '/').strip()
    if not diretorio.endswith('/'):
        diretorio += '/'
    host = "6f38071ad3d5.sn.mynetname.net"
    usuario = "sdr.lucas.marins"
    senha = "sdr.lucas.marins@ftp"
    saida = io.StringIO()
    try:
        with FTP() as ftp:
            ftp.connect(host, 9921)
            ftp.login(usuario, senha)
            ftp.cwd(diretorio)
            arquivos = []
            try:
                for name, facts in ftp.mlsd():
                    if facts.get('type') == 'file' and name.lower().endswith('.pdf'):
                        arquivos.append(name)
            except Exception:
                for name in ftp.nlst():
                    if name.lower().endswith('.pdf'):
                        arquivos.append(name)

            for nome in arquivos:
                buffer = io.BytesIO()
                ftp.retrbinary(f'RETR {nome}', buffer.write)
                buffer.seek(0)
                try:
                    imagens = convert_from_bytes(buffer.getvalue(), dpi=300)
                    texto = ''
                    for img in imagens[:2]:
                        img = ImageOps.autocontrast(img)
                        img = img.convert('L')
                        img = img.point(lambda x: 0 if x < 140 else 255, '1')
                        texto += pytesseract.image_to_string(img, lang='por', config='--psm 6')
                    status = "OK" if "Nota Fiscal" in texto else "Suspeito"
                    dados = extrair_dados_nota(texto)
                    linha = (
                        f"arquivo={nome} | status={status}"
                        f" | cnpj={dados.get('cnpj','')} | data={dados.get('data_emissao','')}"
                        f" | valor={dados.get('valor_total','')} | chave={dados.get('chave_acesso','')}\n"
                    )
                    saida.write(linha)
                except Exception as e:
                    saida.write(f"arquivo={nome} | erro={str(e)}\n")
    except Exception as e:
        return HttpResponse(f"Erro ao processar pasta: {e}", content_type='text/plain')

    conteudo = saida.getvalue()
    nome = diretorio.strip('/').replace('/', '_') or 'raiz'
    response = HttpResponse(conteudo, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename="analise_{nome}.txt"'
    return response

