from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _


class CustomManager(BaseUserManager):

    def _create_user(self, email, username, password, **extra_fields):
        if not email:
            raise ValueError('Должна быть электронная почта')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_admin', True)

        return self._create_user(email, username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=True)
    username = models.CharField(verbose_name='имя', max_length=150)

    is_staff = models.BooleanField(_('staff status'), default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(_('active'), default=True)
    objects = CustomManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    def __str__(self):
        return f'{self.username}, {self.email if self.email else "no email"}'

    def get_full_name(self):
        return f'{self.username}, {self.email if self.email else "no email"}'

    def get_short_name(self):
        return self.username
    class Meta:
        verbose_name = 'Пользователя'
        verbose_name_plural = 'Пользователи'
