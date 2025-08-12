LogHub - Amateur Radio Online Logbook

Integrates with Log of the World (LOTW), Clublog, QRZ and HRDLog.

Uses the latest stable Django, HTMX, and Postgres.

Quickstart

Docker (web + Postgres + Tailwind)

- Copy `.env.example` to `.env` (optional; defaults are fine for dev).
- Build and start services (Python 3.12, Postgres 16, Node 22):

  docker compose up --build

- Open http://localhost:8000


Running tests with Docker (recommended for parity)

- One-off test run using the same image and Postgres as `web`:

  docker compose run --rm test

- Or via Makefile:

  make test

ADIF 3.1.5 Catalog

- The app recognizes all ADIF 3.1.5 fields via the official ADX schema `adx315.xsd` bundled in the repo.
- A normalized tag catalog is generated for UI suggestions and import normalization.
- Regenerate after updating the XSD:

  python scripts/gen_adif_catalog_from_xsd.py

- Output file: `assets/adif_3_1_5.json` (auto-loaded).
