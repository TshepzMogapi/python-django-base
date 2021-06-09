from django.test import TestCase

from app.randomstuff import last_three_chars

class RandomTests(TestCase):

  def test_last_three_chars(self):
    """Tests that last three characters of a string are return"""
    self.assertEqual(last_three_chars('Qwerty'),'rty')