from django.db import models

from users.models import User

NULLABLE = {'blank': True, 'null': True}


# Create your models here.


class Content(models.Model):
    name = models.CharField(max_length=120, verbose_name="Название поста")
    text = models.TextField(verbose_name="Текст поста", **NULLABLE)
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    image = models.ImageField(upload_to="social/", verbose_name="Изображение", **NULLABLE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор", related_name="content_author")
    subscribers_only = models.BooleanField(default=False, verbose_name="Только для подписчиков")

    # добавить поле для требуемого уровня подписки
    def get_like_count(self):
        return self.like_set.count()

    like_count = property(get_like_count)

    def get_comment_count(self):
        return self.comment_content.count()

    comment_count = property(get_comment_count)

    def __str__(self):
        return f'Пост про {self.name}'

    class Meta:
        ordering = ['-date']
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class Like(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE, verbose_name="Лайк")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь", related_name='like_author')


class Comment(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE, verbose_name="Комментарий",
                                related_name='comment_content')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор", related_name='comment_author')
    text = models.TextField(verbose_name="Текст комментария")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    is_paid = models.BooleanField(default=False, verbose_name="Платный комментарий")

    # cost = models.IntegerField(**NULLABLE, verbose_name="Стоимость") нужно сделать привязку к модели транзакция

    def __str__(self):
        return f'Комментарий к {self.content}'

    class Meta:
        ordering = ['-date']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
