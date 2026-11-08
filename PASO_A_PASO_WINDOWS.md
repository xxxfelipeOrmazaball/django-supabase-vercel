# Guía práctica para estudiantes — Windows

**Meta:** ejecutar un proyecto Django existente, cambiar su base de datos local (SQLite) por PostgreSQL en Supabase y comprobar el resultado. **No necesitas instalar PostgreSQL ni psql.**

## 1. Abrir el proyecto

1. Descomprime el ZIP en una carpeta normal (por ejemplo Documentos).
2. Abre esa carpeta en Visual Studio Code, **la que contiene `manage.py`**.
3. Abre `Terminal → New Terminal` y selecciona PowerShell.
4. Comprueba Python: 

```powershell
py -3.12 --version
```

Si tienes otra versión compatible de Python 3 (3.10 o superior) y no 3.12, puedes usar `py -3` en los comandos de creación del entorno.

## 2. Instalar dependencias y ejecutar localmente

Copia estos comandos **uno a uno** en la terminal PowerShell, desde la carpeta del proyecto:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py runserver 8001
```

Si el archivo `.env` ya existe, **no lo sobreescribas** con `Copy-Item`. Abre http://127.0.0.1:8001/ y registra un estudiante **inventado**. Detén el servidor con `Ctrl+C` antes de cambiar la configuración.

> No hace falta activar el entorno virtual en PowerShell: usamos directamente el Python de `.venv`. Si el puerto 8001 está ocupado, usa 8002 tanto en el comando como en el navegador.

## 3. Cuenta y proyecto Supabase

1. Entra a https://supabase.com y crea una cuenta (correo electrónico o GitHub).
2. Crea una organización si aún no existe; elige Free cuando esté disponible.
3. Crea un proyecto y guarda la **contraseña de la base de datos PostgreSQL** en un lugar privado.
4. En el proyecto abre **Connect → Connection string → Session pooler**. Revisa que sea Session pooler, normalmente puerto 5432. No uses la cadena de Direct si tu red no soporta IPv6.

## 4. Conectar Django a Supabase

En VS Code abre el archivo `.env` que copiaste. Cambia las líneas de conexión usando los datos del Session pooler (ejemplo con valores ficticios):

```ini
DB_ENGINE="supabase"
DB_HOST="aws-0-REGION.pooler.supabase.com"
DB_PORT="5432"
DB_NAME="postgres"
DB_USER="postgres.ID_DEL_PROYECTO"
DB_PASSWORD="TU_CONTRASENA_REAL"
```

Las comillas dobles están permitidas. **No copies estos valores de ejemplo literalmente.** No incluyas `postgresql://` dentro de `DB_HOST`; coloca solo el host. `DB_PASSWORD` es la contraseña de la base de datos, no la clave de inicio de sesión de Supabase ni una API key. Guarda `.env`.

## 5. Verificar y crear las tablas de Supabase

Ejecuta en PowerShell:

```powershell
.\.venv\Scripts\python.exe manage.py shell -c "from django.db import connection; connection.ensure_connection(); print(connection.vendor, connection.settings_dict['NAME'])"
```

**Debe mostrar `postgresql postgres`.** Esto confirma el motor y una conexión real. Si dice `sqlite`, vuelve a revisar `.env` antes de continuar.

```powershell
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py runserver 8001
```

Abre http://127.0.0.1:8001/ y registra **otro** estudiante ficticio. Después, en Supabase: **Table Editor → public → estudiantes_estudiante**. El registro nuevo debe aparecer ahí.

## 6. Explicación de cierre

- SQLite y Supabase son **bases diferentes**: el primer estudiante local no aparece automáticamente en Supabase.
- No editamos `models.py` ni las vistas para cambiar de base; solo `.env`.
- Las migraciones crean las tablas correspondientes en cada base de datos.

## Errores rápidos

| Mensaje | Qué hacer |
|---|---|
| `py` no se reconoce | Probar `python --version` y crear el entorno con `python -m venv .venv` |
| `No module named django` | Reinstalar `requirements.txt` con el Python de `.venv` |
| `port is already in use` | Ejecutar `runserver 8002` y abrir ese puerto |
| `password authentication failed` | Revisar usuario y contraseña de PostgreSQL en `.env` |
| `could not translate host name` / timeout | Revisar host de Session pooler e internet |
| `relation ... does not exist` | Ejecutar `migrate` usando la conexión Supabase |

**Seguridad:** nunca enviar una captura de `.env` con la contraseña visible ni subirlo a GitHub. Solo usar registros ficticios.


## Continuación: publicar en Internet

Una vez funcionando con Supabase, sigue `PASO_A_PASO_VERCEL.md`. En Vercel se usa el **Transaction pooler** (normalmente puerto 6543), aunque en tu `.env` local puedes seguir usando Session pooler 5432.
