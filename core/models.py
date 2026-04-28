from django.db import models
from django.contrib.auth.models import User


class Disciplina(models.Model):
    """RF03 - Cadastro de disciplinas"""
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='disciplinas')
    nome = models.CharField(max_length=100)
    professor = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        ordering = ['nome']
        verbose_name = 'Disciplina'
        verbose_name_plural = 'Disciplinas'

    def __str__(self):
        return self.nome


class Atividade(models.Model):
    """RF04, RF10, RF11, RF12"""
    TIPO_CHOICES = [('prova', 'Prova'), ('trabalho', 'Trabalho')]
    PRIORIDADE_CHOICES = [('alta', 'Alta'), ('media', 'Média'), ('baixa', 'Baixa')]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='atividades')
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, related_name='atividades')
    titulo = models.CharField(max_length=200)
    data = models.DateField()
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    prioridade = models.CharField(max_length=10, choices=PRIORIDADE_CHOICES, default='media')
    concluida = models.BooleanField(default=False)
    criada_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['data', 'prioridade']
        verbose_name = 'Atividade'
        verbose_name_plural = 'Atividades'

    def __str__(self):
        return f"{self.titulo} - {self.disciplina.nome} ({self.get_tipo_display()})"

    @property
    def prioridade_cor(self):
        cores = {'alta': 'danger', 'media': 'warning', 'baixa': 'success'}
        return cores.get(self.prioridade, 'secondary')


class CronogramaEstudo(models.Model):
    """RF07 - Cronograma de estudos"""
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cronogramas')
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, related_name='cronogramas')
    data = models.DateField()
    tempo_planejado = models.PositiveIntegerField(help_text='Tempo em minutos')
    descricao = models.CharField(max_length=200, blank=True, null=True,
                                  help_text='Ex: Revisar capítulos 1 a 3')
    concluido = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['data']
        verbose_name = 'Cronograma de Estudo'
        verbose_name_plural = 'Cronogramas de Estudo'

    def __str__(self):
        return f"{self.disciplina.nome} — {self.data} ({self.tempo_planejado} min)"

    @property
    def tempo_formatado(self):
        h = self.tempo_planejado // 60
        m = self.tempo_planejado % 60
        if h and m:
            return f"{h}h {m}min"
        elif h:
            return f"{h}h"
        return f"{m}min"


class RegistroHoras(models.Model):
    """RF08 - Registro de horas estudadas"""
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='registros')
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, related_name='registros')
    data = models.DateField()
    tempo_estudado = models.PositiveIntegerField(help_text='Tempo em minutos')
    observacao = models.CharField(max_length=200, blank=True, null=True,
                                   help_text='Ex: Estudei exercícios de cálculo')
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-data']
        verbose_name = 'Registro de Horas'
        verbose_name_plural = 'Registros de Horas'

    def __str__(self):
        return f"{self.disciplina.nome} — {self.data} ({self.tempo_estudado} min)"

    @property
    def tempo_formatado(self):
        h = self.tempo_estudado // 60
        m = self.tempo_estudado % 60
        if h and m:
            return f"{h}h {m}min"
        elif h:
            return f"{h}h"
        return f"{m}min"
