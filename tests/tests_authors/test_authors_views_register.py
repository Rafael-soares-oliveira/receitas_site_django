from django.test import SimpleTestCase  # Use that if not use a database
from authors import views
from django.urls import reverse, resolve


class Authors_views_test_home(SimpleTestCase):
    def test_authors_register_views_is_correct(self):
        view = resolve(reverse('authors:register'))
        self.assertIs(view.func, views.register_view)

    def test_authors_register_view_returns_status_code_200_OK(self):
        response = self.client.get(reverse('authors:register'))
        self.assertEqual(response.status_code, 200)

    def test_authors_register_view_loads_correct_template(self):
        response = self.client.get(reverse('authors:register'))
        self.assertTemplateUsed(response, 'pages/register_view.html')
