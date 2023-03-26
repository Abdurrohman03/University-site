from django.contrib import admin
from .models import Post, Comment, Body


class BodyInline(admin.TabularInline):
    model = Body
    extra = 0


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [BodyInline]
    list_display = ['id', 'title', 'created_date', 'author', 'image_tag']
    readonly_fields = ['created_date', 'image_tag']
    filter_horizontal = ['tags']
    date_hierarchy = 'created_date'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'created_date', 'parent_comment', 'top_level_comment_id']



