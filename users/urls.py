from django.urls import path, include
from .views import *


urlpatterns = [
    path('login/', login_customer, name='login'),
    path('register/', register_customer, name='register'),
    path('forgotpassword/', forgotpassword, name='forgotpassword'),
    path('resetpassword_validate/<uidb64>/<token>/',resetpassword_validate, name='resetpassword_validate'),
    path('resetpassword/', resetpassword, name='resetpassword'),
    path('logout/', logout_customer, name='logout'),
    path('contact/', contact, name='contact'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    
]
