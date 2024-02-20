from django.urls import reverse, resolve
from recipes.views import views_site
from django.test import SimpleTestCase  # Does not have a database


class Recipe_views_test_category(SimpleTestCase):
    def test_recipes_category_views_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(view.func.view_class, views_site.RecipeListViewCategory)
