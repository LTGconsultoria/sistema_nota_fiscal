import io
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import AnaliseNota

import pdfplumber  # para leitura de PDF

@csrf_exempt
def analisar_nota_view(request):
    if request.method == 'POST' and request.FILES.get('arquivo'):
        arquivo = request.FILES['arquivo']
        nome_arquivo = arquivo.name

        try:
            with pdfplumber.open(arquivo) as pdf:
                texto = ''
                for page in pdf.pages:
                    texto += page.extract_text() + '\n'

            # Simula classificação com IA (você pode substituir por modelo real depois)
            status_previsto = 'OK' if 'Nota Fiscal' in texto else 'Erro'

            # Salva no banco de dados
            resultado = AnaliseNota.objects.create(
                nome_arquivo=nome_arquivo,
                dados_extraidos=texto[:500],  # salva só os primeiros caracteres
                status_previsto=status_previsto
            )

            return JsonResponse({
                'arquivo': nome_arquivo,
                'status_previsto': status_previsto,
                'id_resultado': resultado.id,
            })

        except Exception as e:
            return JsonResponse({'erro': str(e)}, status=500)

    return JsonResponse({'erro': 'Arquivo não enviado'}, status=400)
