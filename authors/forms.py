import re
from typing import Any
from django.core.exceptions import ValidationError
from django import forms
from django.contrib.auth.models import User


def strong_password(password):
    regex = re.compile(r'(?=.*[a-z])(?=.*[a-z])(?=.*[0-9]).{8,}$')
    if not regex.match(password):
        raise ValidationError((
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. '
            'The length should be at least 8 characters.'
        ),
            code='invalid',
        )


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
            'password_confirm'
        ]

    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Type your first name',
        }),
        label='First name',
        error_messages={
            'required': 'This field must not be empty'
        },
    )

    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Type your last name',
        }),
        label='Last name',
        error_messages={
            'required': 'This field must not be empty'
        },
    )

    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Type your username',
        }),
        help_text='Username must have letters, numbers or one of those @.+-_.'
        ' The length should be between 4 and 16 characters.',
        label='Username',
        min_length=4,
        max_length=16,
        error_messages={
            'required': 'This field must not be empty',
            'min_length': 'Username must have at least 4 characters',
            'max_length': 'Username must have a maximum of 16 characters',
        },
    )

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Type your email. Ex: email@email.com'
        }),
        label='Email',
        error_messages={
            'required': 'This field must not be empty'
        },
    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Type your password',
        }),
        label='Password',
        error_messages={
            'required': 'This field must not be empty'
        },
        help_text=(
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number.'
            ' The length should be at least 8 characters.'
        ),
        validators=[strong_password]
    )

    password_confirm = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repeat your password',
        }),
        label='Confirm password',
        error_messages={
            'required': 'This field must not be empty'
        },
    )

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        exists = User.objects.filter(email=email).exists()

        if exists:
            raise ValidationError(
                'User e-mail is already in use', code='invalid')

        return email

    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password != password_confirm:
            raise ValidationError(
                {'password': 'Passwords do not match!',
                 'password_confirm': 'Passwords do not match!'},
            )

        return cleaned_data
