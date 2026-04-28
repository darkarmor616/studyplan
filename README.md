# 📚 StudyPlan

Sistema de Planejamento de Estudos e Controle de Avaliações.

Desenvolvido como projeto da disciplina de **Engenharia de Software II** — IFSULDEMINAS Campus Muzambinho, Bacharelado em Ciência da Computação.

---

## 🚀 Versões

| Versão | Requisitos Implementados | Status |
|--------|--------------------------|--------|
| v1.0   | RF01, RF02, RF03, RF04, RF10, RF11, RF12 | ✅ Completo |
| v2.0   | RF05, RF06 (Lembretes + Calendário) | ✅ Completo |
| v3.0   | RF07, RF08 (Cronograma + Registro de Horas) | ✅ Completo |
| v4.0   | RF09 (Relatórios e Gráficos) | 🔜 Planejado |

---

## ✅ Requisitos implementados

- **RF01** — Cadastro de usuários
- **RF02** — Login de usuário
- **RF03** — Cadastro de disciplinas
- **RF04** — Cadastro de provas e atividades
- **RF05** — Lembretes de atividades (atrasadas e próximas 7 dias)
- **RF06** — Calendário mensal e semanal
- **RF07** — Cronograma de estudos (planejamento de sessões)
- **RF08** — Registro de horas estudadas com totais por disciplina
- **RF10** — Edição e exclusão de tarefas e provas
- **RF11** — Prioridade das atividades (Alta, Média, Baixa)
- **RF12** — Marcar atividades como concluídas

---

## 🛠️ Tecnologias

- Python 3.10+
- Django 4.2
- SQLite (desenvolvimento)
- Bootstrap 5.3
- Bootstrap Icons

---

## ⚙️ Como Executar

```bash
# 1. Clonar o repositório
git clone https://github.com/darkarmor616/studyplan.git
cd studyplan

# 2. Criar e ativar ambiente virtual
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # Linux/Mac

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Aplicar migrations
python manage.py migrate

# 5. Rodar o servidor
python manage.py runserver
```

Acesse: [http://localhost:8000](http://localhost:8000)

---

## 👤 Autor

**Gabriel Corrêa Simões**  
Bacharelado em Ciência da Computação — IFSULDEMINAS Campus Muzambinho
