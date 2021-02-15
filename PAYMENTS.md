# Payments Module

This module adds a basic payment record system for the project.

## Features Added

- support payment form
- payment record storage in database
- purpose, method, and status tracking
- generated transaction id
- payment receipt email to payer
- recent payment list on the payment page
- payment totals included in reports and CSV export

## URLs

- `/payment`

## Current Payment Style

- manual payment record entry
- suitable for cash, bank transfer, eSewa, and Khalti entries
- no direct live payment gateway integration yet

## Future Improvements

- connect to eSewa API
- connect to Khalti API
- add payment verification callback
- add failed and refunded transaction handling
