This project is uses Django + HTMX designed for a solo developer working sporadically, but structured so open‑source contributors can easily join in. It includes Docker, Postgres, Tailwind (CLI), pytest, pre‑commit, GitHub Actions CI, and Renovate bot support for automated dependency updates.
The project is called LogHub.

Purpose:

Have a low‑churn, batteries‑included stack for building and maintaining a web app with minimal upkeep.
Keep the developer onboarding experience simple (one‑command dev environment).
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
Add tests for any new feature or fix.
Keep commits small and focused.
Use good first issue labels for beginner‑friendly tasks.

License: MIT