from django.test import SimpleTestCase  # Use that if not use a database
from authors import views
from django.urls import reverse, resolve


class Authors_views_test_home(SimpleTestCase):
    def test_authors_login_views_is_correct(self):
        view = resolve(reverse('authors:login'))
        self.assertIs(view.func, views.login_view)

    def test_authors_login_view_returns_status_code_200_OK(self):
        response = self.client.get(reverse('authors:login'))
        self.assertEqual(response.status_code, 200)

    def test_authors_login_view_loads_correct_template(self):
        response = self.client.get(reverse('authors:login'))
        self.assertTemplateUsed(response, 'pages/login.html')

    def test_authors_login_raises_404_if_no_request_POST(self):
        url = reverse('authors:login_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_authors_login_create_views_is_correct(self):
        view = resolve(reverse('authors:login_create'))
        self.assertIs(view.func, views.login_create)
