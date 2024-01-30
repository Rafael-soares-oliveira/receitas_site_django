# unittest is 0.5 seconds faster than SimpleTestCase
from unittest import TestCase
from parameterized import parameterized
from authors.forms import RegisterForm
from django.test import TestCase as DjangoTestCase
from django.urls import reverse


class AuthorRegisterFormUnitTest(TestCase):

    @parameterized.expand([
        ('first_name', 'Type your first name'),
        ('last_name', 'Type your last name'),
        ('username', 'Type your username'),
        ('email', 'Type your email. Ex: email@email.com'),
        ('password', 'Type your password'),
        ('password_confirm', 'Repeat your password'),
    ])
    def test_if_placeholder_is_correct(self, field, placeholder_msg):
        form = RegisterForm()
        placeholder = form[field].field.widget.attrs['placeholder']
        self.assertEqual(placeholder_msg, placeholder)

    @parameterized.expand([
        ('username', 'Username must have letters, numbers or one of those '
         '@.+-_. The length should be between 4 and 16 characters.'),
        ('password', 'Password must have at least one uppercase letter, '
            'one lowercase letter and one number.'
            ' The length should be at least 8 characters.'),
    ])
    def test_if_help_text_is_correct(self, field, help_text_msg):
        form = RegisterForm()
        help_text = form[field].field.help_text
        self.assertEqual(help_text_msg, help_text)

    @parameterized.expand([
        ('first_name', 'First name'),
        ('last_name', 'Last name'),
        ('username', 'Username'),
        ('email', 'Email'),
        ('password', 'Password'),
        ('password_confirm', 'Confirm password'),
    ])
    def test_if_label_is_correct(self, field, label_msg):
        form = RegisterForm()
        label = form[field].field.label
        self.assertEqual(label_msg, label)


class AuthorRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self, *args, **kwargs) -> None:
        self.form_data = {
            'username': 'user',
            'first_name': 'first',
            'last_name': 'last',
            'email': 'tests@anyemail.com',
            'password': 'Str0ngP@ssword1',
            'password_confirm': 'Str0ngP@ssword1'
        }
        return super().setUp(*args, **kwargs)

    @parameterized.expand([
        ('username', 'This field must not be empty'),
        ('first_name', 'This field must not be empty'),
        ('last_name', 'This field must not be empty'),
        ('email', 'This field must not be empty'),
        ('password', 'This field must not be empty'),
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.context['form'].errors.get(field))

    def test_username_field_min_length_should_be_four(self):
        self.form_data['username'] = 'abc'
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = 'Username must have at least 4 characters'
        self.assertIn(msg, response.context['form'].errors.get('username'))

    def test_username_field_max_length_should_be_sixteen(self):
        self.form_data['username'] = 'a' * 17
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = 'Username must have a maximum of 16 characters'
        self.assertIn(msg, response.context['form'].errors.get('username'))

    def test_password_field_have_lower_upper_and_letters(self):
        self.form_data['password'] = 'abc'
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = 'Password must have at least one uppercase letter, '
        'one lowercase letter and one number. '
        'The length should be at least 8 characters.'
        self.assertIn(msg, response.context['form'].errors.get('password')[0])
        self.assertIn(msg, response.content.decode('utf-8'))

        self.form_data['password'] = 'Abc@1234'
        self.assertNotIn(
            msg, response.context['form'].errors.get('password'))

    def test_password_and_password_confirm_are_equal(self):
        self.form_data['password'] = 'Abc@1234'
        self.form_data['password_confirm'] = 'Abc@123'
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = 'Passwords do not match!'
        self.assertIn(msg, response.context['form'].errors.get('password'))
        self.assertIn(msg, response.content.decode('utf-8'))

        self.form_data['password'] = 'Abc@1234'
        self.form_data['password_confirm'] = 'Abc@1234'
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertNotIn(msg, response.content.decode('utf-8'))

    def test_send_get_request_to_registration_create_view_returns_404(self):
        url = reverse('authors:register_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_if_email_is_unique(self):
        url = reverse('authors:register_create')
        self.client.post(url, data=self.form_data, follow=True)
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = 'User e-mail is already in use'
        self.assertIn(msg, response.context['form'].errors.get('email'))

    def test_author_created_can_login(self):
        url = reverse('authors:register_create')
        self.form_data.update({
            'username': 'testuser',
            'password': 'P@ss4656',
            'password_confirm': 'P@ss4656',
        })
        self.client.post(url, data=self.form_data, follow=True)

        is_authenticated = self.client.login(
            username='testuser',
            password='P@ss4656',
        )
        self.assertTrue(is_authenticated)
