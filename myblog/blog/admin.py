from django.contrib import admin
from .models import Category, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_date', 'published_date', 'category']
    list_filter = ['created_date', 'published_date', 'category']
    search_fields = ['title', 'content']
    date_hierarchy = 'created_date'

    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'content', 'author', 'category')
        }),
        ('Даты', {
            'fields': ('created_date', 'published_date')
        }),
        ('Медиа', {
            'fields': ('image',)
        }),
    )
