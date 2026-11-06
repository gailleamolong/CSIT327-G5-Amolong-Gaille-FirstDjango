# CSIT327-Amolong-Gaille-FirstDjango

CampusConnect is a Django application for student registration, authentication, profiles, and a role-protected dashboard.

## Requirements

- Python 3.12 or newer
- Git

## Setup on Windows

From the project directory, create and activate a virtual environment in Command Prompt:

```cmd
py -m venv .venv
.venv\Scripts\activate.bat
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open `http://127.0.0.1:8000/`. Sign up at `/accounts/signup/`; sign in at `/accounts/login/`.

To create a Django superuser for `/admin/`:

```cmd
python manage.py createsuperuser
```

The app's admin panel is available to superusers and users with the Administrator role at `/admin-panel/`.

## Configuration and data

The local SQLite database, virtual environments, and `.env` files are ignored by Git. Database migrations are included; run `python manage.py migrate` to create a local database.

For deployments, set a unique `DJANGO_SECRET_KEY` environment variable and configure `DEBUG` and `ALLOWED_HOSTS` for the deployment environment. The fallback secret in settings is for local development only and must not be used in production.

Bootstrap 5 is loaded from jsDelivr, so styling requires an internet connection in the browser.