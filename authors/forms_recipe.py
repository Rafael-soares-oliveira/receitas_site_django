from django.core.exceptions import ValidationError
from django import forms
from recipes.models import Recipe
from collections import defaultdict
from utils.functions import is_positive_number
from django.utils.translation import gettext as _


class AuthorsRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._my_errors = defaultdict(list)

    class Meta:
        model = Recipe
        fields = ['title', 'description', 'preparation_time',
                  'preparation_time_unit', 'servings', 'servings_unit',
                  'preparation_step', 'cover',]

        widgets = {
            'cover': forms.FileInput(
                attrs={
                    'class': 'span-2'
                }),
            'preparation_step': forms.Textarea(
                attrs={
                    'class': 'span-2'
                }),
            'servings_unit': forms.Select(
                choices=(
                    (_('Servings'), _('Servings')),
                    (_('Persons'), _('Persons')),
                    )
                    ),
            'preparation_time_unit': forms.Select(
                choices=(
                    (_('Minutes'), _('Minutes')),
                    (_('Hours'), _('Hours')),
                )
            )
        }

    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)

        if self._my_errors:
            raise ValidationError(self._my_errors)

        return super_clean

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            self._my_errors['title'].append(_('Must have at least 5 chars.'))
        return title

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if len(description) < 15:
            self._my_errors['description'].append(
                _('Please, give more details. At least 15 chars'))
        return description

    def clean_preparation_time(self):
        preparation_time = self.cleaned_data.get('preparation_time')
        if not is_positive_number(preparation_time):
            self._my_errors['preparation_time'].append(
                _('Must be a positive number.'))
        return preparation_time

    def clean_servings(self):
        servings = self.cleaned_data.get('servings')
        if not is_positive_number(servings):
            self._my_errors['servings'].append(
                _('Must be a positive number.'))
        return servings
