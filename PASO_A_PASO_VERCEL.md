# Publicar Django + Supabase en Vercel — Mac y Windows

**Objetivo:** publicar el mismo Django de clases en una URL pública, sin alterar modelos, vistas ni formularios. El proyecto debe funcionar en local con Supabase ANTES de publicarlo.

## 0. Conceptos importantes
- **GitHub** guarda el código, **Vercel** ejecuta Django y **Supabase** almacena los registros.
- Tu `.env` local **nunca** se sube a GitHub; las credenciales se ingresan en **Vercel > Project > Settings > Environment Variables**.
- En local normalmente usamos **Session pooler 5432**. En Vercel, **Transaction pooler 6543** (copia el host real desde el panel de Supabase).
- La web de prueba enumera nombres y correos. **Usa solamente registros inventados; la URL es pública y no hay autenticación en la página principal**.
- La conexión a Supabase es la misma base de datos, aunque cambie el puerto/método de conexión.

## 1. Revisar antes de subir
**Mac (terminal dentro de la carpeta de manage.py):**
```bash
.venv/bin/python manage.py check
.venv/bin/python manage.py makemigrations --check --dry-run
```
**Windows PowerShell:**
```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py makemigrations --check --dry-run
```
Si ya trabajaron la primera guía, no es necesario repetir instalaciones. La carpeta incluye `.gitignore` que protege `.env`, `.venv` y SQLite.

## 2. Subir a GitHub
Crea un repositorio privado o público en GitHub y sube **solo los archivos del proyecto**, sin `.env`.
Con Git instalado, puedes ejecutar desde la carpeta raíz:
```bash
git init
git add .
git status
git commit -m "Proyecto Django listo para Vercel"
git branch -M main
git remote add origin URL_REAL_DE_TU_REPOSITORIO
git push -u origin main
```
Reemplaza `URL_REAL_DE_TU_REPOSITORIO` por el enlace que entrega GitHub. Si el repositorio ya existe o usa otra rama, adapta los comandos.
**IMPORTANTE:** revisa `git status` ANTES de `git commit`: `.env` y `db.sqlite3` no deben aparecer.

## 3. Obtener datos del Transaction pooler
En Supabase: **Connect > Connection string > Transaction pooler**.
Copia **host, username, database y puerto**. El puerto suele ser `6543`, y el usuario suele ser `postgres.ID_DEL_PROYECTO`. No inventes el host a partir de la región.
Si ya creaste tablas mediante Session pooler local, **no necesitas crearlas de nuevo**: ambas conexiones acceden a la misma base.

## 4. Importar en Vercel
1. Entra a https://vercel.com/new e inicia sesión con GitHub.
2. Importa el repositorio y selecciona la carpeta que contiene `manage.py` como **Root Directory** (en este ZIP es la carpeta raíz del proyecto).
3. Deja que Vercel detecte **Django**. Normalmente NO hace falta un archivo `vercel.json` ni una carpeta `api/`.
4. ANTES del deploy, en **Environment Variables** añade:

| Nombre | Valor |
|---|---|
| `DB_ENGINE` | `supabase` |
| `DB_HOST` | El host exacto del **Transaction pooler** |
| `DB_PORT` | `6543` (confirma valor en Supabase) |
| `DB_NAME` | `postgres` (o el nombre mostrado por Supabase) |
| `DB_USER` | El usuario exacto que muestra Supabase |
| `DB_PASSWORD` | La contraseña **de PostgreSQL** |
| `DJANGO_SECRET_KEY` | Clave larga aleatoria, distinta de la clave local de ejemplo |
| `DJANGO_DEBUG` | `False` |

Aplica las variables a **Production** y, si vas a probar deployments de ramas, también a **Preview**. `VERCEL` la establece la plataforma automáticamente: NO la crees manualmente.

**Cómo generar una SECRET_KEY:**
- Mac: `.venv/bin/python -c "import secrets; print(secrets.token_urlsafe(48))"`
- Windows PowerShell: `.\.venv\Scripts\python.exe -c "import secrets; print(secrets.token_urlsafe(48))"`

Copia la clave en las variables de Vercel, no en GitHub.

## 5. Deploy y pruebas
1. Selecciona **Deploy**. Espera el resultado que indique Vercel.
2. Abre la URL `https://...vercel.app` asignada al proyecto.
3. Guarda un estudiante **ficticio**, recarga y confirma que se mantiene.
4. En Supabase > Table Editor > `estudiantes_estudiante`, confirma que apareció el registro.
5. Prueba otra vez desde otro navegador. Este proyecto muestra los registros a cualquiera con la URL; no uses datos reales.

## 6. ¿Y las migraciones?
**No ejecutar `migrate` en cada deploy.** Usa desde el computador del alumno el `.env` local ya conectado a Supabase por Session pooler (5432):
- Mac: `.venv/bin/python manage.py migrate`
- Windows: `.\.venv\Scripts\python.exe manage.py migrate`

Así las tablas se crean/actualizan en la misma base compartida. Para proyectos grandes, planifica migraciones con un proceso controlado.

## 7. Errores frecuentes
| Síntoma | Revisar |
|---|---|
| Error de conexión o timeout | `DB_HOST`, credenciales, puerto `6543`, región y disponibilidad en Supabase |
| `relation ... does not exist` | Migraciones locales ejecutadas contra la base Supabase correcta |
| `DisallowedHost` | Dominio autorizado en `ALLOWED_HOSTS` |
| Error CSRF al enviar formulario | `CSRF_TRUSTED_ORIGINS`, HTTPS y dominio real |
| CSS del admin no aparece | Logs de build, `collectstatic`, `STATIC_ROOT` |
| Error de prepared statements | `prepare_threshold=None` en `settings.py` y Transaction pooler |
| La página muestra `Internal Server Error` | Vercel > Deployment > Logs: no activar DEBUG público |
| Vercel intenta usar SQLite | Comprobar `DB_ENGINE=supabase` |

## 8. Nota pedagógica
**Desarrollo local != producción.** El código es el mismo, pero cambian la forma de arrancarlo, el dominio, la configuración y las credenciales. Vercel no ofrece almacenamiento persistente de archivos locales; si agregan imágenes subidas por usuarios, planificar Supabase Storage u otra solución.

**Fuentes oficiales:**
- https://vercel.com/changelog/zero-configuration-django-support
- https://vercel.com/docs/frameworks/backend/django
- https://supabase.com/docs/guides/database/connecting-to-postgres
- https://supabase.com/kb/troubleshooting/disabling-prepared-statements-qL8lEL
