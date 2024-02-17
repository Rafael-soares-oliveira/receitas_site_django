from collections import defaultdict
from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
from django.utils.text import slugify
from tag.models import Tag
from django.utils.translation import gettext as _


class Category(models.Model):
    name = models.CharField(max_length=65)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')


class Recipe(models.Model):
    title = models.CharField(max_length=65, verbose_name=_('Title'))
    description = models.CharField(
        max_length=165, verbose_name=_('Description'))
    slug = models.SlugField(unique=True, null=True)
    preparation_time = models.IntegerField(verbose_name=_('Preparation Time'))
    preparation_time_unit = models.CharField(
        max_length=65, verbose_name=_('Preparation Time Unit'))
    servings = models.IntegerField(verbose_name=_('Servings'))
    servings_unit = models.CharField(
        max_length=65, verbose_name=_('Servings Unit'))
    preparation_step = models.TextField(verbose_name=_('Preparation Step'))
    preparation_step_is_html = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    cover = models.ImageField(
        upload_to='media/covers/%Y/%m/%d', blank=False,
        default='tests/tests_recipes/imagem_temporaria.jpg',
        verbose_name=_('Cover'))
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True,
        default=None)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(Tag, blank=True, default='')

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f'{slugify(self.title)}'
            self.slug = slug
        return super().save(*args, **kwargs)

    def clean(self, *args, **kwargs):
        error_messages = defaultdict(list)
        recipe_from_db = Recipe.objects.filter(title__iexact=self.title
                                               ).first()
        if recipe_from_db:
            if recipe_from_db.pk != self.pk:
                error_messages['title'].append(
                    _('Found recipes with the same title')
                )

        if error_messages:
            raise ValidationError(error_messages)

    class Meta:
        verbose_name = _('Recipe')
        verbose_name_plural = _('Recipes')
