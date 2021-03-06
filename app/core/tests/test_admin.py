from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

class AdminSiteTests(TestCase):

  def setUp(self):
      self.client = Client()
      self.admin_user = get_user_model().objects.create_superuser(
        email='admin@test.com',
        password='Testing1234!'
      )
      self.client.force_login(self.admin_user)
      self.user = get_user_model().objects.create_user(
        email='test@test.com',
        password='Testing1234!',
        name='Tester Tester'
      )
  
  def test_users_listed_page(self):
    """test that user are listed"""
    url = reverse('admin:core_user_changelist')
    res = self.client.get(url) #response

    self.assertContains(res, self.user.name)
    self.assertContains(res, self.user.email)
  

  def test_user_change_page(self):
    """test user edit works"""
    url = reverse('admin:core_user_change', args=[self.user.id])
    res = self.client.get(url)

    self.assertEqual(res.status_code, 200)
  
  def test_user_create_page(self):
    """test user create works"""
    url = reverse('admin:core_user_add')
    res = self.client.get(url)

    self.assertEqual(res.status_code, 200)