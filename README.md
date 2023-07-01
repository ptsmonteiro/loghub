LogHub (Django + HTMX)

Basic QSO CRUD scaffolding using latest stable Django, HTMX, and Postgres-ready settings.

Quickstart

- Python: 3.11+
- Optional: Postgres via env vars; defaults to SQLite for dev.

Steps

1) Create venv and install deps

   python3 -m venv .venv
   . .venv/bin/activate
   pip install -r requirements.txt

2) Configure environment (optional for Postgres)

   Create a .env file to point to Postgres if desired:

   POSTGRES_DB=loghub
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432

3) Migrate and run

   python manage.py migrate
   python manage.py createsuperuser  # optional
   python manage.py runserver

Then open http://127.0.0.1:8000/ to access QSOs and /admin/ for the admin site.

Notes

- HTMX is included via CDN and hx-boost for snappier navigation.
- The QSO model includes common ADIF/LoTW-aligned fields (CALL, DATE/TIME, BAND, MODE, RST, FREQ, COUNTRY, GRID, COMMENT).
- Tests: a minimal pytest check exists in tests/test_qso_model.py.

Docker (web + Postgres + Tailwind)

- Copy `.env.example` to `.env` (optional; defaults are fine for dev).
- Build and start services (Python 3.12, Postgres 16, Node 22):

  docker compose up --build

- Open http://localhost:8000
- Tailwind CSS is built by the `tailwind` service (installs dev deps via `npm ci`), outputting to `static/css/tailwind.css`.

Tailwind CLI (local)

If you prefer to run Tailwind locally without Docker:

  npm install
  npm run tailwind:watch

CI

GitHub Actions workflow `.github/workflows/ci.yml` runs on Python 3.12: Django checks, migrations (SQLite), and pytest on pushes and PRs.

Running tests with Docker (recommended for parity)

- One-off test run using the same image and Postgres as `web`:

  docker compose run --rm test

- Or via Makefile:

  make test

This keeps local runs consistent with the containerized dev stack. CI still runs tests without Docker for speed, but can be switched later if you prefer full container parity in CI as well.
