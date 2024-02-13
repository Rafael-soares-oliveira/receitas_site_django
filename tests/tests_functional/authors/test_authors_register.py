from .base import AuthorsBaseFunctionalTest
from selenium.webdriver.common.by import By
import pytest


@pytest.mark.functional_test
class AuthorsTestRegister(AuthorsBaseFunctionalTest):
    def click_send_button(self):
        self.browser.find_element(
            By.XPATH,
            '/html/body/main/div[2]/form/div[2]/div/button').click()

    def fill_form_dummy_data_and_send(
            self,
            text=['', 'User', 'UserUser', 'user', 'user@email.com', 'P@ss4656',
                  'P@ss4656']):

        # Acess the homepage
        self.browser.get(self.live_server_url)

        # Click on the toggle menu
        self.browser.find_element(
            By.XPATH,
            '/html/body/nav/label').click()
        # Click on the register button
        self.browser.find_element(
            By.XPATH,
            '/html/body/nav/ul/li[1]/form/button').click()

        for i in range(1, 7):
            self.browser.find_element(
                By.XPATH,
                f'/html/body/main/div[2]/form/div[1]/div[{str(i)}]/input'
            ).send_keys(text[i])

        self.click_send_button()

    def test_error_message_for_empty_field_and_email_invalid(self):
        # EmailField requires that the format be at least equal to 1@1
        text_input = ['', '    ', '    ', '    ', '1@1', '    ', '    ']
        text_error = 'This field must not be empty'
        email_error = 'Informe um endereço de email válido'

        self.fill_form_dummy_data_and_send(text=text_input)

        for i in range(1, 7):
            if i == 4:
                continue
            form = self.browser.find_element(
                By.XPATH,
                f'/html/body/main/div[2]/form/div[1]/div[{str(i)}]'
            ).text
            self.assertIn(text_error, form)

        email_form = self.browser.find_element(
                By.XPATH,
                '/html/body/main/div[2]/form/div[1]/div[4]'
            )
        self.assertIn(email_error, email_form.text)

    def test_passwords_do_not_match(self):
        msg_error = 'Passwords do not match!'

        self.fill_form_dummy_data_and_send(
            text=['', 'User', 'UserUser', 'user', 'user@email.com', 'P@ss4656',
                  'P@ss4655'])

        password = self.browser.find_element(
                By.XPATH,
                '/html/body/main/div[2]/form/div[1]/div[5]'
            )
        password_confirm = self.browser.find_element(
                By.XPATH,
                '/html/body/main/div[2]/form/div[1]/div[6]'
            )

        self.assertIn(msg_error, password.text)
        self.assertIn(msg_error, password_confirm.text)

    def test_username_with_invalid_characters(self):
        msg_error = 'Informe um nome de usuário válido. Este valor pode conter'
        ' apenas letras, números e os seguintes caracteres @/./+/-/_.'

        self.fill_form_dummy_data_and_send(
            text=['', 'User', 'UserUser', '####', 'user@email.com', 'P@ss4656',
                  'P@ss4656'])

        username = self.browser.find_element(
                By.XPATH,
                '/html/body/main/div[2]/form/div[1]/div[3]'
            )

        self.assertIn(msg_error, username.text)

    def test_register_created_sucessfully(self):
        msg = 'Your user is created, please log in.'
        self.fill_form_dummy_data_and_send()

        msg_sucess = self.browser.find_element(
                By.XPATH,
                '/html/body/main')

        self.assertIn(msg, msg_sucess.text)
