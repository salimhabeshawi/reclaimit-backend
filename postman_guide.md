# Beginner's Guide to Testing ReclaimIt with Postman

This guide assumes you have installed Postman and opened it.

## Base URL
We will be using this URL for everything: `http://127.0.0.1:8000/api`

---

## Step 1: Create a User (Registration)

1.  **Open a new tab**: Click the **+** button at the top of the Postman window.
2.  **Set Method**: Click the dropdown that says **GET** and select **POST**.
3.  **Enter URL**: In the bar next to POST, type:
    `http://127.0.0.1:8000/api/register/`
4.  **Set Body**:
    *   Click the **Body** tab (below the URL bar).
    *   Select the **raw** radio button.
    *   Click the dropdown that says **Text** (at the right end of the options) and select **JSON**.
    *   Paste this into the large text area below:
        ```json
        {
            "telegram_username": "@my_test_user",
            "password": "password123",
            "full_name": "Test Student"
        }
        ```
5.  **Send**: Click the big blue **Send** button.
    *   *Success?* You should see status **201 Created** at the bottom.

---

## Step 2: Log In (Get your Access Token)

1.  **Open a new tab** (+).
2.  **Set Method**: Select **POST**.
3.  **Enter URL**:
    `http://127.0.0.1:8000/api/login/`
4.  **Set Body**:
    *   Click **Body** -> **raw** -> **JSON**.
    *   Paste this:
        ```json
        {
            "username": "@my_test_user",
            "password": "password123"
        }
        ```
5.  **Send**: Click **Send**.
6.  **Copy Token**: Look at the response body at the bottom. It will look like:
    ```json
    {
        "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
    }
    ```
    **Select and copy** that long string of characters inside the quotes. You need it for the next steps!

---

## Step 3: Post a Found Item

1.  **Open a new tab** (+).
2.  **Set Method**: Select **POST**.
3.  **Enter URL**:
    `http://127.0.0.1:8000/api/items/`
4.  **Set Permission (Authorization)**:
    *   Click the **Headers** tab (next to Params, Authorization, Body).
    *   In the **Key** column, type: `Authorization`
    *   In the **Value** column, type: `Token ` followed by the token you copied.
        *   **Example**: `Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b`
        *   *Note: There is a space between "Token" and the code!*
5.  **Set Body**:
    *   Click **Body** -> **raw** -> **JSON**.
    *   Paste this:
        ```json
        {
            "university": "AASTU",
            "title": "Black Wallet",
            "description": "Found near the main gate",
            "location_text": "Main Gate Security",
            "date_of_event": "2025-12-14"
        }
        ```
6.  **Send**: Click **Send**.
    *   *Success?* You should see the created item details below.

---

---

## Step 5: Send Claim Request (as "Loser")

**Important**: You must be logged in as a **different user** than the one who posted the item. (Follow Step 1 & 2 to create a second user account if needed).

1.  **Open a new tab** (+).
2.  **Set Method**: Select **POST**.
3.  **Enter URL**:
    `http://127.0.0.1:8000/api/requests/`
4.  **Header**: Add `Authorization` -> `Token <your_second_user_token>`.
5.  **Body**:
    *   **JSON**:
        ```json
        {
            "item": 1
        }
        ```
        *(Change `1` to the ID of the item you want to claim).*
6.  **Send**.
    *   *Result*: You claimed the item!

---

## Step 6: View Requests & See Username (as "Finder")

**Log back in as the Finder** (the User from Step 3).

1.  **Open a new tab**.
2.  **Method**: **GET**.
3.  **URL**: `http://127.0.0.1:8000/api/requests/`
4.  **Header**: `Authorization` -> `Token <finder_token>`.
5.  **Send**.
6.  **Analyze JSON Response**:
    *   Look for the `from_user` object.
    *   You will see `telegram_username`. **This is the Username Exchange**.
    *   Now you can open Telegram and contact them!

---

## Step 7: Resolve Item (as "Finder")

Once you have returned the item, mark it as resolved.

1.  **Open a new tab**.
2.  **Method**: **POST**.
3.  **URL**: `http://127.0.0.1:8000/api/items/1/resolve/`
    *(Replace `1` with your item ID).*
4.  **Header**: `Authorization` -> `Token <finder_token>`.
5.  **Send**.
    *   *Result*: `{"status": "item marked as resolved"}`.

---

## Troubleshooting

*   **403 Forbidden**: Did you forget the Header? or did you paste the token wrong? Make sure it is `Token <your_string>`.
*   **400 Bad Request**: Check your JSON body. Did you miss a comma or a quote?
*   **405 Method Not Allowed**: Did you check GET vs POST? Login and Register MUST be POST.
*   **Authentication credentials were not provided**: You sent a POST request without a Token header.
