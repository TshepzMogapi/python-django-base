from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Product

from product.serializers import ProductSerializer

PRODCTS_URL = reverse('product:list')

class PublicProductApiTests(TestCase):
  def setUp(self):
    self.client = APIClient()

  # def test_authentication_not_required(self): 

class PrivateProductApiTests(TestCase):
  """tests authorized user products"""


  def setUp(self):
      self.user = get_user_model().objects.create_user(
        'test@public.com',
        'Password1234!',
      )

      self.client = APIClient()
      self.client.force_authenticate(self.user)

  def test_retrieve_products(self):
    """tests retrieving products"""
    Product.objects.create(user=self.user, name="Laptop")
    Product.objects.create(user=self.user, name="Monitor")

    res = self.client.get(PRODCTS_URL)

    products = Product.objects.all().order_by('-name')
    serializer = ProductSerializer(products, many=True)
    self.assertEqual(res.status_code, status.HTTP_200_OK)
    self.assertEqual(res.data, serializer.data)
