from test_recipes_model_base import RecipeTestModelBase
from recipes.views import views_site
from django.urls import reverse, resolve
from unittest.mock import patch
from django.utils import translation


class RecipeViewsTestHome(RecipeTestModelBase):
    def test_recipes_home_views_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func.view_class, views_site.RecipeListViewHome)

    def test_recipe_home_view_returns_status_code_200_OK(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'pages/home.html')

    def test_recipe_home_template_shows_no_recipes_found_if_no_recipes(self):
        msg_ptbr = 'Não há receita'
        msg_en = 'No recipes found'
        html_language = translation.get_language()
        response = self.client.get(reverse('recipes:home'))
        if html_language == 'pt-br':
            self.assertIn(msg_ptbr, response.content.decode('utf-8'))
        else:
            self.assertIn(msg_en, response.content.decode('utf-8'))

    def test_recipe_home_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'pk': 10000})
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_home_loads_recipes(self):
        self.make_recipe()
        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')

        self.assertIn('Recipe Title', content)
        self.assertIn('4 Porções', content)

    def test_recipe_home_template_do_not_published(self):
        """Test recipe is_published=False don't show"""
        self.make_recipe(is_published=False)
        msg_ptbr = 'Não há receita'
        msg_en = 'No recipes found'
        html_language = translation.get_language()
        response = self.client.get(reverse('recipes:home'))
        if html_language == 'pt-br':
            self.assertIn(msg_ptbr, response.content.decode('utf-8'))
        else:
            self.assertIn(msg_en, response.content.decode('utf-8'))

    def test_recipe_home_template_shows_contents_per_page(self):
        self.make_recipe_in_batch(qty=20)

        with patch('recipes.views.views_site.PER_PAGE', new=10):
            response = self.client.get(reverse('recipes:home'))
            context = response.context['recipes']
            paginator = context.paginator
            self.assertEqual(paginator.num_pages, 2)
            self.assertEqual(len(paginator.get_page(1)), 10)
            self.assertEqual(len(paginator.get_page(2)), 10)
