# Ramalhete Espiritual

Aplicacao Django para registro diario de praticas espirituais.

## Desenvolvimento local

```bash
python -m venv venv
.\venv\Scripts\pip install -r requirements.txt
.\venv\Scripts\python manage.py migrate
.\venv\Scripts\python manage.py runserver
```

Sem `DATABASE_URL`, o projeto usa SQLite localmente.

## Deploy na Vercel

A Vercel detecta o `manage.py`, o WSGI do Django e os arquivos estaticos
automaticamente. A producao usa PostgreSQL e requer estas variaveis:

```text
DJANGO_DEBUG=False
DJANGO_SECRET_KEY=<segredo aleatorio>
DJANGO_ALLOWED_HOSTS=.vercel.app
DATABASE_URL=<conexao PostgreSQL>
ADMIN_USERNAME=admin
ADMIN_PASSWORD=<senha inicial>
```

Depois de provisionar o banco e configurar as variaveis:

```bash
python manage.py migrate
python manage.py bootstrap_admin
```

As migracoes e o bootstrap do administrador devem ser executados com as
variaveis de producao carregadas no ambiente.
