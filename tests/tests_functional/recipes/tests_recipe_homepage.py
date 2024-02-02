from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .base import RecipeBaseFunctionalTest
import pytest
from unittest.mock import patch


@pytest.mark.functional_test
class RecipeHomepageFunctionalTest(RecipeBaseFunctionalTest):
    def test_recipe_home_page_without_recipes_not_found_message(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.sleep()
        self.assertIn('No recipes found', body.text)

    def test_recipe_search_input_can_find_correct_recipes(self):
        recipes = self.make_recipe_in_batch(2)

        # User acess the homepage
        self.browser.get(self.live_server_url)

        # Look for a search input with the text "Search recipe"
        search_input = self.browser.find_element(
            By.XPATH,
            '//input[@placeholder="Search recipe"]'
            )

        # Click on the input, insert the text "Recipe title 1" and press Enter
        search_input.send_keys(recipes[0].title)
        search_input.send_keys(Keys.ENTER)

        self.assertIn(
            recipes[0].title, self.browser.find_element(
                By.CLASS_NAME, 'main-content-list').text)

        self.sleep()

    @patch('recipes.views.PER_PAGE', new=1)
    def test_recipe_home_page_pagination(self):
        self.make_recipe_in_batch(2)

        # User acess the homepage
        self.browser.get(self.live_server_url)

        # Look at the pagination and click on page 2
        pagination = self.browser.find_element(
            By.XPATH,
            '//div[@aria-label="Go to page 2"]'
        )
        pagination.click()

        self.assertEqual(
            len(self.browser.find_elements(By.CLASS_NAME, 'recipe')), 1)

        self.sleep()
