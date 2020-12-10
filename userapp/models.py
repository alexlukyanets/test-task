from django.contrib.auth.models import AbstractUser
from django.db import models
# from tags.models import ContentItem


class User(AbstractUser):
    is_company_admin = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
