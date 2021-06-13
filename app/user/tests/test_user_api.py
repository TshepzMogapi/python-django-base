from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
PROFILE_URL = reverse('user:profile')

def create_user(**params):
  return get_user_model().objects.create_user(**params)

class PublicUserApiTests(TestCase):
  """tests users public api"""

  def setUp(self):
    self.client = APIClient()

  def test_create_valid_user_success(self):
    """tests create user with correct payload"""
    payload = {
      'email': 'test@public.com',
      'password': 'Password1234!',
      'name': 'Another Test'
    }
    res = self.client.post(CREATE_USER_URL, payload)

    self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    user = get_user_model().objects.get(**res.data)
    self.assertTrue(user.check_password(payload['password']))
    self.assertNotIn('password', res.data)
  

  def test_user_exists(self):
    """tests creating a user that exists fails"""
    payload = {
      'email': 'test@public.com',
      'password': 'Password1234!',
      'name': 'Another Test'
    }
    create_user(**payload)

    res = self.client.post(CREATE_USER_URL, payload)

    self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
  
  def test_password_too_short(self):
    """tests password must be more that 4 characters"""
    payload = {
      'email': 'test@public.com',
      'password': 'Pas',
      'name': 'Another Test',
    }
    res = self.client.post(CREATE_USER_URL, payload)

    self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    user_exists = get_user_model().objects.filter(
      email=payload['email']
    ).exists()
    self.assertFalse(user_exists)
  
  def test_create_user_token(self):
    """tests token created for user"""
    payload = {
      'email': 'test@public.com',
      'password': 'Password1234!',
      'name': 'Another Test'
    }
    create_user(**payload)
    res = self.client.post(TOKEN_URL, payload)

    self.assertIn('token', res.data)
    self.assertEqual(res.status_code, status.HTTP_200_OK)
  
  def test_create_token_invalid_credetials(self):
    """tests token is NOT created if invalid credentials are provided"""
    create_user(email='test@test.com', password='Password1234!')
    payload = {
      'email': 'test@public.com',
      'password': 'WrongPassword1234!',
    }
    res = self.client.post(TOKEN_URL, payload)

    self.assertNotIn('token', res.data)
    self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
  
  def test_create_token_no_user(self):
    """tests token is not created if user doesn't exist"""
    payload = {
      'email': 'test@public.com',
      'password': 'Password1234!',
      'name': 'Another Test'
    }
    res = self.client.post(TOKEN_URL, payload)

    self.assertNotIn('token', res.data)
    self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

  def test_create_token_missing_field(self):
    """tests email and password are required"""
    res = self.client.post(TOKEN_URL, {'email': 'test', 'password': ''})
    self.assertNotIn('token', res.data)
    self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

  def test_retrieve_user_unauthorized(self):
    """tests that auth is required"""
    res = self.client.get(PROFILE_URL)

    self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateUserApiTests(TestCase):
  """tests api requests that require auth"""
  def setUp(self):
    self.user = create_user(
      email='test@public.com',
      password='Password1234!',
      name='Another Test'
    )
    self.client = APIClient()
    self.client.force_authenticate(user=self.user)

  def test_retrieve_profile_success(self):
    """tests retrieving profile for logged in user"""
    res = self.client.get(PROFILE_URL)

    self.assertEqual(res.status_code, status.HTTP_200_OK)
    self.assertEqual(res.data, {
      'name': self.user.name,
      'email': self.user.email
    })

  def test_post_not_allowed(self):
    """tests post is not allowed on profile url"""
    res = self.client.post(PROFILE_URL, {})

    self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
  
  def test_update_user(self):
    """tests updating user profile for authenticated user"""
    payload = {
      'password': 'NewPassword',
      'name': 'New name',
    }

    res = self.client.patch(PROFILE_URL, payload)

    self.user.refresh_from_db()
    self.assertEqual(self.user.name, payload['name'])
    self.assertTrue(self.user.check_password(payload['password']))
    self.assertEqual(res.status_code, status.HTTP_200_OK)
    