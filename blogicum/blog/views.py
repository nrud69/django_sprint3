from django.shortcuts import render, get_object_or_404
from django.http import Http404
from blog.models import Post, Category
from django.db.models import Q
from django.utils import timezone
from .models import Post


def index(request):
    post_list = Post.objects.select_related(
        'category', 'location', 'author'
    ).filter(
        Q(is_published=True) & 
        Q(pub_date__lte=timezone.now()) & 
        Q(category__is_published=True)  # Фильтруем по опубликованной категории
    ).order_by('-pub_date')[:5]

    # Словарь контекста
    context = {
        'post_list': post_list,
    }

    # Рендерим шаблон
    template_name = 'blog/index.html'
    return render(request, template_name, context)


def post_detail(request, id):  
    post = get_object_or_404(
        Post.objects.select_related('author', 'category', 'location'),
        id=id,
        is_published=True
    )

    if not post.category.is_published:
        raise Http404("Category is not published.")

    if post.pub_date > timezone.now():
        raise Http404("Post is scheduled for the future.")

    context = {'post': post}
    return render(request, 'blog/detail.html', context)


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category.objects.filter(is_published=True),
        slug=category_slug
    )

    current_time_local = timezone.localtime(timezone.now())

    # category.save()

    posts = Post.objects.filter(
        category=category,
        is_published=True,
        pub_date__lte=current_time_local
    ).order_by('-pub_date')

    context = {
        'category': category,
        'post_list': posts,
    }

    return render(request, 'blog/category.html', context)
