from django.urls import reverse, resolve
from recipes.views import views_site
from test_recipes_model_base import RecipeTestModelBase
# Uses a database
from django.utils import translation


class Recipe_views_test_search(RecipeTestModelBase):
    def test_recipe_search_uses_correct_view_template(self):
        resolved = resolve(reverse('recipes:search'))
        self.assertIs(
            resolved.func.view_class, views_site.RecipeListViewSearch)

    def test_recipe_search_loads_correct_template(self):
        response = self.client.get(reverse('recipes:search') + '?q=1')
        self.assertTemplateUsed(response, 'pages/search-view.html')

    def test_recipe_search_raises_404_if_no_search_term(self):
        url = reverse('recipes:search')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_recipe_search_term_is_on_page_title_and_escaped(self):
        url = reverse('recipes:search') + '?q=<Test>'
        response = self.client.get(url)
        self.assertIn('Search for &quot;&lt;Test&gt;&quot;',
                      response.content.decode('utf-8'))

    def test_recipe_search_return_none_if_is_published_is_false(self):
        self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipes:search') + '?q=Test')
        msg_ptbr = 'Não há receita'
        msg_en = 'No recipes found'
        html_language = translation.get_language()
        if html_language == 'pt-br':
            self.assertIn(msg_ptbr, response.content.decode('utf-8'))
        else:
            self.assertIn(msg_en, response.content.decode('utf-8'))

    def test_recipe_search_can_find_recipe_by_title(self):
        recipe1 = self.make_recipe(title='This is recipe one', slug='one',
                                   author_data={'username': 'one'})
        recipe2 = self.make_recipe(title='This is recipe two', slug='two',
                                   author_data={'username': 'two'})

        search_url = reverse('recipes:search')
        response1 = self.client.get(f'{search_url}?q={recipe1.title}')
        response2 = self.client.get(f'{search_url}?q={recipe2.title}')
        response_both = self.client.get(f'{search_url}?q=this is recipe')

        self.assertIn(recipe1, response1.context['recipes'])
        self.assertIn(recipe2, response2.context['recipes'])

        self.assertNotIn(recipe1, response2.context['recipes'])
        self.assertNotIn(recipe2, response1.context['recipes'])

        self.assertIn(recipe1, response_both.context['recipes'])
        self.assertIn(recipe2, response_both.context['recipes'])
