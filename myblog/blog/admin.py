from django.contrib import admin
from .models import Category, Post, Problem, Comment


class ProblemInline(admin.TabularInline):
    model = Problem
    extra = 1
    fields = [
        'order',
        'question',
        'correct_answer',
        'answer_type',
        'tolerance',
        'multiple_choices',
        'solution',
        'hint'
    ]
    ordering = ['order']


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ['author', 'created_date']
    can_delete = True


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'difficulty', 'reading_time', 'published_date', 'created_date']
    list_filter = ['difficulty', 'category', 'published_date', 'created_date']
    search_fields = ['title', 'content', 'theory_content']
    list_editable = ['difficulty', 'reading_time']
    inlines = [ProblemInline, CommentInline]
    fieldsets = [
        ('Основная информация', {
            'fields': ['title', 'author', 'category', 'image']
        }),
        ('Содержание', {
            'fields': ['content', 'theory_content']
        }),
        ('Настройки', {
            'fields': ['difficulty', 'reading_time', 'published_date']
        }),
    ]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'color']
    list_editable = ['color']
    search_fields = ['name']


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = [
        'post',
        'order',
        'answer_type',
        'correct_answer',
        'question_preview'
    ]
    list_filter = ['post', 'answer_type']
    search_fields = ['question', 'solution', 'correct_answer']
    ordering = ['post', 'order']
    list_editable = ['order', 'answer_type']

    fieldsets = [
        ('Основная информация', {
            'fields': ['post', 'order', 'question']
        }),
        ('Проверка ответов', {
            'fields': [
                'correct_answer',
                'answer_type',
                'tolerance',
                'multiple_choices'
            ]
        }),
        ('Решение и подсказки', {
            'fields': ['solution', 'hint']
        }),
    ]

    def question_preview(self, obj):
        return obj.question[:80] + '...' if len(obj.question) > 80 else obj.question

    question_preview.short_description = 'Вопрос'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'created_date', 'text_preview']
    list_filter = ['created_date', 'post']
    search_fields = ['author', 'text']
    readonly_fields = ['created_date']

    def text_preview(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text

    text_preview.short_description = 'Текст комментария'