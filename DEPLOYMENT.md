# Deployment Guide

This project includes a simple deployment setup for Django.

## Files Added

- `bldonors/settings_dev.py`
- `bldonors/settings_prod.py`
- `.env.example`
- `requirements.txt`
- `runtime.txt`
- `Procfile`

## Local Development

1. Install Python 3.9 or 3.10
2. Create virtual environment
3. Install dependencies
4. Run migrations
5. Start development server

### Example Commands

```powershell
py -3.9 -m venv env
.\env\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Production Style Run

Use the production settings module:

```powershell
$env:DJANGO_SETTINGS_MODULE="bldonors.settings_prod"
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn bldonors.wsgi
```

## Environment Variables

Copy values from `.env.example` and set real production values for:

- `DJANGO_SECRET_KEY`
- `DJANGO_ALLOWED_HOSTS`
- `DJANGO_CSRF_TRUSTED_ORIGINS`
- email settings
- secure cookie and SSL settings

## Static Files

- source static files stay in `static/`
- collected production files go to `staticfiles/`

Run:

```powershell
python manage.py collectstatic --noinput
```

## Suggested Hosting Options

- Heroku-style deployment using `Procfile`
- PythonAnywhere
- small VPS with Gunicorn and Nginx

## Production Checklist

- set `DJANGO_SETTINGS_MODULE=bldonors.settings_prod`
- set a real secret key
- turn `DEBUG` off
- configure allowed hosts
- configure CSRF trusted origins
- configure email settings
- run migrations
- run collectstatic
- create superuser
- test login, API, reports, payment page, and notifications
