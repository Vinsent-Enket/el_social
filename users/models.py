from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

NULLABLE = {'blank': True, 'null': True}
phone_regex = RegexValidator(regex=r'^\+?\d{9,15}$', message='Телефон должен содержать от 9 до 15 цифр')


class User(AbstractUser):
    username = None
    # Регистрация по номеру телефона
    telephone = models.CharField(max_length=20, validators=[phone_regex], verbose_name='Телефон', unique=True)
    name = models.CharField(max_length=20, verbose_name='Имя')
    email = models.EmailField(verbose_name='Email', unique=True)
    # avatar = models.ImageField(upload_to='avatars', verbose_name='Аватар')
    description = models.CharField(max_length=20, verbose_name='О себе')
    USERNAME_FIELD = "telephone"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.name}, {self.email}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

# Create your models here.
