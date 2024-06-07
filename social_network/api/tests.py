from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from api.models import FriendRequest

User = get_user_model()

class UserAuthTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.signup_url = reverse('user-create')
        self.login_url = reverse('user-login')

    def test_user_signup(self):
        data = {'email': 'testuser@example.com', 'password': 'password123'}
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

    def test_user_login(self):
        user = User.objects.create_user(email='testuser@example.com', password='password123')
        data = {'email': 'testuser@example.com', 'password': 'password123'}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

class UserSearchTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='testuser@example.com', password='password123', name='Test User')
        self.client.force_authenticate(user=self.user)
        self.search_url = reverse('user-search')

    def test_search_by_email(self):
        response = self.client.get(self.search_url, {'query': 'testuser@example.com'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['email'], 'testuser@example.com')

    def test_search_by_name(self):
        response = self.client.get(self.search_url, {'query': 'Test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'Test User')

class FriendRequestTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(email='user1@example.com', password='password123', name='User One')
        self.user2 = User.objects.create_user(email='user2@example.com', password='password123', name='User Two')
        self.client.force_authenticate(user=self.user1)
        self.friend_request_url = reverse('friend-request-create')
        self.friend_request_list_url = reverse('friend-request-list')
        self.friend_list_url = reverse('friend-list')

    def test_send_friend_request(self):
        data = {'to_user_id': self.user2.id}
        response = self.client.post(self.friend_request_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(FriendRequest.objects.count(), 1)

    def test_accept_friend_request(self):
        friend_request = FriendRequest.objects.create(from_user=self.user1, to_user=self.user2, status='pending')
        self.client.force_authenticate(user=self.user2)
        accept_url = reverse('friend-request-update', args=[friend_request.id])
        response = self.client.post(accept_url, {'action': 'accept'})
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        friend_request.refresh_from_db()
        self.assertEqual(friend_request.status, 'accepted')

    def test_reject_friend_request(self):
        friend_request = FriendRequest.objects.create(from_user=self.user1, to_user=self.user2, status='pending')
        self.client.force_authenticate(user=self.user2)
        reject_url = reverse('friend-request-update', args=[friend_request.id])
        response = self.client.post(reject_url, {'action': 'reject'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        friend_request.refresh_from_db()
        self.assertEqual(friend_request.status, 'rejected')

    def test_list_friends(self):
        FriendRequest.objects.create(from_user=self.user1, to_user=self.user2, status='accepted')
        response = self.client.get(self.friend_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['email'], self.user2.email)

    def test_list_pending_friend_requests(self):
        FriendRequest.objects.create(from_user=self.user2, to_user=self.user1, status='pending')
        response = self.client.get(self.friend_request_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['from_user'], self.user2.email)
