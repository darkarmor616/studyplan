from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Disciplina, Atividade, CronogramaEstudo, RegistroHoras


class CadastroForm(UserCreationForm):
    email = forms.EmailField(required=True, label='E-mail')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {'username': 'Nome de usuário'}

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class DisciplinaForm(forms.ModelForm):
    class Meta:
        model = Disciplina
        fields = ['nome', 'professor']
        labels = {'nome': 'Nome da Disciplina', 'professor': 'Professor (opcional)'}
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'professor': forms.TextInput(attrs={'class': 'form-control'}),
        }


class AtividadeForm(forms.ModelForm):
    class Meta:
        model = Atividade
        fields = ['titulo', 'disciplina', 'data', 'tipo', 'prioridade']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'disciplina': forms.Select(attrs={'class': 'form-select'}),
            'data': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'prioridade': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, usuario, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['disciplina'].queryset = Disciplina.objects.filter(usuario=usuario)


class CronogramaForm(forms.ModelForm):
    """RF07 - Cronograma de estudos"""
    class Meta:
        model = CronogramaEstudo
        fields = ['disciplina', 'data', 'tempo_planejado', 'descricao']
        labels = {
            'disciplina': 'Disciplina',
            'data': 'Data',
            'tempo_planejado': 'Tempo planejado (minutos)',
            'descricao': 'O que estudar (opcional)',
        }
        widgets = {
            'disciplina': forms.Select(attrs={'class': 'form-select'}),
            'data': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'tempo_planejado': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'placeholder': 'Ex: 60'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Revisar capítulos 1 a 3'}),
        }

    def __init__(self, usuario, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['disciplina'].queryset = Disciplina.objects.filter(usuario=usuario)


class RegistroHorasForm(forms.ModelForm):
    """RF08 - Registro de horas estudadas"""
    class Meta:
        model = RegistroHoras
        fields = ['disciplina', 'data', 'tempo_estudado', 'observacao']
        labels = {
            'disciplina': 'Disciplina',
            'data': 'Data',
            'tempo_estudado': 'Tempo estudado (minutos)',
            'observacao': 'Observação (opcional)',
        }
        widgets = {
            'disciplina': forms.Select(attrs={'class': 'form-select'}),
            'data': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'tempo_estudado': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'placeholder': 'Ex: 90'}),
            'observacao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Fiz exercícios de cálculo'}),
        }

    def __init__(self, usuario, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['disciplina'].queryset = Disciplina.objects.filter(usuario=usuario)
