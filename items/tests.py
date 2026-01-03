from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import User
from items.models import ItemPost, ContactRequest, University

class ReclaimItTests(APITestCase):
    def setUp(self):
        # Create Universities
        self.aastu, _ = University.objects.get_or_create(short_name="AASTU", defaults={"full_name": "Addis Ababa Science and Technology University"})
        
        # Create Users
        self.user1 = User.objects.create_user(telegram_username="@user1", password="password123")
        self.user2 = User.objects.create_user(telegram_username="@user2", password="password123")
        
        # Create an Item
        self.item = ItemPost.objects.create(
            user=self.user1,
            university=self.aastu,
            title="Lost Wallet",
            description="Black leather wallet",
            location_text="Library",
            date_of_event="2026-01-01"
        )
        
        # URLs
        self.login_url = reverse('login')
        self.items_url = reverse('items-list')
        self.requests_url = reverse('requests-list')

    def authenticate(self, user):
        response = self.client.post(self.login_url, {
            'telegram_username': user.telegram_username,
            'password': 'password123'
        })
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_item_listing_requires_auth(self):
        response = self.client.get(self.items_url)
        # Assuming IsAuthenticated is set as default in settings or viewset
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_item(self):
        self.authenticate(self.user1)
        response = self.client.post(self.items_url, {
            'university': self.aastu.short_name,
            'title': 'Lost Keys',
            'description': 'Keychain with 3 keys',
            'location_text': 'Cafeteria',
            'date_of_event': '2026-01-02'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ItemPost.objects.count(), 2)

    def test_contact_request_privacy(self):
        # User 2 requests User 1's item
        self.authenticate(self.user2)
        response = self.client.post(self.requests_url, {
            'item': self.item.id
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        request_id = response.data['id']

        # Check privacy before acceptance
        # User 2 (claimant) should NOT see User 1's (finder) username in list
        response = self.client.get(f'{self.requests_url}{request_id}/')
        self.assertEqual(response.data['is_accepted'], False)
        # to_user_data should NOT have telegram_username if masking is working
        self.assertNotIn('telegram_username', response.data['to_user_data'])

        # User 1 accepts
        self.authenticate(self.user1)
        accept_url = reverse('requests-accept', kwargs={'pk': request_id})
        response = self.client.post(accept_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Now User 2 should see User 1's username
        self.authenticate(self.user2)
        response = self.client.get(f'{self.requests_url}{request_id}/')
        self.assertTrue(response.data['is_accepted'])
        self.assertIn('telegram_username', response.data['to_user_data'])
        self.assertEqual(response.data['to_user_data']['telegram_username'], '@user1')

    def test_cannot_request_own_item(self):
        self.authenticate(self.user1)
        response = self.client.post(self.requests_url, {
            'item': self.item.id
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
