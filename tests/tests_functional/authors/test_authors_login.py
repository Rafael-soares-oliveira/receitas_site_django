from .base import AuthorsBaseFunctionalTest
from selenium.webdriver.common.by import By
import pytest
from django.contrib.auth.models import User
from django.urls import reverse


@pytest.mark.functional_test
class AuthorsTestLogin(AuthorsBaseFunctionalTest):
    def acess_login_page(self):
        # Acess the homepage
        self.browser.get(self.live_server_url)

        # Click on the login button
        self.browser.find_element(
            By.XPATH,
            '/html/body/header/div[1]/form[2]/button').click()

    def test_login_sucessfully(self):
        # User credentials
        user = User.objects.create_user(username='user', password='P@ss4656')

        self.acess_login_page()

        # Insert into username field
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

        form = self.browser.find_element(
            By.XPATH,
            '/html/body/main')

        msg_sucess = f'Your are logged in with {user.username}'
        msg_logged = f'Your are logged in with {user.username}'
        self.assertIn(msg_sucess, form.text)
        self.assertIn(msg_logged, form.text)

    def test_login_fail(self):
        self.acess_login_page()

        # Insert into username field
        self.browser.find_element(
            By.XPATH,
            '/html/body/main/div[2]/form/div[1]/div[1]/input'
            ).send_keys(' ')

        # Insert into password field
        self.browser.find_element(
            By.XPATH,
            '/html/body/main/div[2]/form/div[1]/div[2]/input'
            ).send_keys(' ')

        # Click on the send button
        self.browser.find_element(
            By.XPATH,
            '/html/body/main/div[2]/form/div[2]/div/button').click()

        form = self.browser.find_element(
            By.XPATH,
            '/html/body/main')

        msg_error = 'Invalid username or password'
        self.assertIn(msg_error, form.text)

    def test_login_create_raises_404_if_not_method_POST(self):
        self.browser.get(
            self.live_server_url + reverse('authors:login_create'))

        self.assertIn(
            'Not Found',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )
