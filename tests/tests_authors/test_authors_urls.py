from unittest import TestCase
from django.urls import reverse


class AuthorsURLsTest(TestCase):
    def test_authors_register_url_is_correct(self):
        home_url = reverse('authors:register')
        self.assertEqual(home_url, '/authors/register/')
