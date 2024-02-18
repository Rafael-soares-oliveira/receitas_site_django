from django.test import TestCase
from recipes.models import Category, Recipe, User


class RecipeMixin():
    def make_category(self, name='Test_category'):
        return Category.objects.create(name=name)

    def make_author(
            self,
            first_name='user',
            last_name='user',
            username='user',
            password='123456',
            email='username@email.com'
            ):
        return User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            email=email,
        )

    def make_recipe(
            self,
            category_data=None,
            author_data=None,
            title='Recipe Title Test',
            description='Recipe Description Test',
            slug='recipe-title-test',
            preparation_time=10,
            preparation_time_unit='Minutos',
            servings=4,
            servings_unit='Porções',
            preparation_step='Recipe Preparation Steps',
            preparation_step_is_html=False,
            is_published=True,
            cover='tests/tests_recipes/imagem_generica.jpg',
    ):
        if category_data is None:
            category_data = {}

        if author_data is None:
            author_data = {}

        return Recipe.objects.create(
            category=self.make_category(**category_data),
            author=self.make_author(**author_data),
            title=title,
            description=description,
            slug=slug,
            preparation_time=preparation_time,
            preparation_time_unit=preparation_time_unit,
            servings=servings,
            servings_unit=servings_unit,
            preparation_step=preparation_step,
            preparation_step_is_html=preparation_step_is_html,
            is_published=is_published,
            cover=cover,
        )

    def make_recipe_in_batch(self, qty=10):
        recipes = []
        for i in range(qty):
            kwargs = {'author_data': {'username': f'user{i}'},
                      'title': f'Recipe title {i}',
                      'slug': f'recipe-test-{i}'}
            recipe = self.make_recipe(**kwargs)
            recipes.append(recipe)
        return recipes


class RecipeTestModelBase(TestCase, RecipeMixin):
    def setUp(self) -> None:
        return super().setUp()
