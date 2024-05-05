from rest_framework.serializers import ValidationError


class LevelValidator:
    """
    Валидатор времени выполнения привычки
    """

    def __init__(self, post_level, author_level):
        self.post_level = post_level
        self.author_level = author_level

    def __call__(self, value):
        if self.post_level > self.author_level:
            raise ValidationError(
                f'Уровень поста {self.post_level} '
                f'а ваш уровень  {self.author_level}'
                f'Операция недоступна')
