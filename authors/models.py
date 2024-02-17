from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _

User = get_user_model()


class Profile(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE,
                                  verbose_name=_('Author'))
    bio = models.TextField(default='', blank=True)

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')
