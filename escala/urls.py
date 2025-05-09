from django.urls import path
from .views import ColaboradorListView, escala_colaborador, escala_macro

urlpatterns = [
    path('colaboradores/', ColaboradorListView.as_view(), name='lista_colaboradores'),
    path('colaboradores/<uuid:colaborador_id>/escala/', escala_colaborador, name='escala_colaborador'),
    path('escala/', escala_macro, name='escala_macro'),
]
