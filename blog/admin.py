from django.contrib import admin

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
    readonly_fields = ['published_at']

    raw_id_fields = ('likes',)
    exclude = ('tags',)
    inlines = [
        TagPostInline,
    ]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'author', 'published_at')
    search_fields = ['text']
    list_filter = ('published_at',)
    readonly_fields = ['published_at']

    raw_id_fields = ('post', 'author')
