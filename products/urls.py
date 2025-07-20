from django.urls import path
from .views import *

urlpatterns = [
    path('category/', category, name='category'),
    path('single-product/<int:pk>/', single_product, name='single-product'),
    # path('comment/<int:product_id>', save_comment, name='comment'),
    path('category/<slug:slug>/', category_detail, name='category_detail'),
    path('product/<int:product_id>/comment/',
         save_comment, name='submit_comment'),
    path('product/<int:product_id>/review/',
         save_review, name='submit_review'),
    
]
