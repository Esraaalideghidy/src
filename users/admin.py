from .models import User, ContactInfo, ContactUs, Profile
from django.contrib import admin
# Register your models here.
admin.site.register(User)
admin.site.register(Profile)
admin.site.register(ContactUs)
admin.site.register(ContactInfo)