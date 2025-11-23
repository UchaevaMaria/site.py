from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import math
import re

from .models import Post, Category, Comment, Problem
from .forms import CommentForm, RegisterForm, PostForm, ProblemForm


def post_list(request):
    query = request.GET.get('q')
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    categories = Category.objects.all()

    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(theory_content__icontains=query)
        )

    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/post_list.html', {
        'page_obj': page_obj,
        'posts': posts,
        'categories': categories,
        'query': query
    })


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all().order_by('-created_date')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form
    })


def category_posts(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    posts = Post.objects.filter(category=category, published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/category_posts.html', {'category': category, 'posts': posts})


def categories_list(request):
    categories = Category.objects.all()
    return render(request, 'blog/categories.html', {'categories': categories})


def check_problem_answer(request, problem_id):
    problem = get_object_or_404(Problem, id=problem_id)
    user_answer = request.POST.get('answer', '').strip().lower()
    correct_answer = problem.correct_answer.strip().lower() if problem.correct_answer else ""

    is_correct = False
    feedback = ""

    if not correct_answer:
        # Если правильный ответ не задан, всегда показываем решение
        is_correct = True
        feedback = "Правильный ответ не задан. Показано решение."

    elif problem.answer_type == 'number':
        try:
            user_num = float(user_answer)
            correct_num = float(correct_answer)
            is_correct = math.isclose(user_num, correct_num, rel_tol=1e-5)
            feedback = "✅ Правильно! Отличная работа! 🎉" if is_correct else "❌ Неправильно. Попробуйте еще раз! 💪"
        except ValueError:
            is_correct = False
            feedback = "❌ Пожалуйста, введите число"

    elif problem.answer_type == 'text':
        is_correct = user_answer == correct_answer
        feedback = "✅ Правильно! Отличная работа! 🎉" if is_correct else "❌ Неправильно. Попробуйте еще раз! 💪"

    elif problem.answer_type == 'formula':
        user_answer = re.sub(r'\s+', '', user_answer)
        correct_answer = re.sub(r'\s+', '', correct_answer)
        is_correct = user_answer == correct_answer
        feedback = "✅ Правильно! Отличная работа! 🎉" if is_correct else "❌ Неправильно. Попробуйте еще раз! 💪"

    elif problem.answer_type == 'multiple':
        is_correct = user_answer == correct_answer
        feedback = "✅ Правильно! Отличная работа! 🎉" if is_correct else "❌ Неправильно. Попробуйте еще раз! 💪"

    # ВОЗВРАЩАЕМ solution ТОЛЬКО ПРИ ПРАВИЛЬНОМ ОТВЕТЕ
    return JsonResponse({
        'is_correct': is_correct,
        'feedback': feedback,
        'solution': problem.solution if is_correct else ""  # Пустая строка при неправильном ответе
    })


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Аккаунт успешно создан! Теперь войдите.')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'blog/register.html', {'form': form})


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user.is_superuser or request.user.username == comment.author:
        comment.delete()
    return redirect('post_detail', pk=comment.post.pk)


# Дополнительные views для создания/редактирования постов и задач
@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})


@login_required
def add_problem_to_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = ProblemForm(request.POST)
        if form.is_valid():
            problem = form.save(commit=False)
            problem.post = post
            problem.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = ProblemForm()
    return render(request, 'blog/problem_form.html', {'form': form, 'post': post})