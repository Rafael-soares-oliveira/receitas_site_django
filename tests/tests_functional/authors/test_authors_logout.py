from .base import AuthorsBaseFunctionalTest
from selenium.webdriver.common.by import By
from django.contrib.auth.models import User
import pytest


@pytest.mark.functional_test
class AuthorsTestLogout(AuthorsBaseFunctionalTest):
    def login(self):
        User.objects.create_user(username='user', password='P@ss4656')
        # Acess the homepage
        self.browser.get(self.live_server_url)

        # Click on the login button
        self.browser.find_element(
            By.XPATH,
            '/html/body/header/div[1]/form[2]/button').click()

        self.browser.find_element(
            By.XPATH,
            '/html/body/main/div[2]/form/div[1]/div[1]/input'
            ).send_keys('user')

        # Insert into password field
        self.browser.find_element(
            By.XPATH,
            '/html/body/main/div[2]/form/div[1]/div[2]/input'
            ).send_keys('P@ss4656')

        # Click on the send button
        self.browser.find_element(
            By.XPATH,
            '/html/body/main/div[2]/form/div[2]/div/button').click()

    def logout_sucessful(self):
        self.login()
        # Click on logout button
        self.browser.find_element(
            By.XPATH,
            '/html/body/header/div[1]/form[2]/button').click()
        self.sleep()
