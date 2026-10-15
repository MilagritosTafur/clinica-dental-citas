# AGENTS.md

Django 6.1 / Python 3.13 appointment app for a dental clinic. UI text, docstrings, and comments are in Spanish — keep that convention.

## Setup
- Install deps: `python -m pip install -r requirements.txt` (Django 6.1.2, psycopg2-binary, python-dotenv).
- `.env` (gitignored, not in the repo) must define `SECRET_KEY` — `settings.py` reads it with **no default**.
- Neon Postgres is provisioned by `neon deploy`, which writes `DATABASE_URL` (pooled), `DATABASE_URL_UNPOOLED` (direct) and `NEON_BRANCH` into **`.env.local`** (gitignored). `settings.py` loads `.env` then `.env.local` and builds `DATABASES` from `DATABASE_URL`.
- Database is **PostgreSQL** (`django.db.backends.postgresql`) even though the README says SQLite. Trust `clinica/settings.py`, not the README.

## Commands
- `python manage.py runserver`
- `python manage.py migrate` — run against the **direct** endpoint: `DATABASE_URL="$DATABASE_URL_UNPOOLED" python manage.py migrate` (pooled PgBouncer is fine for the app, not for migrations).
- `python manage.py test` — `citas/tests.py` is an empty stub; there is no test suite yet.

## Layout
- `manage.py` uses settings module `clinica.settings`.
- `clinica/` = project package (settings, root urls). `citas/` = the only app.
- `clinica/urls.py` mounts `citas.urls` at `/`; admin at `/admin/`.
- Models (`citas/models.py`): `Paciente` (primary key is `dni`, not `id`), `Odontologo`, `Consultorio`, `Tratamiento`, `Cita`, `CitaDetalle`.
- `Cita` prevents double-booking via two `UniqueConstraint`s on `(fecha, hora, odontologo)` and `(fecha, hora, consultorio)`, both with `condition=~Q(estado='cancelada')` (cancelling frees the slot).
- Validation lives in `citas/forms.py` (DNI must be 8 digits; no past dates) plus the DB constraints above.

## Gotchas
- `citas/templates/` **does not exist**, but views render `citas/cita_lista.html` and `citas/form.html`. List/create pages raise `TemplateDoesNotExist` until those templates are added.
- Django 6.x mail config is the `MAILERS` setting (console backend), not `EMAIL_BACKEND`.
- `citas/views copy.py` is an unused stray duplicate — ignore it.
- `package.json` / `neon.ts` are only Neon CLI config (`neon deploy`); there is no JS build or test — `npm run build` has no script. This is a Python/Django app.
- No CI, linter, formatter, or type-check config exists in the repo.
