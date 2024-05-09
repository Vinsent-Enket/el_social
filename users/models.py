from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

NULLABLE = {'blank': True, 'null': True}
phone_regex = RegexValidator(regex=r'^\+?\d{9,15}$', message='Телефон должен содержать от 9 до 15 цифр')


class User(AbstractUser):
    username = None
    # Регистрация по номеру телефона
    telephone = models.CharField(max_length=20, validators=[phone_regex], verbose_name='Телефон', unique=True)
    first_name = models.CharField(max_length=20, verbose_name='Имя')
    last_name = models.CharField(max_length=20, verbose_name='Фамилия')
    email = models.EmailField(verbose_name='Email', unique=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Аватар')
    description = models.CharField(max_length=20, verbose_name='О себе')
    wallet = models.IntegerField(default=0, verbose_name='Баланс')
    USERNAME_FIELD = "telephone"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.first_name}, {self.email}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Subscription(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='На кого подписан',
                               related_name='subscribed_to')
    proprietor = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Подписчик', related_name='subscriber')


# Create your models here.
