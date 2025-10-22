# LearnCycle


LearnCycle is a Django-based web application for managing books, donations, orders, library features, and user accounts. It provides a marketplace and library-like features so users can browse books, manage carts and orders, donate books, and interact with a support/request system.

## Table of contents

- [Features](#features)
- [Tech stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Quick start (development)](#quick-start-development)
- [Database & migrations](#database--migrations)
- [Static files & media](#static-files--media)
- [Running tests](#running-tests)
- [Project layout](#project-layout)
- [Deployment notes](#deployment-notes)
- [Contributing](#contributing)
- [Code style and tips](#code-style-and-tips)
- [License](#license)
- [Contact](#contact)


## Features

- User accounts with profiles (app: `accounts`)
- Book catalog and management (app: `books`)
- Shopping cart and order processing (apps: `cart`, `orders`)
- Donations flow for book donors (app: `donations`)
- Library features (app: `library`)
- Pages and site content (app: `pages`)
- Request and support systems (apps: `requests`, `support`)
- Admin interface and basic signals (Django admin + `signals.py` in `library`)
- Static and media handling (see `static/` and `media/` folders)

This README documents the repository as it is checked into source control. Adjust any environment-specific instructions for your deployment environment.


## Tech stack

- Python (recommended 3.11+)
- Django (see `manage.py`)
- SQLite (default development DB included: `db.sqlite3`)
- Server-side rendered templates (Django templates in `templates/`)


## Prerequisites

- Git
- Python 3.11 or newer
- pip
- Virtual environment tool (venv, virtualenv)


## Quick start (development)

1. Clone the repository

   git clone https://github.com/asrafulmolla/LearnCycle.git
   cd LearnCycle

2. Create and activate a virtual environment

   python -m venv .venv
   source .venv/bin/activate

3. Install dependencies

   pip install -r requirements.txt

4. Create environment variables

   - The project does not include a committed `.env` file. Create one in the project root and add at minimum:

     SECRET_KEY=your-secret-key
     DEBUG=True
     ALLOWED_HOSTS=localhost,127.0.0.1

   - If you use a different database for development or deployment, set DATABASE_URL or update `learncycle/settings.py` accordingly.

5. Apply migrations and create a superuser

   python manage.py migrate
   python manage.py createsuperuser

6. (Optional) Collect static files

   python manage.py collectstatic --noinput

7. Run the development server

   python manage.py runserver

Open http://127.0.0.1:8000/ in your browser.


## Database & migrations

- The repository includes a development SQLite database `db.sqlite3`. For production, use PostgreSQL or another production-ready DB.
- To create or apply migrations:

  python manage.py makemigrations
  python manage.py migrate


## Static files & media

- Static assets are under `static/`. Templates use the `{% static %}` template tag.
- Uploaded media (covers, profile pics, ebooks, banners, etc.) are stored in `media/`. Configure `MEDIA_ROOT` and `MEDIA_URL` in `learncycle/settings.py` for production use.


## Running tests

Run the Django test suite with:

  python manage.py test

Add tests to the `tests.py` files inside each app or create a `tests/` package per app for better organization.


## Project layout (top-level)

- `learncycle/` — project settings, WSGI, ASGI, and URL configuration
- `accounts/` — user models, forms, views, and account management
- `books/` — book models, admin, views for listing and detail pages
- `cart/` — shopping cart models and views
- `donations/` — donation forms and models
- `library/` — library features and signals
- `orders/` — order models and order processing
- `pages/` — static pages and forms
- `requests/` — user requests handling
- `support/` — support app with consumers and routing (likely for websockets)
- `templates/` — Django templates used by the site
- `static/` — project static assets
- `media/` — uploaded media (book covers, ebooks, profile pics, banners, etc.)
- `db.sqlite3` — development database (committed here)
- `requirements.txt` — pinned Python dependencies


## Deployment notes

- Use a production-ready WSGI server (gunicorn/uWSGI) behind a reverse proxy (nginx).
- For static and media in production, serve from a CDN or object storage (S3, GCS) when possible.
- Set `DEBUG=False`, configure `ALLOWED_HOSTS`, and keep `SECRET_KEY` secret.
- Use HTTPS, enable HSTS, and configure secure cookie flags.
- Use environment variables or a secrets manager for credentials.


## Contributing

Contributions are welcome. Suggested workflow:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/name`
3. Make your changes and add tests
4. Run tests locally: `python manage.py test`
5. Open a pull request with a clear description

Please follow the existing project style and add tests for new functionality.


## Code style and tips

- Follow PEP8. Consider using `black` and `ruff`/`flake8` for formatting and linting.
- Prefer class-based views for reusable logic and keep view functions small.
- Use Django signals responsibly; prefer explicit function calls where clarity matters.


## License

No license file is included in the repository. If you want to open source the project, add a `LICENSE` file (for example MIT or Apache-2.0).


## Contact

- Repository: https://github.com/asrafulmolla/LearnCycle
- Owner: asrafulmolla

If you'd like, I can also:

- Add a `.env.example` with recommended environment variables
- Extract exact Python and Django versions from `requirements.txt` and pin them in a `pyproject.toml` or `constraints.txt`
- Add CI (GitHub Actions) for tests and linting

Feel free to tell me which of the above you'd like next.
# LearnCycle
