from django.urls import path
from .views import *


urlpatterns = [
    path('', home, name='home'),
    path('search/', search, name='search'),
    # path('about/', about, name='about'),
    # path('contact/', contact, name='contact')
]
