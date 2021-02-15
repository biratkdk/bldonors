# Bldonors Upgrade Roadmap

## Current Baseline

- Stack: Django 3.2, SQLite, server-rendered templates
- App scope: donors, blood requests, stock, contact, basic authentication
- Current gaps:
  - no automated tests
  - no API layer
  - no background jobs or notifications
  - no reporting dashboard
  - no production deployment setup
  - security and maintainability issues in settings/views

## Target Direction

Turn the project into a small but more advanced product:

- REST API for donors, requests, stock, auth
- admin/reporting dashboard
- email notifications and scheduled reminders
- realtime stock/request updates
- payment integration for campaigns or sponsorships
- production-ready settings and deployment docs
- automated tests for models, views, auth, and API

## Delivery Phases

### Phase 1: Stabilize the Current App

- [in progress] Clean up obvious code issues
- [in progress] Add baseline automated tests
- [pending] Improve model metadata and admin usability
- [pending] Prepare settings for environment-based configuration

### Phase 2: Add a REST API

- [in progress] Add a simple JSON API using Django views
- [in progress] Create manual serializers for core models
- [in progress] Add API routes and basic session permissions
- [pending] Add API tests and endpoint guide

### Phase 3: Notifications

- [in progress] Add email backend configuration
- [in progress] Send notifications for blood requests and stock alerts
- [pending] Add scheduled reminders with a task queue

### Phase 4: Reports and Dashboard

- [in progress] Add aggregate reporting views
- [pending] Add charts for blood groups, demand, and stock
- [in progress] Add CSV export

### Phase 5: Realtime Features

- [pending] Add Django Channels
- [pending] Broadcast stock changes live
- [in progress] Add a lightweight realtime dashboard

### Phase 6: Payments

- [completed] Define payment use case
- [pending] Integrate payment gateway
- [in progress] Record transactions and receipts

### Phase 7: Deployment

- [in progress] Split dev and production settings
- [in progress] Add static file and secret management
- [in progress] Add deployment instructions
- [in progress] Add production checklist

## Immediate Work

This session starts with Phase 1:

1. add a real test suite
2. clean up low-risk code issues
3. keep behavior stable so later phases can build on it
