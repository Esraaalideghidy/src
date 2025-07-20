from django.urls import path
from .views import *

urlpatterns = [
    path('cart/', cart, name='cart'),
    path('checkout/', checkout, name='checkout'),
    path('update_item/', updateItem, name="update_item"),
    path('confirmation/', confirmation, name='confirmation'),
    path('process_order/', processOrder, name="process_order"),
    
]
    