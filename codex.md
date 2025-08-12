This project uses Django + HTMX designed for a solo developer working sporadically, but structured so open‑source contributors can easily join in. It includes Docker, Postgres, Tailwind (CLI), pytest, pre‑commit, GitHub Actions CI, and Renovate bot support for automated dependency updates.
The project is called LogHub.

Purpose: To be a centralized amateur radio logging platform.

Features:
Each log entry (QSO) should follow the guidelines from the LOTW developer information pages.
LogHub will accept uploads from ADIF files and save the upload metadata (date, station callsign, location details, comment, original filename, etc) so that it knows where log entries came from in the future.
It will also keep track of imports from online services like LOTW, clublog, qrz, hrdlog, etc. For each service it will mirror the log entries locally so he knows if the main database is out of sync or not.
It will allow imported log entries (QSOs) to propagate to the online services if they support it.

Practices:

Follow best practices for security, code quality, and contribution friendliness.

Key Technologies:

Django LTS (Python web framework)
HTMX (frontend interactivity without a SPA)
Tailwind CSS (styling)
PostgreSQL (database)
Docker + docker‑compose (containerized dev/prod)
pytest, black, isort, flake8, bandit (testing and linting)

GitHub Actions (CI/CD)


Guidelines:

Follow the coding standards enforced by pre‑commit hooks.
Add tests for any new feature or fix. Tests should be run through docker.
Migrations should be run through docker as well.
Keep commits small and focused.
Use good first issue labels for beginner‑friendly tasks.

License: MIT
