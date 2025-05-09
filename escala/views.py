from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404, redirect
from .models import Colaborador, Plantao
from datetime import datetime, timedelta

class ColaboradorListView(ListView):
    model = Colaborador
    template_name = 'escala/colaboradores.html'
    context_object_name = 'colaboradores'
    paginate_by = 20  # opcional, para paginação

MESES = {
    1: "Janeiro",
    2: "Fevereiro",
    3: "Março",
    4: "Abril",
    5: "Maio",
    6: "Junho",
    7: "Julho",
    8: "Agosto",
    9: "Setembro",
    10: "Outubro",
    11: "Novembro",
    12: "Dezembro"
}

TURNOS = ["M", "T", "N", "AB", "FE", "F"]


def escala_colaborador(request, colaborador_id):
    colaborador = get_object_or_404(Colaborador, id=colaborador_id)

    # Pega o mês selecionado ou usa o mês atual como padrão
    mes_selecionado = int(request.GET.get("mes", datetime.now().month))
    ano_selecionado = datetime.now().year

    # Calcula o número de dias no mês selecionado
    primeiro_dia = datetime(year=ano_selecionado, month=mes_selecionado, day=1)
    proximo_mes = (primeiro_dia.replace(day=28) + timedelta(days=4)).replace(day=1)
    dias_no_mes = (proximo_mes - timedelta(days=1)).day

    # Cria a escala com "F" para folgas
    escala = []
    for dia in range(1, dias_no_mes + 1):
        data = primeiro_dia.replace(day=dia).date()
        plantao = Plantao.objects.filter(colaborador=colaborador, data=data).first()
        turno = plantao.turno.upper() if plantao else "F"
        escala.append({"dia": dia, "turno": turno})

    context = {
        "colaborador": colaborador,
        "escala": escala,
        "mes": MESES[mes_selecionado],
        "meses": MESES.items(),
        "mes_selecionado": mes_selecionado,
        "turnos": TURNOS,
        "title": f"Escala de {colaborador.nome}"
    }
    return render(request, "escala/escala_colaborador.html", context)


def escala_macro(request):
    # Pega o mês selecionado ou usa o mês atual como padrão
    mes_selecionado = int(request.GET.get("mes", datetime.now().month))
    ano_selecionado = datetime.now().year

    # Calcula o número de dias no mês selecionado
    primeiro_dia = datetime(year=ano_selecionado, month=mes_selecionado, day=1)
    proximo_mes = (primeiro_dia.replace(day=28) + timedelta(days=4)).replace(day=1)
    dias_no_mes = (proximo_mes - timedelta(days=1)).day

    # Cria a tabela de escala para todos os colaboradores
    colaboradores = Colaborador.objects.all().order_by("setor__nome", "nome")
    tabela_escala = []

    for colaborador in colaboradores:
        linha = {"colaborador": colaborador.nome, "setor": colaborador.setor, "categoria": colaborador.categoria, "dias": []}
        for dia in range(1, dias_no_mes + 1):
            data = primeiro_dia.replace(day=dia).date()
            plantao = Plantao.objects.filter(colaborador=colaborador, data=data).first()
            turno = plantao.turno if plantao else "F"
            linha["dias"].append(turno)
        tabela_escala.append(linha)

    # Gera a lista de dias para o cabeçalho
    dias = list(range(1, dias_no_mes + 1))

    context = {
        "tabela_escala": tabela_escala,
        "mes": MESES[mes_selecionado],
        "meses": MESES.items(),
        "mes_selecionado": mes_selecionado,
        "dias": dias,
        "title": "Escala Macro"
    }
    return render(request, "escala/escala_macro.html", context)
