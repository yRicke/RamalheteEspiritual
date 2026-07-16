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
```

Depois de provisionar o banco e configurar as variaveis, execute as migracoes:

```bash
python manage.py migrate
```

Para criar ou atualizar o administrador, defina as credenciais apenas no
processo que executara o bootstrap:

```powershell
$env:ADMIN_USERNAME="admin"
$env:ADMIN_PASSWORD="<senha inicial>"
python manage.py bootstrap_admin
```

Nao mantenha `ADMIN_USERNAME` e `ADMIN_PASSWORD` nas variaveis do deployment
depois do bootstrap. O aplicativo usa o usuario salvo no banco de dados.
