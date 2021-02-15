# API Guide

This project has a simple JSON API built using normal Django views.

## Base Path

- `/api/`

## Endpoints

- `GET /api/summary/`
  - Returns total donors, blood requests, stock entries, total available units, and stock grouped by blood group.

- `GET /api/donors/`
  - Returns all donor records in JSON.

- `POST /api/donors/`
  - Creates a donor record from JSON.

- `GET /api/donors/<id>/`
  - Returns one donor record.

- `PUT /api/donors/<id>/`
  - Updates one donor record.
  - Login required.

- `DELETE /api/donors/<id>/`
  - Deletes one donor record.
  - Login required.

- `GET /api/blood-requests/`
  - Returns all blood request records.

- `POST /api/blood-requests/`
  - Creates a blood request.

- `GET /api/blood-requests/<id>/`
  - Returns one blood request.

- `PUT /api/blood-requests/<id>/`
  - Updates one blood request.
  - Login required.

- `DELETE /api/blood-requests/<id>/`
  - Deletes one blood request.
  - Login required.

- `GET /api/stocks/`
  - Returns all stock records.

- `POST /api/stocks/`
  - Creates a stock record.
  - Login required.

- `GET /api/stocks/<id>/`
  - Returns one stock record.

- `PUT /api/stocks/<id>/`
  - Updates one stock record.
  - Login required.

- `DELETE /api/stocks/<id>/`
  - Deletes one stock record.
  - Login required.

- `POST /api/login/`
  - Starts a session login using JSON username and password.

- `POST /api/logout/`
  - Logs out the current session.

- `GET /api/session/`
  - Returns whether the current user is logged in.

## Example JSON

### Create donor

```json
{
  "name": "Ram",
  "email": "ram@example.com",
  "phone": 9800000000,
  "address": "Kathmandu",
  "age": 23,
  "quantity": 1,
  "gender": "Male",
  "blood_group": "O Positive"
}
```

### Login

```json
{
  "username": "admin",
  "password": "yourpassword"
}
```

## Notes

- This API uses session-based authentication.
- It is kept simple for this project.
- It can later be upgraded to Django REST Framework if needed.
