from django.test import LiveServerTestCase  # noqa:F401
from utils.browser_selenium import launchBrowser
from tests.tests_recipes.test_recipes_model_base import RecipeMixin
import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


class RecipeBaseFunctionalTest(StaticLiveServerTestCase, RecipeMixin):
    def setUp(self) -> None:
        self.browser = launchBrowser('--headless')
        return super().setUp()

    def sleep(self):
        time.sleep(6)

    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()
