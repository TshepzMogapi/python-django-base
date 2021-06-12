from django.test import TestCase

from django.contrib.auth import get_user_model

class ModelTests(TestCase):

  def test_create_user_with_email_successful(self):
    """test creating a new user with email is successfull"""
    email = 'test@test.com'
    password = 'Testing1234!'
    user = get_user_model().objects.create_user(
      email=email,
      password=password
    )

    self.assertEqual(user.email, email)
    self.assertTrue(user.check_password(password))
  

  def test_user_email_normalized(self):
    """test email is normalized"""
    email = 'test@TEST.cOM'
    user = get_user_model().objects.create_user(
      email=email,
      password='Testing1234!'
    )

    self.assertEqual(user.email, email.lower())
  

  def test_user_invalid_email(self):
    """test creating user with no email raises error"""
    with self.assertRaises(ValueError):
      get_user_model().objects.create_user(None, 'Testing1234!')
  
  def test_create_new_superuser(self):
    """test creating a super user"""
    user = get_user_model().objects.create_superuser(
      email='test@test.com',
      password='Testing1234!'
    )

    self.assertTrue(user.is_superuser)
    self.assertTrue(user.is_staff)