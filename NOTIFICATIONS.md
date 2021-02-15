# Notifications

This module adds simple email notifications to the project.

## Current Notification Features

- blood request submission sends an email to the system notification email
- blood request submission also sends an acknowledgement email to the requester
- stock create and stock update send a low-stock alert when quantity is at or below the threshold

## Settings

These values can be changed using environment variables:

- `DJANGO_EMAIL_BACKEND`
- `DJANGO_DEFAULT_FROM_EMAIL`
- `DJANGO_EMAIL_HOST`
- `DJANGO_EMAIL_PORT`
- `DJANGO_EMAIL_HOST_USER`
- `DJANGO_EMAIL_HOST_PASSWORD`
- `DJANGO_EMAIL_USE_TLS`
- `DJANGO_EMAIL_USE_SSL`
- `DJANGO_NOTIFICATION_EMAIL`
- `DJANGO_LOW_STOCK_ALERT_LEVEL`

## Default Behavior

- email backend defaults to Django console email backend
- notification email defaults to `admin@bldonors.com`
- low stock alert level defaults to `5`

## Future Upgrade

Later this can be improved with:

- SMS alerts
- scheduled donor reminder emails
- Celery or cron-based background tasks
