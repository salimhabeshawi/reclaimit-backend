# ReclaimIt - Campus Lost & Found Backend

ReclaimIt is a robust Django REST API designed to help university students reconnect with their lost belongings. It simplifies the "Lost & Found" process by allowing students to post found items and enabling potential owners to send claim requests securely.

## 🚀 Features

-   **Found Item Listings**: Students can post details about items they have found on campus (including location and date).
-   **Claim System**: Users who lost an item can send a "Contact Request" to the finder.
-   **Privacy-First**: Telegram usernames are securely exchanged only when a claim is made. The finder decides who to contact.
-   **Item Resolution**: Once an item is returned, the finder can mark it as resolved (which automatically removes it from the active list).
-   **Authentication**: Token-based authentication using Telegram Usernames.

## 🛠️ Tech Stack

-   **Framework**: Django & Django REST Framework (DRF)
-   **Database**: SQLite (Development)
-   **Authentication**: DRF Token Authentication
-   **Package Manager**: `uv` (Faster Python package management)

## 📦 Installation & Setup

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/salimhabeshawi/reclaimit-backend.git
    cd reclaimit-backend
    ```

2.  **Install Dependencies**
    Using `uv`:
    ```bash
    uv sync
    ```
    *(Or using pip: `pip install -r requirements.txt`)*

3.  **Run Migrations**
    ```bash
    uv run python manage.py migrate
    ```

4.  **Create Superuser**
    ```bash
    uv run python manage.py createsuperuser
    ```

5.  **Run Development Server**
    ```bash
    uv run python manage.py runserver
    ```
    The API will be available at `http://127.0.0.1:8000/`.

## 🔌 API Documentation

### Authentication
-   **Register**: `POST /api/register/`
    -   Body: `{"telegram_username": "@user", "password": "..."}`
-   **Login**: `POST /api/login/`
    -   Body: `{"username": "@user", "password": "..."}`
    -   Returns: `{"token": "..."}`

### Items
-   **List Items**: `GET /api/items/`
-   **Post Item**: `POST /api/items/` (Requires Auth)
    -   Body: `{"title": "...", "university": "AASTU", "location_text": "...", "description": "..."}`
-   **Resolve Item**: `POST /api/items/{id}/resolve/` (Requires Auth, Finder Only)

### Requests (Claims)
-   **Send Claim**: `POST /api/requests/`
    -   Body: `{"item": <item_id>}`
-   **View Claims**: `GET /api/requests/`
    -   **Finder**: Sees incoming requests + Claimant's Username.
    -   **Claimant**: Sees sent requests history.

## 🧪 Testing

You can test the API using **Postman** or **cURL**.
A browsable API interface is also enabled for the Login endpoint (`/api-auth/login/`).

---
Built with ❤️ for Students.
