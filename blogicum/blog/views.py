from django.shortcuts import render
from django.utils.timezone import make_aware
from django.http import Http404
from blog.models import Post, Category
from django.db.models import Q
import datetime
from django.shortcuts import render
from django.db.models import Q
import datetime
from .models import Post


def index(request):
    today_date = datetime.date.today()

    post_list = Post.objects.select_related(
        'category', 'location', 'author'
    ).filter(
        Q(is_published=True) & 
        Q(pub_date__date__lt=today_date) & 
        Q(category__is_published=True)  # Фильтруем по опубликованной категории
    ).order_by('-pub_date')[1:6]

    # Словарь контекста
    context = {
        'post_list': post_list,
    }

    # Рендерим шаблон
    template_name = 'blog/index.html'
    return render(request, template_name, context)


def post_detail(request, id):
    try:
        # Фильтрация на уровне базы данных
        post = Post.objects.filter(
            id=id,
            is_published=True,
            pub_date__lte=make_aware(datetime.datetime.now()),
            category__is_published=True
        ).first()

        if not post:
            raise Http404("Пост не найден или снят с публикации")

    except Post.DoesNotExist:
        raise Http404("Пост не найден")

    context = {
        'post': post
    }
    template_name = 'blog/detail.html'

    return render(request, template_name, context)


def category_posts(request, category_slug):
    today_date = datetime.date.today()

    # Попытка найти категорию по slug
    try:
        category = Category.objects.get(slug=category_slug)
    except Category.DoesNotExist:
        raise Http404("Категория не найдена")

    # Если категория не опубликована, возвращаем ошибку 404
    if not category.is_published:
        raise Http404("Категория не опубликована")

    # Фильтруем посты по категории и датам
    post_list = Post.objects.select_related(
        'category', 'location', 'author'
    ).filter(
        Q(is_published=True) &
        Q(pub_date__date__lt=today_date) &
        Q(category__slug=category_slug)
    )

    context = {
        'post_list': post_list,
        'category': category,
    }
    template_name = 'blog/category.html'

    return render(request, template_name, context)
