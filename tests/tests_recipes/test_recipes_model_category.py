from test_recipes_model_base import RecipeTestModelBase
from django.core.exceptions import ValidationError


class RecipeCategoryModelTest(RecipeTestModelBase):
    def setUp(self) -> None:
        self.category = self.make_category()
        return super().setUp()

    def test_recipe_category_title_max_length_is_65_characters(self):
        category_title = 'A' * 66
        self.category = self.make_category(name=category_title)
        with self.assertRaises(ValidationError):
            self.category.full_clean()

    def test_recipe_string_representation_category(self):
        self.category = self.make_category(name='Testing Representation')
        self.category.full_clean()
        self.category.save()
        self.assertEqual(
            str(self.category),
            'Testing Representation',
            msg='Recipe string representation need to be same as title'
        )
