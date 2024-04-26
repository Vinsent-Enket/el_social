# Generated by Django 4.2.7 on 2024-04-25 15:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_remove_user_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='wallet',
            field=models.IntegerField(default=0, verbose_name='Баланс'),
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(choices=[('0', 'Free'), ('1', 'Basic'), ('2', 'Premium'), ('3', 'Pro')], max_length=1, verbose_name='Уровень подписки')),
                ('price', models.IntegerField(default=0, verbose_name='Цена подписки')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscribed_to', to=settings.AUTH_USER_MODEL, verbose_name='На кого подписан')),
                ('proprietor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriber', to=settings.AUTH_USER_MODEL, verbose_name='Подписчик')),
            ],
        ),
    ]
