from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist

from social.models import Content, Comment


# Register your models here.

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'content', 'date')


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'text', 'date', 'like_count', 'comment_count')

    def get_form(self, request, *args, **kwargs):
        form = super().get_form(request, *args, **kwargs)
        self.prepare_like_form(form)
        self.prepare_comment_form(form)
        return form

    def prepare_like_form(self, form):
        if 'likes' in form.base_fields:
            form.base_fields['likes'].queryset = form.base_fields['likes'].queryset.select_related('post')

    def prepare_comment_form(self, form):
        if 'comment' in form.base_fields:
            form.base_fields['comment'].queryset = form.base_fields['comment'].queryset.select_related('post')

    # def save_formset(self, request, form, formset, change):
    #     instances = formset.save(commit=False)
    #     for instance in instances:
    #         if not instance.pk:
    #             try:
    #                 post = Content.objects.get(id=instance.post.id)
    #                 instance.post = post
    #                 instance.save()
    #             except (ObjectDoesNotExist, ValueError):
    #                 formset.management_form.errors.append(
    #                     'Пост не найден.'
    #                 )
    #                 continue
    #             instance.save()
    #             formset.save_m2m()
