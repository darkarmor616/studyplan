from django.contrib import admin
from .models import Disciplina, Atividade, CronogramaEstudo, RegistroHoras

@admin.register(Disciplina)
class DisciplinaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'professor', 'usuario']

@admin.register(Atividade)
class AtividadeAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'disciplina', 'data', 'tipo', 'prioridade', 'concluida']

@admin.register(CronogramaEstudo)
class CronogramaAdmin(admin.ModelAdmin):
    list_display = ['disciplina', 'data', 'tempo_planejado', 'concluido', 'usuario']

@admin.register(RegistroHoras)
class RegistroHorasAdmin(admin.ModelAdmin):
    list_display = ['disciplina', 'data', 'tempo_estudado', 'usuario']
