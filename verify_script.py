import os
import sys
import time

import django

# Setup Django environment
sys.path.append("/home/salimhabeshawi/reclaimit-backend")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth import get_user_model  # noqa: E402
from rest_framework.test import APIClient  # noqa: E402

from items.models import ItemPost  # noqa: E402

User = get_user_model()


def run_verification():
    print("Starting Verification...")

    unique_suffix = int(time.time())
    finder_username = f"@finder_{unique_suffix}"
    loser_username = f"@loser_{unique_suffix}"

    client = APIClient()

    # 0. Check Authorization for Items
    print("0. Checking Authorization for Items (Unauthenticated)...")
    resp_items_unauth = client.get("/api/items/")
    if resp_items_unauth.status_code == 401:
        print("SUCCESS: Items list is restricted to authenticated users")
    else:
        print(
            f"FAILED: Items list is accessible without auth: Status {resp_items_unauth.status_code}"
        )
        return

    # 1. Register Users
    print(f"1. Registering Users ({finder_username}, {loser_username})...")
    finder_data = {
        "telegram_username": finder_username,
        "password": "password123",
        "full_name": "Finder User",
    }
    loser_data = {
        "telegram_username": loser_username,
        "password": "password123",
        "full_name": "Loser User",
    }

    resp_finder = client.post("/api/register/", finder_data)
    if resp_finder.status_code != 201:
        print(f"FAILED: Register Finder: {resp_finder.data}")
        return
    else:
        print("SUCCESS: Registered Finder")

    resp_loser = client.post("/api/register/", loser_data)
    if resp_loser.status_code != 201:
        print(f"FAILED: Register Loser: {resp_loser.data}")
        return
    else:
        print("SUCCESS: Registered Loser")

    # Login to get tokens (simulated)
    resp_token_f = client.post(
        "/api/login/", {"telegram_username": finder_username, "password": "password123"}
    )
    if "access" in resp_token_f.data:
        token_finder = resp_token_f.data["access"]
        print("SUCCESS: Finder Logged In (JWT)")
    else:
        print(f"FAILED: Finder Login: {resp_token_f.data}")
        return

    resp_token_l = client.post(
        "/api/login/", {"telegram_username": loser_username, "password": "password123"}
    )
    if "access" in resp_token_l.data:
        token_loser = resp_token_l.data["access"]
        print("SUCCESS: Loser Logged In (JWT)")
    else:
        print(f"FAILED: Loser Login: {resp_token_l.data}")
        return

    # 2. Post Item (As Finder)
    print("2. Posting Item...")
    client.credentials(HTTP_AUTHORIZATION="Bearer " + token_finder)
    item_data = {
        "university": "AASTU",
        "title": "Found Wallet",
        "description": "Black leather wallet found near library",
        "location_text": "Library Entrance",
        "date_of_event": "2023-10-27",
    }
    resp_item = client.post("/api/items/", item_data)
    if resp_item.status_code == 201:
        print("SUCCESS: Item Posted")
        item_id = resp_item.data["id"]
    else:
        print(f"FAILED: Post Item: {resp_item.data}")
        return

    # 3. Create Contact Request (As Loser)
    print("3. Creating Contact Request...")
    client.credentials(HTTP_AUTHORIZATION="Bearer " + token_loser)
    req_data = {"item": item_id}
    resp_req = client.post("/api/requests/", req_data)
    if resp_req.status_code == 201:
        print("SUCCESS: Request Created")
    else:
        print(f"FAILED: Create Request: {resp_req.data}")
        return

    # 4. Verify Privacy (Loser cannot see Finder's username initially)
    print("4. Verifying Privacy (Loser seeing Finder)...")
    client.credentials(HTTP_AUTHORIZATION="Bearer " + token_loser)
    resp_list_l = client.get("/api/requests/")
    req_id = resp_list_l.data[0]["id"]
    if "telegram_username" in resp_list_l.data[0]["to_user_data"]:
        print("FAILED: Loser can see Finder username before acceptance")
        return
    else:
        print("SUCCESS: Finder username hidden from Loser initially")

    # 5. Verify Visibility (Finder sees request with Loser's username)
    print("5. Verifying Finder Visibility...")
    client.credentials(HTTP_AUTHORIZATION="Bearer " + token_finder)
    resp_list_f = client.get("/api/requests/")
    if (
        len(resp_list_f.data) > 0
        and resp_list_f.data[0]["from_user_data"]["telegram_username"] == loser_username
    ):
        print(f"SUCCESS: Finder sees request from {loser_username}")
    else:
        print(f"FAILED: Finder cannot see request from Loser: {resp_list_f.data}")
        return

    # 6. Accept Request (As Finder)
    print("6. Accepting Request...")
    resp_accept = client.post(f"/api/requests/{req_id}/accept/")
    if resp_accept.status_code == 200:
        print("SUCCESS: Request Accepted")
    else:
        print(f"FAILED: Accept Request: {resp_accept.data}")
        return

    # 7. Verify Privacy (Loser can NOW see Finder's username)
    print("7. Verifying Visibility after Acceptance...")
    client.credentials(HTTP_AUTHORIZATION="Bearer " + token_loser)
    resp_list_l2 = client.get("/api/requests/")
    if resp_list_l2.data[0]["to_user_data"].get("telegram_username") == finder_username:
        print(f"SUCCESS: Loser can now see Finder username: {finder_username}")
    else:
        print("FAILED: Loser still cannot see Finder username")
        return

    # 8. Verify Resolve Logic
    print("8. Verifying Resolve Logic...")
    client.credentials(HTTP_AUTHORIZATION="Bearer " + token_finder)
    resp_resolve = client.post(f"/api/items/{item_id}/resolve/")
    if resp_resolve.status_code == 200:
        item = ItemPost.objects.get(id=item_id)
        if item.is_resolved:
            print("SUCCESS: Item Resolved")
        else:
            print("FAILED: Item not resolved in DB")
    else:
        print(f"FAILED: Resolve Action: {resp_resolve.data}")


if __name__ == "__main__":
    run_verification()
