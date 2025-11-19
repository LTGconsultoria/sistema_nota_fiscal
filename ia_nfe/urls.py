from django.urls import path
from .views import analisar_nota_view

urlpatterns = [
    path('analisar/', analisar_nota_view, name='analisar_nota'),
]
