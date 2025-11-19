from django.urls import path
from . import views
from django.contrib.auth import views as auth_views  # Importando as views padrão do Django

urlpatterns = [
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('pre_relatorio/', views.pre_relatorio_view, name='pre_relatorio'),
    path('ftp/', views.lista_pdfs_ftp, name='lista_pdfs_ftp'),
    path('ftp/arquivo/<path:arquivo>/', views.abrir_arquivo_ftp, name='abrir_arquivo_ftp'),
    path('ftp/upload/', views.upload_arquivo_ftp, name='upload_arquivo_ftp'),
    # Adicione esta linha para a rota de logout:
    path('logout/', views.login_view, name='logout'),
    path('relatorios/geral/<str:data_inicio>/<str:data_fim>/', views.relatorio_geral_view, name='relatorio_geral'),
    path('relatorios/pendentes/<str:data_inicio>/<str:data_fim>/', views.relatorio_pendentes_view, name='relatorio_pendentes'),
    path('relatorios/por_empresa/<str:data_inicio>/<str:data_fim>/', views.relatorio_empresa_view, name='relatorio_empresa'),
    path('relatorios/estatisticas/<str:data_inicio>/<str:data_fim>/', views.relatorio_estatisticas_view, name='relatorio_estatisticas'),
    path('relatorios/erros/<str:data_inicio>/<str:data_fim>/', views.relatorio_erros_view, name='relatorio_erros'),
    path('ftp/analisar_ia/', views.analisar_pdf_ftp, name='analisar_pdf_ftp'),
    path('ftp/analisar_todos/', views.analisar_todos_ftp, name='analisar_todos_ftp'),



]