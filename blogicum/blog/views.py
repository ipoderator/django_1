from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from .models import Post, Category


def index(request):
    template = 'blog/index.html'
    post_list = Post.objects.filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=timezone.now()
    ).order_by('-created_at')[:5]
    context = {'posts': post_list}
    return render(request, template, context)


def post_detail(request, post_id):
    template = 'blog/detail.html'
    post = get_object_or_404(
        Post.objects.filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=timezone.now(),
            pk=post_id))
    context = {'post': post}
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True)
    category_list = Post.objects.select_related(
        'category',
        'author',
        'location'
    ).filter(
        is_published=True,
        category__slug=category_slug,
        pub_date__lte=timezone.now()
    )
    context = {
        'category': category,
        'post_list': category_list
    }
    return render(request, template, context)
