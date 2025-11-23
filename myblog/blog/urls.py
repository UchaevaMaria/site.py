from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('category/<int:category_id>/', views.category_posts, name='category_posts'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='post_list'), name='logout'),
    path('check-answer/<int:problem_id>/', views.check_problem_answer, name='check_answer'),
    path('create-post/', views.create_post, name='create_post'),
    path('post/<int:post_id>/add-problem/', views.add_problem_to_post, name='add_problem'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
]