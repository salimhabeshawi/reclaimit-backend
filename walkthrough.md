# ReclaimIt Backend Walkthrough

## Overview

ReclaimIt is a Django REST API for managing "Found" items on campus. It allows students to post items they found and other students to claim them by sending a contact request.

## Features

- **Authentication**: Token-based (using `telegram_username` and `password`).
- **Items**: Post found items (University, Location, Description).
- **Claims**: Send "Contact Requests" to claim an item.
- **Privacy**: Finder's telegram is not publicly listed. It is revealed to the claimant? No, the **Claimant's** telegram is revealed to the **Finder**. (As per implementation: Finder sees who requested).
- **Admin**: Full control via Django Admin.

## Endpoints

### Accounts

| Method | Endpoint         | Description                                                                                     |
| :----- | :--------------- | :---------------------------------------------------------------------------------------------- |
| `POST` | `/api/register/` | Register a new user. Required: `telegram_username`, `password`. Optional: `full_name`, `email`. |
| `POST` | `/api/login/`    | obtain auth tokens. Required: `telegram_username`, `password`.                                  |

### Items

| Method | Endpoint                   | Description                                                        |
| :----- | :------------------------- | :----------------------------------------------------------------- |
| `GET`  | `/api/items/`              | List all found items. Filter: `?university=AASTU`. (Requires Auth) |
| `POST` | `/api/items/`              | Post a found item.                                                 |
| `GET`  | `/api/items/{id}/`         | Retrieve item details.                                             |
| `POST` | `/api/items/{id}/resolve/` | Mark item as resolved (Owner only).                                |

### Requests

| Method | Endpoint                     | Description                                                                                                                                                               |
| :----- | :--------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `GET`  | `/api/requests/`             | List requests. **Finder** sees requests received (including **Claimant's** username). **Claimant** sees their sent requests (Finder's username is hidden until accepted). |
| `POST` | `/api/requests/`             | Create a request (Claim an item). Payload: `{"item": <id>}`.                                                                                                              |
| `POST` | `/api/requests/{id}/accept/` | Accept a request (Finder only). This reveals the Finder's telegram username to the Claimant.                                                                              |

## Usage Examples

### 1. Register

```bash
curl -X POST http://localhost:8000/api/register/ \
     -H "Content-Type: application/json" \
     -d '{"telegram_username": "@alex", "password": "securepass"}'
```

### 2. Login

```bash
curl -X POST http://localhost:8000/api/login/ \
     -H "Content-Type: application/json" \
     -d '{"telegram_username": "@alex", "password": "securepass"}'
```

_Response:_ `{"access": "eyJ...", "refresh": "eyJ..."}`

### 3. Post Found Item (as Finder)

```bash
curl -X POST http://localhost:8000/api/items/ \
     -H "Authorization: Bearer <access_token>" \
     -H "Content-Type: application/json" \
     -d '{
           "university": "AASTU",
           "title": "Black Wallet",
           "description": "Found in library",
           "location_text": "Library 2nd Floor",
           "date_of_event": "2023-11-01"
         }'
```

### 4. Claim Item (as Loser)

```bash
curl -X POST http://localhost:8000/api/requests/ \
     -H "Authorization: Bearer <access_token>" \
     -H "Content-Type: application/json" \
     -d '{"item": 1}'
```

### 5. Accept Request (as Finder)

```bash
curl -X POST http://localhost:8000/api/requests/1/accept/ \
     -H "Authorization: Bearer <finder_token>"
```

### 6. View Requests & See Finder Username (as Loser/Claimant)

```bash
curl -X GET http://localhost:8000/api/requests/ \
     -H "Authorization: Bearer <loser_token>"
```

_Response_: JSON list containing `to_user_data: { telegram_username: "@finder_user" }` (only if accepted).

### 7. Resolve Item (as Finder)

```bash
curl -X POST http://localhost:8000/api/items/1/resolve/ \
     -H "Authorization: Bearer <access_token>"
```

_Response_: `{"status": "item marked as resolved"}`

## Setup & Run

1. **Migrations**: `uv run python manage.py migrate`
2. **Run Server**: `uv run python manage.py runserver`
3. **Create Superuser**: `uv run python manage.py createsuperuser`
