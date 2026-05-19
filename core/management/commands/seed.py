from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Disciplina, Atividade, CronogramaEstudo, RegistroHoras
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Popula o banco com dados de exemplo para demonstração'

    def handle(self, *args, **kwargs):
        user = User.objects.filter(username='admin').first()
        if not user:
            self.stdout.write('Usuário admin não encontrado.')
            return

        # Disciplinas
        d1, _ = Disciplina.objects.get_or_create(usuario=user, nome='Engenharia de Software II', professor='Prof. Paulo')
        d2, _ = Disciplina.objects.get_or_create(usuario=user, nome='Banco de Dados II', professor='Prof. João Marcelo')
        d3, _ = Disciplina.objects.get_or_create(usuario=user, nome='Projeto e Análise de Algoritmo', professor='Prof. Ricardo')

        hoje = date.today()

        # Atividades
        Atividade.objects.get_or_create(usuario=user, titulo='Apresentação do Projeto', disciplina=d1, defaults={'data': hoje + timedelta(days=2), 'tipo': 'trabalho', 'prioridade': 'alta'})
        Atividade.objects.get_or_create(usuario=user, titulo='Prova Final', disciplina=d2, defaults={'data': hoje + timedelta(days=7), 'tipo': 'prova', 'prioridade': 'alta'})
        Atividade.objects.get_or_create(usuario=user, titulo='Trabalho', disciplina=d3, defaults={'data': hoje + timedelta(days=14), 'tipo': 'trabalho', 'prioridade': 'media'})
        Atividade.objects.get_or_create(usuario=user, titulo='Lista de Exercícios', disciplina=d2, defaults={'data': hoje - timedelta(days=2), 'tipo': 'trabalho', 'prioridade': 'baixa', 'concluida': True})

        # Cronograma
        CronogramaEstudo.objects.get_or_create(usuario=user, disciplina=d1, data=hoje, defaults={'tempo_planejado': 60, 'descricao': 'Revisar documentação do projeto'})
        CronogramaEstudo.objects.get_or_create(usuario=user, disciplina=d2, data=hoje + timedelta(days=1), defaults={'tempo_planejado': 90, 'descricao': 'Estudar integrais'})
        CronogramaEstudo.objects.get_or_create(usuario=user, disciplina=d3, data=hoje + timedelta(days=2), defaults={'tempo_planejado': 120, 'descricao': 'Implementar algoritmo de Dijkstra'})

        # Registro de horas
        RegistroHoras.objects.get_or_create(usuario=user, disciplina=d1, data=hoje - timedelta(days=1), defaults={'tempo_estudado': 60, 'observacao': 'Estudei requisitos'})
        RegistroHoras.objects.get_or_create(usuario=user, disciplina=d2, data=hoje - timedelta(days=2), defaults={'tempo_estudado': 90, 'observacao': 'Exercícios de cálculo'})
        RegistroHoras.objects.get_or_create(usuario=user, disciplina=d3, data=hoje - timedelta(days=3), defaults={'tempo_estudado': 45, 'observacao': 'Revisão de grafos'})

        self.stdout.write(self.style.SUCCESS('Dados de exemplo criados com sucesso!'))
