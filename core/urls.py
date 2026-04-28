from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('', views.dashboard, name='dashboard'),
    path('cadastro/', views.cadastro, name='cadastro'),

    # Disciplinas
    path('disciplinas/', views.disciplina_lista, name='disciplina_lista'),
    path('disciplinas/nova/', views.disciplina_criar, name='disciplina_criar'),
    path('disciplinas/<int:pk>/editar/', views.disciplina_editar, name='disciplina_editar'),
    path('disciplinas/<int:pk>/excluir/', views.disciplina_excluir, name='disciplina_excluir'),

    # Atividades
    path('atividades/', views.atividade_lista, name='atividade_lista'),
    path('atividades/nova/', views.atividade_criar, name='atividade_criar'),
    path('atividades/<int:pk>/editar/', views.atividade_editar, name='atividade_editar'),
    path('atividades/<int:pk>/excluir/', views.atividade_excluir, name='atividade_excluir'),
    path('atividades/<int:pk>/concluir/', views.atividade_concluir, name='atividade_concluir'),

    # Calendário
    path('calendario/', views.calendario_mensal, name='calendario_mensal'),
    path('calendario/semanal/', views.calendario_semanal, name='calendario_semanal'),

    # Cronograma RF07
    path('cronograma/', views.cronograma_lista, name='cronograma_lista'),
    path('cronograma/novo/', views.cronograma_criar, name='cronograma_criar'),
    path('cronograma/<int:pk>/editar/', views.cronograma_editar, name='cronograma_editar'),
    path('cronograma/<int:pk>/excluir/', views.cronograma_excluir, name='cronograma_excluir'),
    path('cronograma/<int:pk>/concluir/', views.cronograma_concluir, name='cronograma_concluir'),

    # Registro de Horas RF08
    path('horas/', views.registro_lista, name='registro_lista'),
    path('horas/novo/', views.registro_criar, name='registro_criar'),
    path('horas/<int:pk>/editar/', views.registro_editar, name='registro_editar'),
    path('horas/<int:pk>/excluir/', views.registro_excluir, name='registro_excluir'),
]
