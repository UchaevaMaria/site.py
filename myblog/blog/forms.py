from django import forms
from .models import Comment, Post, Problem
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'text']
        widgets = {
            'author': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваше имя'
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Ваш комментарий...'
            })
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title', 
            'content', 
            'theory_content',
            'category', 
            'image',
            'difficulty',
            'reading_time'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название статьи'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Основное содержание статьи...'
            }),
            'theory_content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Теоретическая часть материала...'
            }),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'difficulty': forms.Select(attrs={'class': 'form-control'}),
            'reading_time': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 60
            }),
        }

class ProblemForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = ['question', 'solution', 'hint', 'order', 'correct_answer', 'answer_type', 'tolerance', 'multiple_choices']
        widgets = {
            'question': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Условие задачи...'
            }),
            'solution': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control',
                'placeholder': 'Подробное решение задачи...'
            }),
            'hint': forms.Textarea(attrs={
                'rows': 2,
                'class': 'form-control',
                'placeholder': 'Подсказка для решения (опционально)...'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'correct_answer': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Правильный ответ для проверки...'
            }),
            'answer_type': forms.Select(attrs={'class': 'form-control'}),
            'tolerance': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'multiple_choices': forms.Textarea(attrs={
                'rows': 2,
                'class': 'form-control',
                'placeholder': 'Варианты через запятую: Да, Нет, Не знаю...'
            })
        }
        help_texts = {
            'correct_answer': 'Правильный ответ для автоматической проверки',
            'answer_type': 'Выберите тип ответа',
            'tolerance': 'Допустимая погрешность для числовых ответов',
            'multiple_choices': 'Для типа "Множественный выбор" укажите варианты через запятую',
        }

class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email адрес'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Этот email уже используется.")
        return email