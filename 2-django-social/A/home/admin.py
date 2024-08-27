from django.contrib import admin
from .models import Post, Comment, Vote

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'body', 'slug', 'created_at', 'updated_at')
    search_fields = ('body', 'slug')
    list_filter = ('updated_at',)
    prepopulated_fields = {'slug': ('body',)}
    raw_id_fields = ('user',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'post', 'reply', 'is_reply', 'body', 'created_at')
    search_fields = ('body',)
    list_filter = ('created_at',)
    raw_id_fields = ('user', 'post', 'reply')

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'post')
    raw_id_fields = ('user', 'post')