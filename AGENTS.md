# Repository Guidelines

## Project Structure & Module Organization
- `loghub/`: Django project settings, URLs, ASGI/WSGI.
- `logbook/`: Main app (models, views, templates, imports, forms, templatetags).
- `logbook/templates/logbook/`: UI templates; e.g., `import_review.html`.
- `assets/` and `static/`: Tailwind input and compiled CSS/assets.
- `scripts/`: Utilities (e.g., ADIF catalog generation).
- `tests/`: Pytest suite.

## Docker-First Workflow (no local setup)
- Use Docker Compose for all tasks. Examples:
  - Start stack (web + Postgres): `make up` or `docker compose up --build`.
  - Background web only: `make web`.
  - Follow logs: `make logs`.
  - Open shell in web container: `make shell`.
  - Run tests in isolated container: `make test`.
- Common one-liners (run from host):
  - Migrations: `docker compose run --rm web python manage.py migrate`
  - Make migrations: `docker compose run --rm web python manage.py makemigrations logbook`
  - Django admin user: `docker compose run --rm web python manage.py createsuperuser`
- CSS is built/watched inside `web` automatically (no host Node required).

## Coding Style & Naming Conventions
- Python 3.12, Django 5.x, 4-space indentation.
- snake_case for functions/vars, PascalCase for classes, UPPER_CASE for constants.
- Use type hints where practical; validate models via `clean()` and `save()`.
- Templates under `logbook/templates/logbook/`; keep HTMX usage minimal and declarative.

## Testing Guidelines
- Framework: `pytest` + `pytest-django` (settings: `loghub.settings`).
- Tests live in `tests/` as `test_*.py`; prefer arrange–act–assert.
- Run via Docker: `make test` (recommended) or `docker compose run --rm test`.

## Commit & Pull Request Guidelines
- Commits: concise subject (≤72 chars), present tense; include scope prefix when helpful (e.g., `imports:`).
- PRs: clear description, rationale, and screenshots for UI changes; link issues.
- Note schema changes, migrations, and test coverage adjustments.

## Security & Configuration
- Configure via `.env` (see `.env.example`). Key vars: `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `DJANGO_ALLOWED_HOSTS`, `POSTGRES_*`.
- Secrets never committed; repository volumes mount the working tree into containers.
