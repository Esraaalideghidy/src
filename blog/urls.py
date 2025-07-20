from .views import *
from django.urls import path

urlpatterns = [
    path('blog/',blog,name='blog'),
    path('single-blog/<int:pk>/', single_blog, name='single-blog'),
    path('category-detail/<slug:slug>/', category_detail, name='category-detail'),
    path('save-comment/<int:blog_id>/', save_comment, name='save-comment'),
]