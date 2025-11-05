from django import forms
from .models import Comment
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'text']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'image']

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
