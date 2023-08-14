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
    )[:COUNT_NUM]
    context = {'post_list': post_list}
    return render(request, template, context)


def post_detail(request, post_id):
    """Страница категории"""
    post = get_object_or_404(
        Post.objects.filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=TIME,
        ),
        pk=post_id
    )
    context = {'post': post}
    return render(request, 'blog/detail.html', context)


def category_posts(request, category_slug):
    """Страница отдельной публикации"""
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    post_list = Post.objects.filter(
        category__slug=category_slug,
        is_published=True,
        pub_date__lte=TIME
    )
    context = {
        'category': category,
        'post_list': post_list,
    }
    return render(request, 'blog/category.html', context=context)