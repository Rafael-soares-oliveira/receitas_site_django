from collections import defaultdict
from typing import Any
from authors.models import Profile
from utils.functions import strong_password
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserChangeForm
from django.utils.translation import gettext as _


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
            'placeholder': _('Type your first name'),
        }),
        label=_('First Name'),
        error_messages={
            'required': _('This field must not be empty')
        },
    )

    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': _('Type your last name'),
        }),
        label=_('Last Name'),
        error_messages={
            'required': _('This field must not be empty')
        },
    )

    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': _('Type your username'),
        }),
        help_text=_(
            'Username must have letters, numbers or one of those @.+-_.'
            ' The length should be between 4 and 16 characters.'),
        label=_('Username'),
        min_length=4,
        max_length=16,
        error_messages={
            'required': _('This field must not be empty'),
            'min_length': _('Username must have at least 4 characters'),
            'max_length': _('Username must have a maximum of 16 characters'),
        },
    )

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': _('Type your email. Ex: email@email.com')
        }),
        label='Email',
        error_messages={
            'required': _('This field must not be empty')
        },
    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': _('Type your password'),
        }),
        label=_('Password'),
        error_messages={
            'required': _('This field must not be empty')
        },
        help_text=(
            _('Password must have at least one uppercase letter, '
              'one lowercase letter and one number.'
              ' The length should be at least 8 characters.')
        ),
        validators=[strong_password]
    )

    password_confirm = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': _('Repeat your password'),
        }),
        label=_('Confirm password'),
        error_messages={
            'required': _('This field must not be empty')
        },
    )

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        exists = User.objects.filter(email=email).exists()

        if exists:
            raise ValidationError(
                _('User e-mail is already in use'), code='invalid')

        return email

    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password != password_confirm:
            raise ValidationError(
                {'password': _('Passwords do not match!'),
                 'password_confirm': _('Passwords do not match!')},
            )

        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': _('Type your username')
        }),
        label=_('Username'),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': _('Type your password')
        }),
        label=_('Password'),
    )


class ProfileFormEdit(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._my_errors = defaultdict(list)

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
        ]

        def clean(self, *args, **kwargs):
            super_clean = super().clean(*args, **kwargs)

            if self._my_errors:
                raise ValidationError(self._my_errors)

            return super_clean

        def clean_email(self):
            email = self.cleaned_data.get('email', '')
            exists = User.objects.filter(email=email).exists()

            if exists:
                raise ValidationError(
                    _('User e-mail is already in use'), code='invalid')

            return email


class MyProfileForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
        ]

    first_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'readonly': 'readonly',
        }),
        label=_('First name'),
    )

    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'readonly': 'readonly',
        }),
        label=_('Last name'),
    )

    email = forms.EmailField(
        widget=forms.TextInput(attrs={
            'readonly': 'readonly',
        }),
        label=_('Email'),
    )


class BioFormEdit(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._my_errors = defaultdict(list)

    class Meta:
        model = Profile
        fields = [
            'bio',
        ]

        def clean(self, *args, **kwargs):
            super_clean = super().clean(*args, **kwargs)

            if self._my_errors:
                raise ValidationError(self._my_errors)

            return super_clean
