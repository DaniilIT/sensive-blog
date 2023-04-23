from django.contrib import admin
from django.utils.safestring import mark_safe

from blog.models import Post, Tag, Comment

admin.site.register(Tag)


class TagPostInline(admin.TabularInline):
    model = Tag.posts.through
    raw_id_fields = ('tag',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_at')
    search_fields = ['title']
    list_filter = ('published_at',)

    fields = ['title', 'slug', 'image', 'preview',
              'text', 'author', 'published_at', 'likes']
    readonly_fields = ['published_at', 'preview']
    raw_id_fields = ('likes',)

    inlines = [
        TagPostInline,
    ]

    def preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="max-height: 200px;">')
        return 'Файл не выбран'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'author', 'published_at')
    search_fields = ['text']
    list_filter = ('published_at',)
    readonly_fields = ['published_at']

    raw_id_fields = ('post', 'author')
