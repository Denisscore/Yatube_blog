from django.contrib import admin
from .models import Group, Post, Comment


class PostGroup(admin.ModelAdmin):
    list_display = ("pk", "title", "slug", "description")
    empty_value_display = "-пусто-"


class PostAdmin(admin.ModelAdmin):
    list_display = ("pk", "text", "pub_date", "author")
    search_fields = ("text",)
    list_filter = ("pub_date",)
    empty_value_display = "-пусто-"


class CommentAdmin(admin.ModelAdmin):
    list_display = ("author", "created", "text")
    search_fields = ("text",)
    list_filter = ("created",)
    empty_value_display = "-пусто-"

admin.site.register(Post, PostAdmin)
admin.site.register(Group, PostGroup)
admin.site.register(Comment, CommentAdmin)
