from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default='#446A7D')

    def __str__(self):
        return self.name


class Post(models.Model):
    DIFFICULTY_LEVELS = [
        ('beginner', 'Начальный'),
        ('intermediate', 'Средний'),
        ('advanced', 'Продвинутый'),
    ]

    title = models.CharField(max_length=200)
    content = models.TextField()
    theory_content = models.TextField(blank=True, null=True, help_text="Теоретическая часть")
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_LEVELS, default='beginner')
    reading_time = models.IntegerField(default=5, help_text="Время чтения в минутах")

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class Problem(models.Model):
    ANSWER_TYPES = [
        ('text', 'Текстовый ответ'),
        ('number', 'Числовой ответ'),
        ('formula', 'Математическая формула'),
        ('multiple', 'Множественный выбор'),
    ]

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='problems')
    question = models.TextField()
    solution = models.TextField()
    hint = models.TextField(blank=True)
    order = models.IntegerField(default=0)

    # НОВЫЕ ПОЛЯ ДЛЯ АВТОМАТИЧЕСКОЙ ПРОВЕРКИ
    correct_answer = models.CharField(
        max_length=200,
        blank=True,
        help_text="Правильный ответ для автоматической проверки"
    )
    answer_type = models.CharField(
        max_length=20,
        choices=ANSWER_TYPES,
        default='text',
        help_text="Тип ответа для правильной проверки"
    )
    tolerance = models.FloatField(
        default=0.01,
        help_text="Допустимая погрешность для числовых ответов"
    )
    multiple_choices = models.TextField(
        blank=True,
        help_text="Варианты ответов через запятую (для множественного выбора)"
    )

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Задача к {self.post.title}"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=100)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Комментарий от {self.author} к "{self.post}"'