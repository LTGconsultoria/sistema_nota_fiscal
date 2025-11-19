from django.db import models

class AnaliseNota(models.Model):
    nome_arquivo = models.CharField(max_length=255)
    tipo_documento = models.CharField(max_length=50, null=True, blank=True)
    dados_extraidos = models.TextField()
    status_previsto = models.CharField(max_length=50, null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome_arquivo
