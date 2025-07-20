from django.contrib import admin
from .models import *
from django.contrib.auth.models import User
# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'available_at', 'is_hot_deal']
    list_filter = ['is_hot_deal']
class variationAdmin(admin.ModelAdmin):
    list_display = ['product', 'variation_category', 'variation_value','is_active']
    list_editable=('is_active',)
    list_filter = ['product', 'variation_category',
                   'variation_value']
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(variation, variationAdmin)

admin.site.register(Comment)
admin.site.register(Reviews)
admin.site.register(User)




