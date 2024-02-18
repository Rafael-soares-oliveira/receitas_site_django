from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from recipes.models import Recipe
import os


def delete_cover(instance):
    try:
        os.remove(instance.cover.path)
    except (ValueError, FileNotFoundError):
        ...


# Delete the cover when delete the recipe
@receiver(pre_delete, sender=Recipe)
def recipe_cover_delete(sender, instance, *args, **kwargs):
    old_instance = Recipe.objects.filter(pk=instance.pk).first()
    if old_instance:
        delete_cover(old_instance)


# Delete the old cover when change the cover
@receiver(pre_save, sender=Recipe)
def recipe_cover_update(sender, instance, *args, **kwargs):
    old_instance = Recipe.objects.filter(pk=instance.pk).first()
    if not old_instance:
        return

    is_new_cover = old_instance.cover != instance.cover
    if is_new_cover:
        delete_cover(old_instance)