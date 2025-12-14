
import os
import django
import sys
import json

# Setup Django environment
sys.path.append('/home/salimhabeshawi/reclaimit-backend')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from items.models import ItemPost, ContactRequest

User = get_user_model()

def run_verification():
    print("Starting Verification...")
    
    # Clean up
    User.objects.all().delete()
    ItemPost.objects.all().delete()
    ContactRequest.objects.all().delete()
    
    client = APIClient()

    # 1. Register Users
    print("1. Registering Users...")
    finder_data = {"telegram_username": "@finder", "password": "password123", "full_name": "Finder User"}
    loser_data = {"telegram_username": "@loser", "password": "password123", "full_name": "Loser User"}
    
    resp_finder = client.post('/api/register/', finder_data)
    if resp_finder.status_code != 201:
        print(f"FAILED: Register Finder: {resp_finder.data}")
        return
    else:
        print("SUCCESS: Registered Finder")

    resp_loser = client.post('/api/register/', loser_data)
    if resp_loser.status_code != 201:
        print(f"FAILED: Register Loser: {resp_loser.data}")
        return
    else:
        print("SUCCESS: Registered Loser")
        
    # Login to get tokens (simulate usage)
    resp_token_f = client.post('/api/login/', {"username": "@finder", "password": "password123"})
    if 'token' in resp_token_f.data:
        token_finder = resp_token_f.data['token']
        print("SUCCESS: Finder Logged In")
    elif 'auth_token' in resp_token_f.data: # DRF sometimes returns 'auth_token' depending on version/config? No, default is 'token'.
        token_finder = resp_token_f.data['auth_token'] # Authtoken default view returns {"token": ...}
    else:
        print(f"FAILED: Finder Login: {resp_token_f.data}")
        # DRF obtain_auth_token expects 'username' and 'password'
        # User model uses telegram_username as USERNAME_FIELD so we pass that as 'username'
    
    resp_token_l = client.post('/api/login/', {"username": "@loser", "password": "password123"})
    if 'token' in resp_token_l.data:
        token_loser = resp_token_l.data['token']
        print("SUCCESS: Loser Logged In")
    else:
         print(f"FAILED: Loser Login: {resp_token_l.data}")
    
    # 2. Post Item (As Finder)
    print("2. Posting Item...")
    client.credentials(HTTP_AUTHORIZATION='Token ' + token_finder)
    item_data = {
        "university": "AASTU",
        "title": "Found Wallet",
        "description": "Black leather wallet found near library",
        "location_text": "Library Entrance",
        "date_of_event": "2023-10-27"
    }
    resp_item = client.post('/api/items/', item_data)
    if resp_item.status_code == 201:
        print("SUCCESS: Item Posted")
        item_id = resp_item.data['id']
    else:
        print(f"FAILED: Post Item: {resp_item.data}")
        return

    # 3. Create Contact Request (As Loser)
    print("3. Creating Contact Request...")
    client.credentials(HTTP_AUTHORIZATION='Token ' + token_loser)
    req_data = {"item": item_id}
    resp_req = client.post('/api/requests/', req_data)
    if resp_req.status_code == 201:
        print("SUCCESS: Request Created")
    else:
        print(f"FAILED: Create Request: {resp_req.data}")
        return

    # 4. Verify Visibility (Finder sees request)
    print("4. Verifying Visibility...")
    client.credentials(HTTP_AUTHORIZATION='Token ' + token_finder)
    resp_list = client.get('/api/requests/')
    if resp_list.status_code == 200:
        results = resp_list.data # Should be list or paginated
        if isinstance(results, dict) and 'results' in results:
             results = results['results']
             
        if len(results) > 0 and results[0]['from_user']['telegram_username'] == '@loser':
             print(f"SUCCESS: Finder sees request from {results[0]['from_user']['telegram_username']}")
        else:
             print(f"FAILED: Finder cannot see request: {results}")

    # 5. Verify Resolve Logic
    print("5. Verifying Resolve Logic...")
    client.credentials(HTTP_AUTHORIZATION='Token ' + token_finder)
    resp_resolve = client.post(f'/api/items/{item_id}/resolve/')
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
