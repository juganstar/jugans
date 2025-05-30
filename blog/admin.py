from django.contrib import admin
from .models import Post, Category, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'status', 'publish_date')
    list_filter = ('status', 'category')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    actions = ['approve_posts', 'reject_posts']  # Actions for PostAdmin

    def approve_posts(self, request, queryset):
        queryset.update(status='published')  # Approve selected posts
    approve_posts.short_description = "Approve selected posts"

    def reject_posts(self, request, queryset):
        queryset.update(status='draft')  # Send back to draft
    reject_posts.short_description = "Reject selected posts"

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_date', 'active')
    list_filter = ('active', 'created_date')
    search_fields = ('user__username', 'post__title', 'text')
    actions = ['approve_comments']  # Action for CommentAdmin

    def approve_comments(self, request, queryset):
        queryset.update(active=True)  # Approve selected comments
    approve_comments.short_description = "Approve selected comments"