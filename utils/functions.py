from django.core.exceptions import ValidationError
import re


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


def is_positive_number(value):
    try:
        number_string = float(value)
    except ValueError:
        return False
    return number_string > 0


print(is_positive_number('10.5'))
