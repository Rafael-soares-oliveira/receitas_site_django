from django.urls import reverse, resolve
from recipes.views import views_site
from test_recipes_model_base import RecipeTestModelBase  # Uses a database


class Recipe_views_test_recipes(RecipeTestModelBase):

    def test_recipes_recipe_views_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'pk': 1}))
        self.assertIs(view.func.view_class, views_site.RecipeDetail)

    def test_recipe_recipe_view_loads_correct_template(self):
        recipe = self.make_recipe()
        response = self.client.get(reverse(
            'recipes:recipe', kwargs={'pk': recipe.pk}))  # type:ignore
        self.assertTemplateUsed(response, 'pages/recipe-view.html')
