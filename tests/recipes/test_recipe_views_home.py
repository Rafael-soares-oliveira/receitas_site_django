from django.test import TestCase
from recipes import views
from django.urls import reverse, resolve
# from recipes.models import Recipe, Category
# from unittest.mock import patch


class RecipeViewsTestHome(TestCase):
    def test_recipes_home_views_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipe_home_view_returns_status_code_200_OK(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'pages/home.html')
