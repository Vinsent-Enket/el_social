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
    wallet = models.IntegerField(default=0, verbose_name='Баланс')
    author_level = models.IntegerField(default=0, verbose_name='Уровень автора')
    USERNAME_FIELD = "telephone"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.name}, {self.email}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Subscription(models.Model):
    level = (
        ('0', 'Free'),
        ('1', 'Basic'),
        ('2', 'Premium'),
        ('3', 'Pro')
    )
    level = models.CharField(max_length=1, choices=level, verbose_name='Уровень подписки')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='На кого подписан',
                               related_name='subscribed_to')
    proprietor = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Подписчик', related_name='subscriber')
    price = models.IntegerField(default=0, verbose_name='Цена подписки')

    def save(self, *args, **kwargs):
        if self.level == '1':
            self.price = 100
        elif self.level == '2':
            self.price = 200
        elif self.level == '3':
            self.price = 300
        super().save(*args, **kwargs)

# Create your models here.
