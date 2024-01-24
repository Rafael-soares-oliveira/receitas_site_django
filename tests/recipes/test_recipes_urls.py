from unittest import TestCase
from django.urls import reverse


class TestRecipesUrl(TestCase):
    def test_if_home_url_load(self):
        url = reverse('recipes:home')
        self.assertEqual(url, '/')
