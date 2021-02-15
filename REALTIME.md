# Realtime Module

This module adds a lightweight realtime-style feature without WebSockets.

## Current Approach

- a login-protected JSON endpoint returns the latest report values
- the reports page uses jQuery AJAX polling every 10 seconds
- total donors, requests, stock entries, total units, and low stock list refresh automatically

## URLs

- `/reports/live-data`

## Why This Approach

- simple to understand
- easy to add to an existing Django project
- does not require Redis, Channels, or background servers

## Future Upgrade

- Django Channels
- true live stock updates with WebSockets
- dashboard alerts without page polling
