from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from .models import Post, Category

COUNT_NUM: int = 5


def index(request):
    """Главная страница проекта"""
    post_list = Post.objects.select_related(
        'category'
    ).filter(pub_date__lte=timezone.now(),
             is_published=True,
             category__is_published=True)[:COUNT_NUM]
    context = {
        'post_list': post_list
    }
    return render(request, 'blog/index.html', context)


def post_detail(request, id):
    """Страница категории"""
    posts = get_object_or_404(
        Post.objects.filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=timezone.now(),
            pk=id
        )
    )
    context = {
        'post': posts
    }
    return render(request, 'blog/detail.html', context)


def category_posts(request, category_slug):
    """Страница отдельной публикации"""
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    post_list = Post.objects.select_related(
        'category',
    ).filter(
        category=category,
        is_published=True,
        pub_date__lte=timezone.now()
    )
    context = {
        'post_list': post_list
    }
    return render(request, 'blog/category.html', context)
