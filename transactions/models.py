from django.db import models

from users.models import Subscription, User


class Transaction(models.Model):
    price = models.IntegerField(verbose_name="Цена")
    date = models.DateField(auto_now=True, verbose_name="Дата")
    executed = models.BooleanField(default=False, verbose_name="Выполнено")
    payer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Покупатель", related_name="payer")

    def __str__(self):
        return f'{self.subscription} - {self.user}'

    class Meta:
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'
        ordering = ['-date']

# Create your models here.
