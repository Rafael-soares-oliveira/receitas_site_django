from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .base import RecipeBaseFunctionalTest
import pytest
from unittest.mock import patch
from django.utils import translation


@pytest.mark.functional_test
class RecipeHomepageFunctionalTest(RecipeBaseFunctionalTest):
    def test_recipe_home_page_without_recipes_not_found_message(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        msg_ptbr = 'Não há receita'
        msg_en = 'No recipes found'
        html_language = translation.get_language()

        if html_language == 'pt-br':
            self.assertIn(msg_ptbr, body.text)
        else:
            self.assertIn(msg_en, body.text)

    def test_recipe_search_input_can_find_correct_recipes(self):
        recipes = self.make_recipe_in_batch(2)
        html_language = translation.get_language()
        # User acess the homepage
        self.browser.get(self.live_server_url)

        # Look for a search input with the text "Search recipe"
        if html_language == 'pt-br':
            search_input = self.browser.find_element(
                By.XPATH,
                '//input[@placeholder="Pesquisar receita"]'
                )
        else:
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

    @patch('recipes.views.views_site.PER_PAGE', new=1)
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
