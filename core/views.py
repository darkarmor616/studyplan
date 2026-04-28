from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from datetime import date, timedelta
import calendar

from .models import Disciplina, Atividade, CronogramaEstudo, RegistroHoras
from .forms import CadastroForm, DisciplinaForm, AtividadeForm, CronogramaForm, RegistroHorasForm


# ─── Auth ────────────────────────────────────────────────────────────────────

def cadastro(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Conta criada com sucesso! Bem-vindo ao StudyPlan.')
            return redirect('dashboard')
    else:
        form = CadastroForm()
    return render(request, 'core/cadastro.html', {'form': form})


# ─── Dashboard ───────────────────────────────────────────────────────────────

@login_required
def dashboard(request):
    hoje = date.today()
    em_7_dias = hoje + timedelta(days=7)

    atividades_pendentes = Atividade.objects.filter(
        usuario=request.user, concluida=False).order_by('data')[:5]

    lembretes_atrasados = Atividade.objects.filter(
        usuario=request.user, concluida=False, data__lt=hoje).order_by('data')

    lembretes_proximos = Atividade.objects.filter(
        usuario=request.user, concluida=False,
        data__gte=hoje, data__lte=em_7_dias).order_by('data')

    # Resumo de horas desta semana
    inicio_semana = hoje - timedelta(days=hoje.weekday())
    registros_semana = RegistroHoras.objects.filter(
        usuario=request.user, data__gte=inicio_semana, data__lte=hoje)
    total_minutos_semana = sum(r.tempo_estudado for r in registros_semana)

    total_disciplinas = Disciplina.objects.filter(usuario=request.user).count()
    total_pendentes = Atividade.objects.filter(usuario=request.user, concluida=False).count()
    total_concluidas = Atividade.objects.filter(usuario=request.user, concluida=True).count()

    # Cronogramas de hoje
    cronogramas_hoje = CronogramaEstudo.objects.filter(
        usuario=request.user, data=hoje, concluido=False)

    return render(request, 'core/dashboard.html', {
        'atividades_pendentes': atividades_pendentes,
        'lembretes_atrasados': lembretes_atrasados,
        'lembretes_proximos': lembretes_proximos,
        'total_disciplinas': total_disciplinas,
        'total_pendentes': total_pendentes,
        'total_concluidas': total_concluidas,
        'total_minutos_semana': total_minutos_semana,
        'cronogramas_hoje': cronogramas_hoje,
        'hoje': hoje,
    })


# ─── Disciplinas ─────────────────────────────────────────────────────────────

@login_required
def disciplina_lista(request):
    disciplinas = Disciplina.objects.filter(usuario=request.user)
    return render(request, 'core/disciplina_lista.html', {'disciplinas': disciplinas})

@login_required
def disciplina_criar(request):
    if request.method == 'POST':
        form = DisciplinaForm(request.POST)
        if form.is_valid():
            d = form.save(commit=False)
            d.usuario = request.user
            d.save()
            messages.success(request, f'Disciplina "{d.nome}" cadastrada!')
            return redirect('disciplina_lista')
    else:
        form = DisciplinaForm()
    return render(request, 'core/disciplina_form.html', {'form': form, 'titulo': 'Nova Disciplina'})

@login_required
def disciplina_editar(request, pk):
    disciplina = get_object_or_404(Disciplina, pk=pk, usuario=request.user)
    if request.method == 'POST':
        form = DisciplinaForm(request.POST, instance=disciplina)
        if form.is_valid():
            form.save()
            messages.success(request, 'Disciplina atualizada!')
            return redirect('disciplina_lista')
    else:
        form = DisciplinaForm(instance=disciplina)
    return render(request, 'core/disciplina_form.html', {'form': form, 'titulo': 'Editar Disciplina'})

@login_required
def disciplina_excluir(request, pk):
    disciplina = get_object_or_404(Disciplina, pk=pk, usuario=request.user)
    if request.method == 'POST':
        nome = disciplina.nome
        disciplina.delete()
        messages.success(request, f'Disciplina "{nome}" excluída.')
        return redirect('disciplina_lista')
    return render(request, 'core/confirmar_exclusao.html', {'objeto': disciplina, 'tipo': 'disciplina'})


# ─── Atividades ──────────────────────────────────────────────────────────────

@login_required
def atividade_lista(request):
    atividades = Atividade.objects.filter(usuario=request.user).order_by('concluida', 'data')
    return render(request, 'core/atividade_lista.html', {'atividades': atividades})

@login_required
def atividade_criar(request):
    if request.method == 'POST':
        form = AtividadeForm(request.user, request.POST)
        if form.is_valid():
            a = form.save(commit=False)
            a.usuario = request.user
            a.save()
            messages.success(request, f'Atividade "{a.titulo}" cadastrada!')
            return redirect('atividade_lista')
    else:
        form = AtividadeForm(request.user)
    return render(request, 'core/atividade_form.html', {'form': form, 'titulo': 'Nova Atividade'})

@login_required
def atividade_editar(request, pk):
    atividade = get_object_or_404(Atividade, pk=pk, usuario=request.user)
    if request.method == 'POST':
        form = AtividadeForm(request.user, request.POST, instance=atividade)
        if form.is_valid():
            form.save()
            messages.success(request, 'Atividade atualizada!')
            return redirect('atividade_lista')
    else:
        form = AtividadeForm(request.user, instance=atividade)
    return render(request, 'core/atividade_form.html', {'form': form, 'titulo': 'Editar Atividade'})

@login_required
def atividade_excluir(request, pk):
    atividade = get_object_or_404(Atividade, pk=pk, usuario=request.user)
    if request.method == 'POST':
        titulo = atividade.titulo
        atividade.delete()
        messages.success(request, f'Atividade "{titulo}" excluída.')
        return redirect('atividade_lista')
    return render(request, 'core/confirmar_exclusao.html', {'objeto': atividade, 'tipo': 'atividade'})

@login_required
def atividade_concluir(request, pk):
    atividade = get_object_or_404(Atividade, pk=pk, usuario=request.user)
    atividade.concluida = not atividade.concluida
    atividade.save()
    status = 'concluída' if atividade.concluida else 'reaberta'
    messages.success(request, f'Atividade "{atividade.titulo}" marcada como {status}.')
    return redirect('atividade_lista')


# ─── Calendário ──────────────────────────────────────────────────────────────

@login_required
def calendario_mensal(request):
    hoje = date.today()
    ano = int(request.GET.get('ano', hoje.year))
    mes = int(request.GET.get('mes', hoje.month))

    mes_anterior = {'ano': ano - 1, 'mes': 12} if mes == 1 else {'ano': ano, 'mes': mes - 1}
    mes_proximo = {'ano': ano + 1, 'mes': 1} if mes == 12 else {'ano': ano, 'mes': mes + 1}

    atividades = Atividade.objects.filter(usuario=request.user, data__year=ano, data__month=mes)
    atividades_por_dia = {}
    for a in atividades:
        atividades_por_dia.setdefault(a.data.day, []).append(a)

    cal = calendar.monthcalendar(ano, mes)
    semanas = []
    for semana in cal:
        dias = []
        for dia in semana:
            if dia == 0:
                dias.append({'dia': None, 'atividades': []})
            else:
                d = date(ano, mes, dia)
                dias.append({'dia': dia, 'data': d,
                             'atividades': atividades_por_dia.get(dia, []),
                             'hoje': d == hoje})
        semanas.append(dias)

    nomes_pt = {
        'January': 'Janeiro', 'February': 'Fevereiro', 'March': 'Março',
        'April': 'Abril', 'May': 'Maio', 'June': 'Junho',
        'July': 'Julho', 'August': 'Agosto', 'September': 'Setembro',
        'October': 'Outubro', 'November': 'Novembro', 'December': 'Dezembro',
    }

    return render(request, 'core/calendario_mensal.html', {
        'semanas': semanas,
        'mes_nome': nomes_pt.get(calendar.month_name[mes], ''),
        'ano': ano, 'mes': mes,
        'mes_anterior': mes_anterior, 'mes_proximo': mes_proximo, 'hoje': hoje,
    })

@login_required
def calendario_semanal(request):
    hoje = date.today()
    inicio_semana_str = request.GET.get('inicio')
    if inicio_semana_str:
        try:
            from datetime import datetime
            inicio_semana = datetime.strptime(inicio_semana_str, '%Y-%m-%d').date()
        except ValueError:
            inicio_semana = hoje - timedelta(days=hoje.weekday())
    else:
        inicio_semana = hoje - timedelta(days=hoje.weekday())

    fim_semana = inicio_semana + timedelta(days=6)
    semana_anterior = inicio_semana - timedelta(days=7)
    semana_proxima = inicio_semana + timedelta(days=7)

    atividades = Atividade.objects.filter(
        usuario=request.user, data__gte=inicio_semana, data__lte=fim_semana)
    atividades_por_dia = {}
    for a in atividades:
        atividades_por_dia.setdefault(a.data, []).append(a)

    dias_pt = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
    dias = []
    for i in range(7):
        d = inicio_semana + timedelta(days=i)
        dias.append({'data': d, 'nome': dias_pt[i],
                     'atividades': atividades_por_dia.get(d, []),
                     'hoje': d == hoje})

    return render(request, 'core/calendario_semanal.html', {
        'dias': dias, 'inicio_semana': inicio_semana, 'fim_semana': fim_semana,
        'semana_anterior': semana_anterior, 'semana_proxima': semana_proxima, 'hoje': hoje,
    })


# ─── Cronograma de Estudos (RF07) ────────────────────────────────────────────

@login_required
def cronograma_lista(request):
    cronogramas = CronogramaEstudo.objects.filter(usuario=request.user).order_by('concluido', 'data')
    return render(request, 'core/cronograma_lista.html', {'cronogramas': cronogramas})

@login_required
def cronograma_criar(request):
    if request.method == 'POST':
        form = CronogramaForm(request.user, request.POST)
        if form.is_valid():
            c = form.save(commit=False)
            c.usuario = request.user
            c.save()
            messages.success(request, 'Sessão de estudo adicionada ao cronograma!')
            return redirect('cronograma_lista')
    else:
        form = CronogramaForm(request.user)
    return render(request, 'core/cronograma_form.html', {'form': form, 'titulo': 'Nova Sessão de Estudo'})

@login_required
def cronograma_editar(request, pk):
    cronograma = get_object_or_404(CronogramaEstudo, pk=pk, usuario=request.user)
    if request.method == 'POST':
        form = CronogramaForm(request.user, request.POST, instance=cronograma)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cronograma atualizado!')
            return redirect('cronograma_lista')
    else:
        form = CronogramaForm(request.user, instance=cronograma)
    return render(request, 'core/cronograma_form.html', {'form': form, 'titulo': 'Editar Sessão'})

@login_required
def cronograma_excluir(request, pk):
    cronograma = get_object_or_404(CronogramaEstudo, pk=pk, usuario=request.user)
    if request.method == 'POST':
        cronograma.delete()
        messages.success(request, 'Sessão removida do cronograma.')
        return redirect('cronograma_lista')
    return render(request, 'core/confirmar_exclusao.html', {'objeto': cronograma, 'tipo': 'sessão de estudo'})

@login_required
def cronograma_concluir(request, pk):
    cronograma = get_object_or_404(CronogramaEstudo, pk=pk, usuario=request.user)
    cronograma.concluido = not cronograma.concluido
    cronograma.save()
    status = 'concluída' if cronograma.concluido else 'reaberta'
    messages.success(request, f'Sessão marcada como {status}.')
    return redirect('cronograma_lista')


# ─── Registro de Horas (RF08) ─────────────────────────────────────────────────

@login_required
def registro_lista(request):
    registros = RegistroHoras.objects.filter(usuario=request.user)

    # Totais por disciplina
    from django.db.models import Sum
    totais = RegistroHoras.objects.filter(usuario=request.user).values(
        'disciplina__nome').annotate(total=Sum('tempo_estudado')).order_by('-total')

    total_geral = sum(r.tempo_estudado for r in registros)

    return render(request, 'core/registro_lista.html', {
        'registros': registros,
        'totais': totais,
        'total_geral': total_geral,
    })

@login_required
def registro_criar(request):
    if request.method == 'POST':
        form = RegistroHorasForm(request.user, request.POST)
        if form.is_valid():
            r = form.save(commit=False)
            r.usuario = request.user
            r.save()
            messages.success(request, f'Registro de {r.tempo_formatado} adicionado!')
            return redirect('registro_lista')
    else:
        form = RegistroHorasForm(request.user)
    return render(request, 'core/registro_form.html', {'form': form, 'titulo': 'Registrar Horas Estudadas'})

@login_required
def registro_editar(request, pk):
    registro = get_object_or_404(RegistroHoras, pk=pk, usuario=request.user)
    if request.method == 'POST':
        form = RegistroHorasForm(request.user, request.POST, instance=registro)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registro atualizado!')
            return redirect('registro_lista')
    else:
        form = RegistroHorasForm(request.user, instance=registro)
    return render(request, 'core/registro_form.html', {'form': form, 'titulo': 'Editar Registro'})

@login_required
def registro_excluir(request, pk):
    registro = get_object_or_404(RegistroHoras, pk=pk, usuario=request.user)
    if request.method == 'POST':
        registro.delete()
        messages.success(request, 'Registro excluído.')
        return redirect('registro_lista')
    return render(request, 'core/confirmar_exclusao.html', {'objeto': registro, 'tipo': 'registro de horas'})
