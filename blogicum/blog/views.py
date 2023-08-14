from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from .models import Post, Category

COUNT_NUM: int = 5
TIME = timezone.now()


def index(request):
    template = 'blog/index.html'
    post_list = Post.objects.filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=TIME
    ).order_by('-created_at')[:COUNT_NUM]
    context = {'posts': post_list}
    return render(request, template, context)


def post_detail(request, id):
    """Страница категории"""
    posts = get_object_or_404(
        Post.objects.filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=TIME,
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
        pub_date__lte=TIME
    )
    context = {
        'post_list': post_list
    }
    return render(request, 'blog/category.html', context)
