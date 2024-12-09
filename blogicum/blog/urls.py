from django.urls import path

from . import views

app_name = 'blog'
ur = 'category/<slug:category_slug>/'

urlpatterns = [
    path('', views.index, name='index'),
    path('posts/<int:id>/', views.post_detail, name='post_detail'),
    path(ur, views.category_posts, name='category_posts'),
]
