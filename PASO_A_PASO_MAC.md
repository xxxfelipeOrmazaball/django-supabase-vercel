# Guía en Mac — preparar y probar antes de Vercel

## 1. Abrir la carpeta
Descomprime el ZIP y abre en VS Code **la carpeta donde está `manage.py`**. Terminal > New Terminal.

Comprueba Python:
```bash
python3 --version
```
Usa una versión compatible con Django 5.2 (por ejemplo Python 3.12 o 3.13).

## 2. Instalar sin cambiar el entorno global
```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
cp .env.example .env
.venv/bin/python manage.py migrate
.venv/bin/python manage.py runserver 8001
```
Si ya existe `.env`, NO lo reemplaces con `cp`. Abre http://127.0.0.1:8001/ y registra solo datos ficticios. Detén el servidor con `Control+C`.

## 3. Conectarse a Supabase (si ya lo tienen funcionando, omitir)
En Supabase > Connect copia los valores de **Session pooler** (puerto 5432) a `.env`:
```ini
DB_ENGINE=supabase
DB_HOST=HOST_REAL_DEL_SESSION_POOLER
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres.ID_REAL_DEL_PROYECTO
DB_PASSWORD=TU_PASSWORD_REAL
```
No uses la contraseña de tu cuenta Supabase ni una API key. Prueba:
```bash
.venv/bin/python manage.py shell -c "from django.db import connection; connection.ensure_connection(); print(connection.vendor, connection.settings_dict['NAME'])"
.venv/bin/python manage.py migrate
.venv/bin/python manage.py runserver 8001
```
Debe imprimir `postgresql postgres`. Confirma un registro ficticio en Supabase > Table Editor.

**Siguiente paso:** abre `PASO_A_PASO_VERCEL.md`.
