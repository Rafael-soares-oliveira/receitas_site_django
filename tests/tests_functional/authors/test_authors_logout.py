from .base import AuthorsBaseFunctionalTest
from selenium.webdriver.common.by import By
from django.contrib.auth.models import User
import pytest


@pytest.mark.functional_test
class AuthorsTestLogout(AuthorsBaseFunctionalTest):
    def test_logout_sucessful(self):
        User.objects.create_user(username='user', password='P@ss4656')
        # Acess the login page
        self.browser.get(self.live_server_url + '/authors/login/')

        # Insert into username field
        username = self.browser.find_element(
            By.XPATH,
            '/html/body/main/div[2]/form/div[1]/div[1]/input'
            )
        username.send_keys('user')
        # Insert into password field
        password = self.browser.find_element(
            By.XPATH,
            '/html/body/main/div[2]/form/div[1]/div[2]/input'
            )
        password.send_keys('P@ss4656')

        # Click on the send button
        self.browser.find_element(
            By.XPATH,
            '/html/body/main/div[2]/form/div[2]/div/button').click()

        self.browser.find_element(
            By.XPATH,
            '/html/body/main/div/form/button').click()

        username = self.browser.find_element(
            By.XPATH,
            '/html/body/main/div[2]/form/div[1]/div[1]/input'
            )
        username.send_keys('user')
        # Insert into password field
        password = self.browser.find_element(
            By.XPATH,
            '/html/body/main/div[2]/form/div[1]/div[2]/input'
            )
        password.send_keys('P@ss4656')
