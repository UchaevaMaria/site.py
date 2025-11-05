from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Post, Category, Comment
from .forms import CommentForm, RegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def post_list(request):
    query = request.GET.get('q')
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

    if query:
        posts = posts.filter(Q(title__icontains=query) | Q(content__icontains=query))

    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/post_list.html', {'page_obj': page_obj, 'query': query})

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
