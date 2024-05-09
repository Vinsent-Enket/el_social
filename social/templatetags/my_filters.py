from django import template
from django.utils.safestring import mark_safe

register = template.Library()

# Создание фильтра
@register.filter()
def trim_to(text):
    if len(text) > 100:
        result = text[:100]
    else:
        result = text
    return mark_safe(result)

@register.filter()
def mymedia(value):
    if value:
        return f'/media/{value}'
